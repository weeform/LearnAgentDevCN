# C1-3 · 输入、长度与停止：messages / max_tokens / stop / stream

> 阅读约 16 分钟。目标：掌握 messages 的无状态前提，以及长度、停止、流式四组参数。

## 1. messages：无状态是理解一切的前提

API 不保存任何会话。你每次请求都必须把**完整历史**发过去。服务端只做一次「续写」，然后就忘了。

```python
messages = [
    {"role": "system",    "content": "..."},
    {"role": "user",      "content": "..."},
    {"role": "assistant", "content": "..."},   # 普通回复
    {"role": "assistant", "content": None, "tool_calls": [...]},  # 或：发起工具调用
    {"role": "tool",      "tool_call_id": "call_abc", "content": "..."},  # 工具结果
    {"role": "user",      "content": "..."},
]
```

四种角色：

| role | 含义 | 注意 |
|---|---|---|
| `system` | 全局指令、人设、约束、输出格式 | 放在最前；每轮都重发，成本固定 |
| `user` | 用户输入 |  |
| `assistant` | 模型的回复，或它发起的工具调用 | 可以**伪造**，用来引导后续生成 |
| `tool` | 工具执行结果 | 必须带 `tool_call_id`，与调用一一对应 |

Claude 的差异：system 是**顶层独立字段**，`system="..."`，而不是 messages 里的一项（新版本也支持在对话中途插入 system 消息）。

### 无状态带来的三个直接后果

1. **成本随轮次线性增长**。第 10 轮的输入 token = 前 9 轮全部内容。这是 Agent 变贵的首要原因。
2. **上下文管理是 Agent 的核心工程问题**，不是边缘优化。裁剪、压缩、摘要、缓存都要围绕它设计。
3. **会话状态保存在你的程序里**，不在模型里。断点续跑、多轮持久化都要自己做。

## 2. max_tokens / max_completion_tokens

- `max_tokens`：旧字段，限制输出 token 数。
- `max_completion_tokens`：新字段，**包含推理 token**。OpenAI 已推荐用它替代 `max_tokens`，o-series 模型只认这个。

设太小的后果：输出被**硬截断**，JSON 截一半、`finish_reason="length"`、解析直接失败。这是 Agent 最常见的低级 bug 来源之一，而且很容易被误判成「prompt 写得不好」。

设太大的后果：基本没坏处，只是给「模型跑飞了」留更大空间，最多烧钱。

**实践建议**：

- 工具调用类请求：给足 1024-4096，保证 JSON 能写完。
- 最终回答类请求：按期望长度的 2 倍设。
- 永远不要在这一点上省钱——一次截断导致的重试，比多留 token 贵得多。

## 3. stop：让模型在该停的地方停

`stop` 接收最多 4 个字符串，模型一旦生成其中任意一个就立即停止，**且不包含该字符串本身**。

三个典型用法：

1. **防止模型自说自话**。Agent 里一个经典 bug：模型没有真的发起工具调用，而是把「工具调用的样子」当成普通文本写出来，甚至自己编造工具返回结果。用 `stop=["\nObservation:", "User:"]` 之类的序列能挡住一部分。
2. **截断多余输出**。只要第一个 JSON 对象时可以用类似 `stop=["}\n"]` 的技巧（需谨慎，JSON 有嵌套）。
3. **多轮对话模板对齐**。一些开源模型用固定模板，需要 stop 来切分轮次。

**注意**：如果用了官方 `tools` 参数做工具调用，通常不需要 stop 来管这件事——模型生成完整 tool_call 后会自然停止。

## 4. finish_reason：Agent 循环的方向盘

响应里这个字段决定了你的代码下一步干什么。**Agent 循环本质就是一个基于 finish_reason 的状态机。**

| 值 | 含义 | Agent 该做什么 |
|---|---|---|
| `stop` | 自然结束 | 把内容返回给用户，退出循环 |
| `length` | 撞到 token 上限被截断 | 报错 / 加长 max_completion_tokens / 要求模型继续 |
| `tool_calls` | 模型要求调用工具 | 执行工具，结果以 `role=tool` 追加，继续循环 |
| `content_filter` | 被安全策略拦截 | 记录日志，给用户兜底回复 |

Claude 对应字段叫 `stop_reason`，取值 `end_turn`、`max_tokens`、`tool_use`、`refusal` 等。

**这是很多教程不强调、但极其关键的一点**：不要只看 `message.content` 是否为空来判断有没有工具调用，要看 `finish_reason`。

## 5. stream：为什么 Agent 也需要流式

设 `stream=True`，服务端用 SSE 逐 token 返回，而不是等全部生成完。

- **对用户体验**：首字延迟从「全部生成完」降到「第一个 token」，几秒 → 零点几秒。
- **对 Agent**：调试时能实时看到模型在干什么；长任务能及时中断。
- **代价**：解析逻辑变复杂（要拼 delta）；开了 stream 默认不返回 usage，需要 `stream_options={"include_usage": true}`。

注意：工具调用的参数在流式下是**增量片段**，必须拼完整后再解析 JSON。

## 6. n：基本不用

生成 n 个候选。注意**按所有候选的总 token 计费**。成本翻倍，Agent 场景几乎用不到。真需要多样性，不如用不同 temperature 调多次，可控性更好。

## 7. usage：成本的唯一真相

```json
"usage": {
  "prompt_tokens": 1200,
  "completion_tokens": 85,
  "total_tokens": 1285,
  "prompt_tokens_details": {"cached_tokens": 900},
  "completion_tokens_details": {"reasoning_tokens": 40}
}
```

- `prompt_tokens` 通常占大头，多轮对话尤其如此。`cached_tokens` 是命中缓存的部分，价格通常低很多——**把稳定不变的内容（system prompt、工具定义）放在前面，可以吃到缓存折扣**。这也是「system prompt 尽量稳定」的经济动机。
- `reasoning_tokens` 单独计费，推理模型的账单里这块可能占比很高。

**Agent 视角**：每次循环都打印 usage，画成折线。Agent 失控的第一征兆就是 token 曲线异常抬升。

## 思考题

> 先自己答，再展开参考思路。这三问不考记忆，考的是你能不能把它用在自己的项目上。

1. 「messages 是无状态的」这条对多轮对话的实现意味着什么？你以为的「上下文」到底存在哪？
2. 被 max_tokens 截断后，为什么不能把 content 当最终答案返回给用户？
3. stop 是「你定的规则」，finish_reason 是「模型的报告」。为什么两者都要看，只看一个会漏什么？

<details>
<summary>参考思路</summary>

1. 上下文完全存在你这边：每次请求都要把历史重新发一遍。所以「省 token」的本质是省你自己重复发送的那部分（见 C3-3 的平方增长）。
2. 截断意味着句子没写完，可能是半句 JSON、半个数字。当答案返回会把残缺数据写进下游，属于最典型的静默污染。
3. stop 命中说明是你要它停的，finish_reason=length 说明是被截断的，tool_calls 说明要执行工具。只看 content 非空就返回，会把这三种情况混成一锅。

</details>

## 8. 下一篇

C1-4 是本课程落点：模型明明只会生成文本，凭什么能「调用工具」？`tools`、`tool_choice`、`response_format` 背后的机制是什么。
