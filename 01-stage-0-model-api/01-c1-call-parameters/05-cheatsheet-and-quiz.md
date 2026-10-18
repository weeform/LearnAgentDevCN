# C1-5 · 速查表与自测题
## 1. 一页速查表

### 输入类

| 参数 | 作用 | Agent 建议 |
|---|---|---|
| `model` | 选模型 | 按任务分级：简单抽取用小模型，规划用大模型 |
| `messages` | 全量历史，无状态 | 自己管理长度与裁剪 |
| `system` | 全局指令 | 保持稳定，吃到 prompt 缓存 |
| `tools` | 工具 JSON Schema | 描述质量 >> 参数调优 |
| `response_format` | 约束输出格式 | 需被代码解析时优先 json_schema |

### 采样类

| 参数 | 作用 | Agent 建议 |
|---|---|---|
| `temperature` | softmax 前缩放 logits，T→0 即贪心 | 0（工具调用）/ 0.3-0.7（问答）/ 0.8+（创意） |
| `top_p` | 按累计概率截断候选集，自适应 | 与 temperature 二选一，通常不动 |
| `top_k` | 固定保留前 k 个 | OpenAI 不支持；vLLM / Claude 可用 |
| `seed` | 尽力而为的确定性 | 调试用，生产不依赖 |
| `frequency_penalty` | 按出现次数惩罚重复 | 0 |
| `presence_penalty` | 按是否出现惩罚，鼓励新话题 | 0 |

### 长度与停止

| 参数 | 作用 | Agent 建议 |
|---|---|---|
| `max_completion_tokens` | 输出上限（含推理 token），替代 max_tokens | 给足，1024-4096 |
| `stop` | 最多 4 个停止序列 | 防模型自说自话 / 编造观察结果 |
| `n` | 候选个数 | 1 |
| `reasoning_effort` / `thinking` | 推理模型的思考预算 | 替代 temperature 使用 |

### 工具与工程

| 参数 | 作用 | Agent 建议 |
|---|---|---|
| `tool_choice` | auto / none / required / 指定 | 最后一步设 none；流程约束用指定 |
| `parallel_tool_calls` | 是否允许一轮多调 | 无依赖时开，按 tool_call_id 回填 |
| `stream` | SSE 流式 | 面向用户时开；记得 include_usage |
| `logprobs` | 返回 token 概率 | 做置信度或拒答判定时才开 |

### finish_reason 分派

| 值 | 动作 |
|---|---|
| `stop` | 返回用户，退出 |
| `length` | 增大 max_completion_tokens 或报错 |
| `tool_calls` | 执行工具 → 回填 → 继续循环 |
| `content_filter` | 兜底回复 + 记录 |

## 2. 自测题（先自己答，再看答案）

1. API 是无状态的，这意味着什么？举两个由此产生的工程问题。
2. `temperature=0` 时输出一定完全确定吗？为什么？
3. temperature 和 top_p 分别改变了计算过程中的哪一步？
4. `top_p=0.1` 一定比 `top_p=0.9` 更确定吗？为什么？
5. 为什么说「模型不会调用工具」？真正调用工具的是谁？
6. 模型的输出要被你的代码直接 JSON 解析，优先用什么参数？它凭什么能保证格式合法？
7. `max_tokens` 设太小，Agent 会出现什么现象？代码里怎么检测到？
8. Agent 循环应依据哪个字段判断「要不要执行工具」？为什么不能只看 content 是否为空？
9. 想让模型在最后一步输出自然语言总结、不再调工具，怎么设参数？
10. 在推理类模型（如 o-series、Claude Opus 4.7 及以上）上调 temperature 会怎样？应该改用什么？
11. 为什么 system prompt 要保持稳定？除了效果还有哪方面收益？
12. 一轮里模型返回了 3 个工具调用，你的代码要注意什么？

### 答案要点

1. 每次请求都要重发完整历史。工程问题：成本随轮次增长；会话状态要自己持久化；上下文需要裁剪与压缩。
2. 不一定。多数实现里 T=0 等价于贪心解码，但浮点并行归约顺序、后端版本变化都可能造成偶发差异。
3. temperature 在 softmax 之前对 logits 做除法缩放；top_p 在采样前按累计概率截断候选集。
4. 不一定。top_p 只在模型不确定时才起作用；模型高度确定时（某 token 概率 0.95），top_p 从 1.0 降到 0.1 可能毫无变化。
5. 模型只是生成了一段符合约定的结构化文本（tool_calls）；真正执行函数的是你的代码，再把结果回填给模型。
6. 优先 `response_format: {"type": "json_schema", ...}`。它靠约束解码：根据 Schema 维护状态机，逐 token 把非法 token 的 logits 置为 -inf，只从合法集合采样，因此格式 100% 合法。
7. 输出被硬截断，JSON 不完整、解析失败，`finish_reason == "length"`。检测这个值即可。
8. 依据 `finish_reason`（Claude 是 `stop_reason`）。content 为空可能是其他原因，只有 finish_reason 是权威信号。
9. `tool_choice="none"`（Claude 是 `{"type": "none"}`），或者该轮请求干脆不带 tools。
10. 会直接报 400（这些模型不支持 temperature / top_p / top_k）。改用 `reasoning_effort`（OpenAI）或 `thinking`（Claude）控制思考强度。
11. 稳定前缀能命中 prompt 缓存，`cached_tokens` 单价显著低于普通输入 token，能省不少钱；同时保证行为一致。
12. 按 `tool_call_id` 一一回填，可并发执行但结果必须各自对应；同时确认这些调用之间没有依赖关系。

## 3. 常见坑清单

- 把 `max_tokens` 设得太小，JSON 被截断，然后去调 prompt——其实改一个数字就好。
- 同时调 temperature 和 top_p，效果不可预测，也无法复现。
- 用 content 是否为空判断有无工具调用，漏掉 finish_reason。
- 忘记把 assistant 的 tool_calls 消息追加进 messages，导致下一轮报「tool_call_id 找不到」。
- 工具 description 写得含糊，然后花大量时间调 temperature——方向错了。
- 流式模式下忘了 `stream_options={"include_usage": True}`，拿不到 token 统计。
- 换了模型直接复用旧参数配置，遇到不支持的参数报 400。

## 4. 课程收尾：三条带走

1. **模型只是在续写 token**。所有 Agent 机制都建立在这个事实上。
2. **Agent 的稳定性来自约束，不来自运气**：temperature=0、json_schema、tool_choice、最大步数。
3. **工具描述的质量，比任何参数调优都重要**。

## 5. 下一步

回到 `00 · 学习路径总纲`，进入**阶段 1 · Prompt 与上下文工程**。下一门课会从「system prompt 的结构化写法」开始。
