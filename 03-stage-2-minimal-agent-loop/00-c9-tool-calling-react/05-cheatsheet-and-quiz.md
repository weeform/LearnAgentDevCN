# C9-5 · 工具调用与 ReAct 速查表与自测
> 阅读约 10 分钟。这一篇把 C9 压成能查、能自测的东西。

## 1. 一轮工具往返速查

```
messages 变化：
  system, user
→ + assistant(tool_calls)      # 模型表达调用意图
→ 执行工具（你的代码）
→ + tool(tool_call_id, result) # 结果回填，id 必须对上
→ 再次请求
```

- `tool` 消息是**你的代码**塞进去的，别漏。
- 并行调用：按 `tool_call_id` 一一对应；流式 `arguments` 按 index 累加再 `json.loads`。

## 2. ReAct 三段式

`Thought（想）→ Action（做）→ Observation（看）→ 再想`

- 原生 `tool_calls` 是生产首选；纯文本 ReAct 脆弱，只用于教学。
- 显式 Thought 按需加，别为简单任务付 token。

## 3. 终止条件速查

| 信号 | 动作 |
|---|---|
| `finish_reason=stop` | 返回最终答案 |
| `finish_reason=tool_calls` | 执行 + 继续 |
| `finish_reason=length` | 报错，不硬解析 |
| 步数上限 | 强制停 + 报未完成 + 附 trace |
| 连续失败 N 次 | 主动终止 + 降级 |

## 4. 自测（7 道）

> 答对 5 道以上，本课通过。

1. 一轮工具调用的消息数组要经历哪几步？哪条消息是「你的代码」塞进去的？
2. 并行返回两个工具调用时，回填结果靠什么保证不串？
3. 为什么生产里优先用原生 `tool_calls` 而不是纯文本 ReAct？
4. ReAct 三段式里，Observation 的作用是什么？为什么它决定循环质量？
5. `finish_reason=length` 时为什么不能把 `msg.content` 当最终答案？
6. 最大步数设成「很大」会有什么问题？到了上限该怎么做？
7. 为什么 Agent 循环要用 `temperature=0` 这一档采样？

### 答案要点

1. system/user → assistant(tool_calls) → 执行 → tool(result) → 再请求；`tool` 消息是代码塞的。
2. `tool_call_id` 与结果一一对应，数量一致。
3. 原生 tool_calls 稳定、各家支持一致；纯文本 ReAct 靠正则解析，格式漂移、解析出错是常态。
4. 它是模型「看世界」的唯一窗口，反馈真实环境结果；含糊/超长/报错不清会带偏下一步。
5. 输出被截断，content 是残缺的，返回会污染下游。
6. 白烧钱、浪费步数预算；到上限应明确报「未完成」并附已执行步骤，不要假装成功。
7. 追求可复现，采样走稳定档（见 C1-2），避免循环路径每次漂移。

## 5. 下一篇

C9 结课。下一门 C10 讲「工具设计」：粒度、命名、描述、参数校验——因为工具描述质量直接决定模型调用成功率。
