# C24-3 · 实现
> 阅读约 15 分钟，建议在电脑前跟着敲。目标：写出能跑的最小闭环，再逐步加混合检索、重排、拒答，最终每个答案都能点回原文。

## 1. 先跑通最小闭环，别一步到位

新手最常见的死法是一上来就把混合检索、重排、拒答全写上，结果哪里错了都不知道。

> 铁律：**先跑通「切分 → embedding → 向量检索 → 生成」这条最短路**，能问能答了，再一项一项加料。每加一项，跑一次评测集看数字涨没涨。

下面代码用 OpenAI 兼容接口 + Chroma（本地向量库），换 `base_url` 可接 DeepSeek、通义等。骨架可跑，注释标了哪些是「教学简化」。

## 2. 文档加载与切分

```python
import re
from pathlib import Path

def load_markdown(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")

def split_by_structure(text: str, max_tokens=500, overlap=60) -> list[str]:
    """先按标题切大块，再按段落切小块，块间重叠。"""
    sections = re.split(r"(?=^#{1,3} )", text, flags=re.M)   # 标题是天然语义边界
    chunks = []
    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
        buf, buf_len = "", 0
        for p in sec.split("\n\n"):                  # 大块内按段落切
            approx = len(p) // 2                       # 粗略估算 token（中文约 2 字符/token）
            if buf and buf_len + approx > max_tokens:
                chunks.append(buf.strip())
                buf = buf[-overlap:]                   # 重叠：带上上块结尾
                buf_len = len(buf) // 2
            buf += p + "\n\n"
            buf_len += approx
        if buf.strip():
            chunks.append(buf.strip())
    return chunks
```

> 这里的 token 估算是「够用即止」的近似，生产里应调用 tokenizer 精确计数（见 C3）。关键是**别按固定字符数硬切**——`re.split` 按标题切，才让边界贴住语义。

## 3. Embedding 与向量库写入

```python
import chromadb
from openai import OpenAI

client = OpenAI()   # 生成与 embedding 都走它，或单独配 embedding 客户端
chroma = chromadb.PersistentClient(path="./kb_store")
collection = chroma.get_or_create_collection("kb")

def embed(texts: list[str]) -> list[list[float]]:
    r = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [d.embedding for d in r.data]

def index_documents(doc_path: str, doc_id: str):
    chunks = split_by_structure(load_markdown(doc_path))
    for i, c in enumerate(chunks):
        collection.add(
            ids=[f"{doc_id}:{i}"],               # 引用 id：从切分就埋进去
            documents=[c],
            embeddings=embed([c]),
            metadatas=[{"doc": doc_id, "chunk": i, "source": doc_path}],
        )
    print(f"indexed {len(chunks)} chunks from {doc_id}")
```

> `f"{doc_id}:{i}"` 就是 C24-2 说的「贯穿全链路的身份」。向量库里除了向量，还存了原文和来源路径——后面回链就靠 metadata。

## 4. 检索（先纯向量，最小闭环）

```python
def retrieve(query: str, k=6) -> list[dict]:
    qv = embed([query])[0]
    res = collection.query(query_embeddings=[qv], n_results=k)
    return [
        {"id": res["ids"][0][j],
         "text": res["documents"][0][j],
         "doc": res["metadatas"][0][j]["doc"]}
        for j in range(len(res["ids"][0]))
    ]
```

## 5. 带引用约束的生成 prompt

这是「可溯源」的落点。把检索到的 chunk 编号，强制模型逐断言引用：

```python
SYSTEM = """你是知识库问答助手。规则：
1. 只根据下面给出的【参考资料】回答，逐条标注引用编号 [1][2]…，编号对应资料序号。
2. 每个事实性断言后都要紧跟它的 [编号]，不要整段只挂一个。
3. 如果【参考资料】不足以回答，直接输出「文档中没有相关信息」，绝不用你的常识补充。
4. 不要编造资料里不存在的编号。"""

def build_prompt(question: str, hits: list[dict]) -> str:
    refs = "\n\n".join(f"[{i+1}] {h['text']}" for i, h in enumerate(hits))
    return f"【参考资料】\n{refs}\n\n【问题】{question}\n\n请按规则回答。"
```

## 6. 引用解析与回链

模型返回的 `[2]` 要能点回原文。生成后解析引用编号，映射到 chunk 与来源：

```python
import re

def parse_citations(answer: str, hits: list[dict]) -> list[dict]:
    """提取答案里的 [n]，映射回对应 chunk，生成可点击的回链。"""
    cited = []
    for n in sorted({int(x) for x in re.findall(r"\[(\d+)\]", answer)}):
        if 1 <= n <= len(hits):
            h = hits[n-1]
            cited.append({"cite": n, "chunk_id": h["id"],
                          "doc": h["doc"], "snippet": h["text"][:60]})
    return cited

def answer(question: str) -> tuple[str, list[dict]]:
    hits = retrieve(question)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": build_prompt(question, hits)}],
        temperature=0, max_completion_tokens=2048,
    )
    text = resp.choices[0].message.content
    return text, parse_citations(text, hits)
```

前端把 `parse_citations` 返回的 `chunk_id` 渲染成锚点，就能做到「每个断言点回原文」。

## 7. 逐步加料：混合检索、重排、拒答

最小闭环跑通后，按 C24-2 的设计一项项加：

**加 BM25 混合检索 + RRF 合并：**

```python
from rank_bm25 import BM25Okapi
import jieba

def build_bm25(corpus: list[str]):
    return BM25Okapi([list(jieba.cut(c)) for c in corpus])

def hybrid_retrieve(query, k=50):
    qv = embed([query])[0]
    vec = collection.query(query_embeddings=[qv], n_results=k)
    bm = bm25.get_scores(list(jieba.cut(query)))
    return rrf_merge(vec, bm)          # RRF 合并，见 C14-3
```

**加 rerank（只重排合并后的 top 50）：**

```python
from sentence_transformers import CrossEncoder
reranker = CrossEncoder("BAAI/bge-reranker-base")   # 交叉编码器

def rerank(query, candidates, top_k=6):
    scores = reranker.predict([(query, c["text"]) for c in candidates])
    ranked = sorted(zip(candidates, scores), key=lambda x: -x[1])
    return [(c, s) for c, s in ranked[:top_k]]
```

**加拒答兜底（rerank 最高分低于阈值直接拒答）：**

```python
REFUSAL_THRESHOLD = 0.3   # 用评测集校准，见 C24-4

def answer(question):
    ranked = rerank(question, hybrid_retrieve(question))
    if not ranked or ranked[0][1] < REFUSAL_THRESHOLD:
        return "文档中没有相关信息。", []
    hits = [c for c, _ in ranked]
    ...  # 生成 + parse_citations，同上
```

## 8. 小结

- 先跑通「切分 → embedding → 检索 → 生成」最小闭环，再加混合/重排/拒答，每加一项跑评测。
- 引用 id 在 `index_documents` 里就埋好（`doc_id:chunk_index`），生成时编号、返回后解析回链。
- 生成 prompt 是「可溯源」的落点：逐断言编号、无据则拒、不许编造编号。
- 拒答兜底用 rerank 最高分阈值，阈值用评测集校准，不拍脑袋。

## 下一篇

C24-4 给这条链路装尺子：50 条评测集怎么构造标注、可溯源率与拒答准确率怎么自动算、至少 3 个失败案例分析，以及成本结构拆解。
