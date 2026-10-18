# C1-1 · 课程导览与参数全景图
> 补充阅读
> ：本篇第 ②③ 步直接用了“分词”“logits”“前向推理”，但没解释模型内部长什么样。如果你不确定 token 和 logits 是什么，建议先读 [C0-1 · 大模型到底在做什么](../00-c0-llm-fundamentals/01-what-llm-actually-does.md) 和 [C0-2 · Token 与向量](../00-c0-llm-fundamentals/02-token-and-vector.md)（合计约 20 分钟）；想拿完整底图再看 [C0-5 · 一次推理的完整流程](../00-c0-llm-fundamentals/05-full-inference-pipeline.md)。不读也能跟上本课，但会少一层“为什么”。

## 1. 先建立一个正确的心智模型

很多人把「调大模型」想象成「问一个问题，得到一个答案」。对 Agent 开发来说这个模型太粗了，会导致后面很多决策做不对。

更准确的模型是：

> 你每次调用，都是在让模型**续写一段文本**。你给的所有输入（system、历史、工具定义）会被拼成一段文本；模型做的事是「预测下一个 token」；你把新生成的 token 拼回去，再预测下一个，直到某个停止条件。

记住三件事：

1. **模型不会「记住」任何东西**。API 是无状态的，你每次都要把完整历史发过去。
2. **模型输出的永远是 token 序列**。所谓「调用工具」，只是它生成了一段符合约定的结构化文本，由你的代码去解析和执行。
3. **模型不会执行代码**。真正执行工具的永远是你的程序，模型只是「说」它想调用什么。

这三条决定了 Agent 的全部架构。

## 2. 一次调用的完整生命周期

```
① 输入组装
   system prompt + 历史消息 + 工具定义(JSON Schema) + 本轮用户输入
        ↓
② 分词（tokenize）
   文本 → token id 序列（中文约 1 字 ≈ 0.6-1 token，英文 1 词 ≈ 1.3 token）
        ↓
③ 前向推理
   token id 序列过一遍模型，在最后一个位置输出一个「词表大小的向量」= logits
        ↓
④ 采样（C1-2 的重点）
   logits →（top_k / top_p 截断）→（temperature 缩放）→ softmax → 概率分布 → 抽一个 token
        ↓
⑤ 拼接与循环
   新 token 拼回序列，回到 ③。这就是「自回归」，
   也是为什么输出按 token 计费、按 token 逐个吐出
        ↓
⑥ 停止
   遇到 stop 序列 / EOS / 达到 max_tokens / 生成了完整的 tool_call → 返回 finish_reason
        ↓
⑦ 你的代码分支
   finish_reason == "tool_calls" → 执行工具 → 结果作为新消息追加 → 回到 ①
   finish_reason == "stop"       → 结束，返回给用户
```

第 ⑦ 步就是 Agent 循环。整条链路里你能控制的东西只有四个：**① 的输入、④ 的采样方式、⑥ 的停止条件、⑦ 的分支逻辑**。本课程就是逐个拆这四项。

## 3. 参数全景图

按「你拿它来干什么」分五类。这就是本课程的地图。

### A. 输入类（决定模型看到什么）

| 参数 | 作用 | 备注 |
|---|---|---|
| `model` | 选哪个模型 | 决定能力、价格、上下文长度、支持哪些参数 |
| `messages` | 对话历史数组 | 无状态，每次全量发送 |
| `system`（Claude 为顶层字段） | 系统指令 | 稳定人设与约束放这里 |
| `tools` | 可用工具的 JSON Schema 列表 | Agent 的核心，见 C1-4 |
| `response_format` | 约束输出格式 | json_object / json_schema |

### B. 采样类（决定模型怎么选下一个 token）

| 参数 | 作用 | 常用值 |
|---|---|---|
| `temperature` | 缩放 logits，控制分布陡峭程度 | Agent 场景 0-0.3 |
| `top_p` | 核采样，只保留累计概率 p 的候选 | 0.8-1.0，与 temperature 二选一 |
| `top_k` | 只保留概率最高的 k 个候选 | OpenAI 官方 API 不支持；vLLM / Claude 支持 |
| `seed` | 尽力而为的确定性 | 需要复现时设置 |
| `frequency_penalty` | 按出现次数惩罚重复 | Agent 场景通常为 0 |
| `presence_penalty` | 按是否出现过惩罚，鼓励新话题 | Agent 场景通常为 0 |

### C. 长度与停止类（决定什么时候停）

| 参数 | 作用 |
|---|---|
| `max_tokens` / `max_completion_tokens` | 输出 token 上限（后者含推理 token，已取代前者） |
| `stop` | 停止序列，最多 4 个 |
| `n` | 生成几个候选（计费按总量，Agent 基本不用） |
| `reasoning_effort` / `thinking` | 推理模型的「思考预算」 |

### D. 工具类（Agent 专属）

| 参数 | 作用 |
|---|---|
| `tool_choice` | 强制 / 禁止 / 指定调用某个工具 |
| `parallel_tool_calls` | 是否允许一轮返回多个工具调用 |

### E. 工程类（不影响输出内容，影响可维护性）

| 参数 | 作用 |
|---|---|
| `stream` | SSE 流式返回 |
| `stream_options` | 流式时是否附带 usage |
| `metadata` / `user` / `safety_identifier` | 打标、滥用检测 |
| `logprobs` / `top_logprobs` | 返回 token 概率，做置信度分析用 |
| `logit_bias` | 强行抬高或压低某些 token 的概率（已不推荐） |

## 4. 一个最小可用请求长什么样

```python
from openai import OpenAI
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "你是助手。需要查数据时必须调用工具，不要编造。"},
        {"role": "user", "content": "北京今天天气怎么样"},
    ],
    tools=[...],          # 见 C1-4
    tool_choice="auto",
    temperature=0,
    max_completion_tokens=1024,
    stream=False,
)

choice = resp.choices[0]
print(choice.finish_reason)   # "tool_calls" 或 "stop"
print(choice.message.tool_calls)   # 模型想调用的工具
print(resp.usage)                  # 本次 token 消耗
```

## 5. 一个重要提醒：参数支持度因模型而异

不要把参数当成「永远存在」。现实情况：

- **推理 / 思考类模型**（如 o-series、GPT-5 系列、Claude Opus 4.7 及以上）不支持 `temperature`、`top_p`、`top_k` 等采样参数，传非默认值会直接报 400。改用 `reasoning_effort`（OpenAI）或 `thinking`（Claude）控制思考强度。
- `max_tokens` 已被 `max_completion_tokens` 取代（后者包含推理 token），旧字段在 o-series 上不兼容。
- `top_k`、`repetition_penalty` 在 OpenAI 官方 Chat Completions API 中被忽略或不支持，但在 vLLM、Claude 等处可用。

**结论：接一个新模型，第一件事是查它支持哪些参数，而不是照抄上一个模型的配置。**

## 6. 下一篇

C1-2 拆解第 ④ 步：logits 是怎么变成那一个 token 的，temperature 和 top_p 到底改了什么。
