# C4-2 · 工具调用的流式拼接
> 阅读约 12 分钟。这是整个阶段 0 最容易出 bug 的一节，也是区分"调过 API"和"写过 Agent 框架"的分水岭。

## 1. 难点在哪

文本内容流式过来，你只要 `+=` 就行。工具调用不一样：

```
第1片: {"tool_calls":[{"index":0,"id":"call_abc","function":{"name":"search","arguments":""}}]}
第2片: {"tool_calls":[{"index":0,"function":{"arguments":"{\"qu"}}]}
第3片: {"tool_calls":[{"index":0,"function":{"arguments":"ery\":\"kv"}}]}
第4片: {"tool_calls":[{"index":0,"function":{"arguments":" cache\"}"}}]}
```

关键特征：

1. `id` 和 `function.name`**只在第一片出现**，后面全是 `null`；
2. `function.arguments` 是**字符串的分片**，单独一片几乎必然不是合法 JSON；
3. 并行调用时会有**多个 index**，交错到达；
4. 结束信号是 `finish_reason == "tool_calls"`，**不是**流结束。

## 2. 正确的累加算法

核心数据结构：用**index 做 key 的字典**，每个条目维护 `id` / `name` / `arguments_buffer`。

```python
def collect_tool_calls(chunks):
    calls = {}                      # index -> {id, name, args}
    for ch in chunks:
        delta = ch["choices"][0]["delta"]
        for tc in delta.get("tool_calls") or []:
            i = tc.get("index", 0)
            slot = calls.setdefault(i, {"id": None, "name": None, "args": ""})
            if tc.get("id"):
                slot["id"] = tc["id"]                       # 只有首片有
            fn = tc.get("function") or {}
            if fn.get("name"):
                slot["name"] = fn["name"]                   # 只有首片有
            if fn.get("arguments"):
                slot["args"] += fn["arguments"]             # 关键：字符串累加
        if ch["choices"][0].get("finish_reason") == "tool_calls":
            break

    out = []
    for i in sorted(calls):
        s = calls[i]
        out.append({
            "id": s["id"],
            "name": s["name"],
            "arguments": json.loads(s["args"]),   # 到这里才是完整 JSON
        })
    return out
```

四个必须做对的点：

- **按 index 分槽**，不能用单个变量（并行调用会串味）；
- **累加 arguments 字符串**，不要对单片做 `json.loads`；
- **只在 `finish_reason` 出现后才解析**；
- 最后 `sorted(calls)` 保证顺序稳定（便于日志比对与回归测试）。

## 3. Anthropic 的对应写法

Anthropic 结构不同但思路一致：

- `content_block_start` 带 `type: "tool_use"`、`id`、`name` —— 相当于"首片"；
- 后续 `content_block_delta` 的 `partial_json`（`input_json_delta`）是**参数分片**，需要累加；
- `content_block_stop` 表示该工具块结束，此时才能 `json.loads`；
- 一个消息里可以有多个 tool_use 块，**各自累加，互不干扰**。

一句话总结：**无论哪家，"拼接 + 延迟解析"的套路是通用的。**

## 4. 五个经典 bug（附症状）

| bug | 症状 | 修法 |
|---|---|---|
| 对单片 arguments 做 `json.loads` | 几乎每次都抛 `JSONDecodeError` | 累加后再解析 |
| 用单个变量存 name/args | 并行调用时参数互相污染 | 按 index 分槽 |
| 用 `delta.content` 判断有没有工具调用 | 工具调用时 content 为 `None`，代码走进空分支 | 判断 `delta.tool_calls` |
| 不等 `finish_reason` 就执行工具 | 参数不完整，执行报错 | 等 `finish_reason == "tool_calls"` |
| 忽略 `id` | 回传工具结果时无法对应，多工具场景错乱 | 保存 id，回传时原样带上 |

最后一条要特别提醒：**工具结果回传时必须带上对应的 `tool_call_id`**：

```python
messages.append({
    "role": "tool",
    "tool_call_id": call["id"],     # 必须与请求时一致
    "content": json.dumps(result, ensure_ascii=False),
})
```

少了它或写错，API 会直接报 400。

## 5. 可复用的设计：流式收集器

建议在你的调用层里封装一个纯函数：

```
feed(chunk) -> None          # 喂进一个 chunk，内部累加
result() -> (text, calls)    # 流结束后一次性取出文本与工具调用列表
```

好处：

- **可单元测试**：喂一组录制的 chunk，断言输出，不依赖网络；
- **可跨家复用**：OpenAI / Anthropic / DeepSeek 只是 `feed` 的解析分支不同；
- 与业务解耦：上层只关心"这一步模型说了什么、要调哪些工具"。

## 6. 一个真实世界的坑：`arguments` 可能是空串

有些模型在决定调用工具时，会先发一个 `arguments: ""` 的空片，然后才开始吐内容；极少数情况下（无参数工具）**整个 arguments 都是空字符串**。所以解析时要：

```python
args = json.loads(s["args"]) if s["args"].strip() else {}
```

否则 `json.loads("")` 会抛异常，而这个问题往往在上线几天后才被一个"无参数工具"触发。

## 7. 小结

- 工具调用的 `arguments` 是**增量字符串**，必须累加后解析。
- 按 `index` 分槽，支持并行调用。
- `id` / `name` 只在首片出现；`finish_reason == "tool_calls"` 才是结束信号。
- 回传结果必须带 `tool_call_id`。
- 封装成"喂食式"收集器，方便测试与跨家复用。

## 下一篇

工具调用是"模型按你的 schema 输出"的一种形式。更广义的问题是：怎么让模型**稳定输出任意结构**——C4-3 讲 JSON Schema 与 strict 模式。
