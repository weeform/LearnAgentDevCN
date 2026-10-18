# C3-2 · 怎么数 token：工具、误差与估算公式
> 阅读约 10 分钟。目标：建立一套「离线估算 + 线上校准」的双轨做法，把 token 估算误差压到 10% 以内。

## 1. 三种数法，各有各的用处

| 方法 | 精度 | 代价 | 适合场景 |
|---|---|---|---|
| 官方库离线数（tiktoken 等） | 对自家模型**精确** | 免费、本地、毫秒级 | 上线前估 prompt、做截断、算预算 |
| 计数接口（Anthropic `count_tokens`） | 精确 | 一次 HTTP 请求 | 提交前校验、跨模型对比 |
| **响应的 `usage` 字段** | **唯一真实值** | 只能事后拿到 | 计费对账、成本监控、校准估算公式 |

结论先给：**估算用库，对账用 usage，别用字符数除以 4 当真值。**

## 2. OpenAI：tiktoken

```python
import tiktoken

enc = tiktoken.get_encoding("o200k_base")      # GPT-4o / GPT-5 系列共用
# 或：enc = tiktoken.encoding_for_model("gpt-5")

n = len(enc.encode("把这段中文数一数"))
print(n)

# 安全的 token 级截断（对应 C3-1 坑 5）
def truncate(text, max_tokens):
    ids = enc.encode(text)
    return enc.decode(ids[:max_tokens])
```

要点：

- `encode` 返回 id 列表，`decode` 能还原——**截断一定要走这条路**，不要按字符切。
- `encoding_for_model` 对未知模型会报错或回落，生产环境建议**显式指定 encoding 名**。
- tiktoken 数的是**纯文本**，不含消息结构的额外开销（见第 4 节）。

## 3. Anthropic：count_tokens 端点

```python
resp = client.messages.count_tokens(
    model="claude-sonnet-5",
    messages=[{"role": "user", "content": "..."}],
    tools=[...],           # 工具定义也一起算
)
print(resp.input_tokens)
```

优点：官方口径、**连 tools/system 一起算**，和实际计费一致，且免费。  
代价：多一次网络往返，不适合热路径；适合**提交前校验**和**跨模型对比**（比如验证"换新分词器后多了多少 token"这个猜想）。

## 4. 别忽略「结构开销」

你数的是文本，API 数的是**整个请求序列化后的结果**。多出来的部分包括：

- 每条消息的 role 与分隔符：每条约**+3～7 token**；
- `system` 消息同样计入；
- **工具定义**（JSON Schema 序列化后）：每个工具几十到几百 token；
- 多模态内容（图片）按另一套规则折算。

所以估算公式一般长这样：

```
prompt_tokens ≈ sum(text_tokens) + 4 × 消息条数 + tools_tokens
```

一个 20 条消息、带 8 个工具的对话，结构开销可能就有**300～800 token**——相对总量不大，但当你做精细预算（比如卡在缓存门槛附近）时它会导致误判。

> 顺带记住：OpenAI 的缓存门槛是**1024 token 起**，命中按 128 token 递增（C2-5 已讲）。如果你的稳定前缀估算出来是"大概 1000 token"，那它很可能**不命中**——这种临界场景必须用 usage 的实际值来确认。

## 5. 估算公式（没有库的时候用）

| 内容 | 经验系数 | 误差范围 |
|---|---|---|
| 英文 | 字符数 ÷ 4 | ±10% |
| 中文 | 字符数 × 0.6～1.0 | 波动较大，±30% |
| 代码 | 字符数 ÷ 3.5 | ±15% |
| JSON（minified） | 字符数 ÷ 3 | ±15% |

中文误差大的原因就是 C3-1 坑 1：常用词合并、生僻字碎片化，差异能到两倍。

**所以正确姿势是**：用公式做**粗筛**（"这个 prompt 大概 2K 还是 20K？"），用库做**精算**，用 usage 做**对账**。

## 6. 落地：把 token 数变成可观测指标

建议在你的调用层里固定记录这几个字段（对应阶段 5 的可观测性，现在先埋点）：

```
request_id, model,
prompt_tokens, cached_tokens, completion_tokens,
tools_count, messages_count,
latency_ms, finish_reason
```

有了这些，你能回答三个关键问题：

1. 稳定前缀到底多大？→ 决定能不能吃到缓存（C2-5）；
2. 每一步的输入增长速率是多少？→ 决定 Agent 的成本曲线（C3-3）；
3. 哪个工具最费 token？→ 决定先优化谁。

## 7. 小结

- 数 token 三件套：**tiktoken / count_tokens / usage**，最后一个才是真值。
- 记得加上**结构开销**（消息 + tools），别只数正文。
- 截断必须在**token 层面**做。
- 换模型要**重量一次**。

## 下一篇

会数 token 之后，就能算钱了。C3-3 讲成本结构，以及 Agent 循环里那个让人心疼的 O(n²)。
