# C4-1 · 流式输出：SSE 协议与增量解析
> 阅读约 12 分钟。看完你应该能手写一个不依赖 SDK 的流式读取。

## 1. Agent 也要流式吗？分两种场景

| 场景 | 要不要流式 | 原因 |
|---|---|---|
| **最终回答**给用户看 | 要 | 首 token 延迟（TTFT）决定体验，30 秒空白不可接受 |
| **中间步骤**（思考/工具调用） | 通常不要 | 反正要等完整参数才能执行；流式只是增加复杂度 |

一个常见设计：**中间步关闭流式，最终回答开启流式**。这样既降低复杂度，又保证用户体验。

顺带一个工程收益：流式能**规避长请求的读超时**——只要数据在持续到达，连接就是活的。

## 2. SSE：流式用的协议

大模型 API 的流式基本都基于**SSE（Server-Sent Events）**：

```
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
```

数据帧长这样：

```
data: {"choices":[{"delta":{"content":"你"},"index":0}]}

data: {"choices":[{"delta":{"content":"好"},"index":0}]}

data: [DONE]
```

三个规则：

1. 每个事件以 `data: ` 开头；
2. 事件之间用**空行**（`\n\n`）分隔——不是换行，是空行；
3. 流结束的标志是 `data: [DONE]`（OpenAI 系），**必须显式检测它**。

以 `:` 开头的行是**注释/心跳**（如 `: ping`），解析时应当忽略而不是报错。

## 3. chunk 里到底有什么（OpenAI 系）

```json
{
  "id": "chatcmpl-xxx",
  "choices": [
    {
      "index": 0,
      "delta": { "content": "你好" },
      "finish_reason": null
    }
  ]
}
```

要点：

- 文本在 `choices[0].delta.content`，每次一小片（可能只有一个字，甚至半个字）；
- `finish_reason` 只在**最后一个 chunk**有值（`stop` / `length` / `tool_calls` / `content_filter`）；
- **默认拿不到 `usage`**。要传 `stream_options: {"include_usage": true}`，服务端会在 `[DONE]` 之前额外发一个带 `usage` 的 chunk。做成本核算时别漏了这一点（否则你的成本统计全是 0）。

## 4. Anthropic 的事件流

Anthropic 的粒度更细，是**具名事件**：

| 事件 | 含义 |
|---|---|
| `message_start` | 消息开始，含 `usage.input_tokens` |
| `content_block_start` | 内容块开始（文本块或工具块，带 `name`） |
| `content_block_delta` | 增量：`text_delta`（文本）或 `input_json_delta`（工具参数） |
| `content_block_stop` | 当前块结束 |
| `message_delta` | 含 `stop_reason` 与 `usage.output_tokens` |
| `message_stop` | 流结束 |

好处是**打字更自然**（整块边界清晰），坏处是解析代码要处理更多事件类型。工具参数在 `input_json_delta` 里同样是**字符串分片**，需要累加（C4-2 详述）。

## 5. 心跳、缓冲与代理

生产环境两个坑：

1. **反向代理缓冲**：Nginx 等默认会缓冲响应，导致流式变成"一次性吐出"。解决：设置 `X-Accel-Buffering: no`，或让代理支持流式。
2. **空闲超时**：模型思考期间可能几十秒没有数据，中间设备（负载均衡、CDN）可能掐断连接。服务端会发心跳注释行保活；你自己也该设置合理的**读超时**（不是总超时）。

## 6. 断流：最麻烦的情况

流进行中网络断了，你已经收到了前 800 个字。这时：

- **无法续传**——API 没有"从第 800 字继续"的能力；
- 简单重试会**重新生成一遍**（内容可能不同，且重新花钱）；
- 因此：**先把已收到内容存下来**，让用户看到部分结果，把重试作为可选动作，而不是默认动作。

对 Agent 来说更稳的做法是：中间步骤不流式（要么成功要么失败，语义清晰），只有最终回答流式且允许"部分展示 + 手动重试"。

## 7. 一个最小可用骨架（Python）

```python
import json, httpx

def stream_chat(payload, headers):
    buf = ""
    with httpx.stream("POST", URL, json=payload, headers=headers, timeout=None) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if not line:
                continue
            if line.startswith(":"):          # 心跳/注释
                continue
            if not line.startswith("data:"):
                continue
            data = line[len("data:"):].strip()
            if data == "[DONE]":
                break
            chunk = json.loads(data)
            delta = chunk["choices"][0]["delta"]
            if "content" in delta and delta["content"]:
                yield ("text", delta["content"])
            fr = chunk["choices"][0].get("finish_reason")
            if fr:
                yield ("finish", fr)
```

注意几个细节：

- `iter_lines()` 已经按行切分，但你仍要处理**空行分隔**的语义；
- `delta` 可能**完全为空**（比如 role 消息），要做防御；
- 超时设成 `None` 或足够大，别用默认的短超时；
- 每个 chunk 都可能是半个 UTF-8 字符吗？——不会，SSE 层已是完整行，但**一个汉字可能被拆成多个 chunk**，拼接即可，不要按 chunk 做语义处理。

## 8. 小结

- SSE：`data:` 开头、空行分隔、`[DONE]` 结束，`:` 开头是心跳。
- 文本在 `delta.content`，`finish_reason` 只在最后一帧，`usage` 要显式 `include_usage`。
- 代理缓冲和空闲超时是生产环境两大杀手。
- 断流**无法续传**，设计上要让部分结果可用。

## 下一篇

文本拼接很简单，难的是工具调用——因为参数是一段**增量字符串**。C4-2 专门讲它。
