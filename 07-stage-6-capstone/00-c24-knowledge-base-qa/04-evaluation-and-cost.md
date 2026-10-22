# C24-4 · 评测与成本数据
> 阅读约 12 分钟，建议在电脑前边读边做。目标：给 C24-3 的链路装上尺子——评测集怎么造、可溯源率与拒答准确率怎么自动算、失败案例怎么看、成本怎么拆。

## 1. 评测集构造与标注

沿用 C24-1 第 4 节的口径，落盘成 JSONL，每条三样：

```json
{"id": 1, "type": "answerable", "question": "退款周期是几天？",
 "gold_answer": "7 天", "gold_chunk_id": "faq:12"}
{"id": 41, "type": "refuse", "question": "CEO 的星座是什么？",
 "gold_answer": "文档中没有相关信息"}
```

- `answerable`（40 条）：必须有 `gold_chunk_id`，指向唯一支撑它的 chunk——这是算召回率的 ground truth。
- `refuse`（10 条）：`gold_answer` 固定为拒答标记。

> 造题最省力的办法：**边读文档边造**，读到一句能出题的事实就记一条。反过来「做完系统再憋题」既慢又容易偏。

## 2. 可溯源率怎么自动算

「可溯源」有两条能自动判：**逐断言覆盖**和**引用正确**（见 C24-1 第 2 节）。人工逐条看 50 条太慢，用 LLM-as-judge 自动打分（方法见 C20）：

```python
JUDGE_PROMPT = """你是评判员。判断下面答案里的每个事实性断言，是否都被其引用的编号正确支撑。
- 断言有引用且引用原文确实支撑 → 可溯源
- 有断言没引用、或引用指向的原文不支撑该断言 → 不可溯源
只回答「可溯源」或「不可溯源」，并给一句理由。"""

def judge_traceable(question, answer, cited_chunks) -> bool:
    # cited_chunks: 把 parse_citations 的 [n] 换成对应原文拼给 judge
    resp = client.chat.completions.create(
        model="gpt-4o-mini", temperature=0,
        messages=[{"role": "user", "content": JUDGE_PROMPT +
                  f"\n问题:{question}\n答案:{answer}\n引用原文:{cited_chunks}"}],
    )
    return "可溯源" in resp.choices[0].message.content
```

> 为什么引用正确性必须 judge，不能只靠正则数 `[n]`：模型完全可能「挂了编号但指错地方」。正则只能证明「有引用」，judge 才能证明「引用对」。

**可溯源率 = 可溯源通过条数 / 40**，目标 ≥95%。

## 3. 拒答准确率怎么算

拒答不用 judge，纯规则就能判（见 C24-1 第 5 节两个数）：

```python
def eval_refusal(results):
    refuse_hits = sum(1 for r in results if r["type"] == "refuse"
                      and "没有相关信息" in r["answer"])    # 拒答召回
    false_refuse = sum(1 for r in results if r["type"] == "answerable"
                       and "没有相关信息" in r["answer"])   # 误拒
    return refuse_hits / 10, false_refuse / 40
```

> 把拒答召回率和误拒率分开报。该拒没拒（编造）的危害远大于误拒，看数字时优先盯召回率，宁可误拒略高也别放编造过关。

## 4. 至少 3 个失败案例分析

跑完评测，挑最典型的 3 个失败，每个回答三问：**现象是什么、根因在哪一环、怎么修**。示例：

| 案例 | 现象 | 根因 | 修复 |
|---|---|---|---|
| 1 | 问「快充技巧」召回一堆无关段落 | 纯向量检索漏掉「快充」关键词 | 上 BM25 混合检索，RRF 合并 |
| 2 | 答对但引用指错 chunk | 切分把「退款 7 天」劈进两个相邻块 | 加大重叠，或按语义边界重切 |
| 3 | 该拒答却编了一段 | rerank 最高分 0.2 仍进生成 | 阈值提到 0.3，低于直接拒答 |

> 失败案例不是扣分项，是作品集里最值钱的部分——它证明你「知道为什么失败、怎么修」，比一句「效果很好」可信得多。

## 5. 成本结构拆解

单次问答的钱花在四环，量级如下（以一次取 6 个 chunk、生成 200 token 为例）：

| 环节 | 单价量级 | 说明 |
|---|---|---|
| query embedding | 极低 | 一次调用，1 个查询向量 |
| 检索（向量+BM25） | 几乎免费 | 本地计算 |
| rerank | 中 | 交叉编码器过 top 50，比生成便宜但按条计 |
| 生成 | **占大头** | 输入含 6 个 chunk + 输出，token 最多 |

> 结论：**在线成本基本由「生成」决定，而生成成本由「塞进去多少 chunk」决定**。所以省钱的杠杆不在检索，在「少塞、塞准」。

三个可落地的优化：

1. **缓存**：相同/相似问题直接返回缓存答案，命中率高的场景能砍掉大部分生成成本。
2. **重排只对 top-k**：rerank 只过 top 50，绝不碰全库（C14-4 的原则），这步已省一大截。
3. **减少 chunk 数**：从 top 10 砍到 top 5，看可溯源率掉不掉——不掉就省一半生成输入成本。

## 6. 小结

- 评测集 JSONL 落盘，`answerable` 带 `gold_chunk_id`，`refuse` 固定拒答标记。
- 可溯源率用 LLM-as-judge 判「断言是否被引用正确支撑」（C20 方法），正则只能证「有引用」。
- 拒答拆「召回率」「误拒率」两个数，优先盯召回率。
- 成本大头在生成，省钱的杠杆是「少塞、塞准」：缓存、rerank 只过 top-k、减 chunk 数。

## 下一篇

C24-5 收尾：把三个关键取舍讲清楚（混合检索、切分粒度、拒答阈值），并把它写进作品集——README、评测截图、成本表怎么摆。
