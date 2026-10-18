# C9-1 · 工具调用协议细节：消息数组怎么拼
> 阅读约 12 分钟。目标：把「一次带工具调用的完整往返」在消息数组层面彻底吃透。参数含义在 C1-4 讲过，这里只讲工程细节。

## 1. 一轮工具调用的完整生命周期

回顾 C1-4 的结论：模型不会「调用」任何东西，它只是**生成一段结构化的 `tool_calls` 文本**，真正执行的是你的代码。一轮往返在消息数组上的变化如下：

```
① 请求前：messages = [system, user]
② 模型返回：assistant 消息（含 tool_calls）
③ 追加 assistant 消息到 messages
④ 你的代码执行工具，得到结果
⑤ 追加 tool 消息（含 tool_call_id + 结果）
⑥ 再次请求（此时 messages 已含 ①②③④⑤）
```

关键点：**第 6 步的请求，messages 必须完整包含 assistant 的 tool_calls 和对应的 tool 结果**，否则服务端会报错（工具调用的「问题」和「答案」必须成对出现）。

## 2. 四种消息的角色分工

| role | 谁产生 | 内容 | 作用 |
|---|---|---|---|
| `system` | 你 | 固定指令 | 任务背景、约束 |
| `user` | 用户 / 你 | 输入、工具结果 | 需求、执行反馈 |
| `assistant` | 模型 | 文本 / tool_calls | 模型的回复或调用意图 |
| `tool` | 你的代码 | 执行结果 | 告诉模型「工具跑完返回了什么」 |

注意：`tool` 消息不是模型发的，是**你的代码在执行完工具后塞进去的**。很多人第一次写会漏掉这一步，导致下一轮模型「看不到工具结果」。

## 3. tool_call_id 是回填的钥匙

一次请求里，模型可能**并行**返回多个工具调用（见 C1-4 的 `parallel_tool_calls`）。每个调用都有一个唯一的 `tool_call_id`。回填时**必须让每个 tool 结果的 id 和对应的 tool_call id 严格对上**：

```python
# 模型返回了两个调用
#   call_1: id="call_abc", name="get_weather", args={"city":"北京"}
#   call_2: id="call_def", name="get_weather", args={"city":"上海"}

# 回填时
messages.append(assistant_msg)                      # 含两个 tool_calls
for call in assistant_msg.tool_calls:
    result = execute(call.function.name,
                     json.loads(call.function.arguments))
    messages.append({
        "role": "tool",
        "tool_call_id": call.id,    # ← id 必须一一对应
        "content": json.dumps(result, ensure_ascii=False),
    })
```

顺序可以乱（并行执行的完成顺序不定），但 **id 对上、数量一致** 是硬性要求。

## 4. arguments 是字符串，要累加后再解析

流式场景下（见 C4-2），`tool_calls` 的 `arguments` 是**分片送达**的，必须按 `index` 分槽累加，等 `finish_reason == "tool_calls"` 后再 `json.loads`。这里用**非流式**简化讲解，但生产里这个坑极其常见，务必记住。

## 5. 一条易错点：把工具结果塞进 user 还是 tool

OpenAI 系用 `role=tool` + `tool_call_id`；Anthropic 的 Claude 用 **user 消息里的 `tool_result` content block**（不是独立的 tool role）。跨家时要按各家协议来，不能混用（见 C1-4 的跨家对比表）。

## 6. 小结

- 一轮往返 = assistant(tool_calls) → 执行 → tool(结果) 成对出现。
- `tool` 消息是你的代码塞进去的，别漏。
- 并行调用靠 `tool_call_id` 一一对应；流式 `arguments` 要按 index 累加再解析。

## 下一篇

C9-2 讲 ReAct 的 Thought / Action / Observation 三段式：为什么「让模型先把想法说出来」能显著提升多步任务的正确率。
