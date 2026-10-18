# C1-4 · Agent 核心参数：tools / tool_choice / response_format
> 这一篇是整门课的落点，前三篇都是为它做铺垫。

## 1. 先破除幻觉：模型不会「调用」任何东西

真相是三步：

1. 你在请求里声明 `tools=[{...}, {...}]`，每个工具用**JSON Schema**描述名字、用途、参数。
2. 模型判断当前要不要用工具。如果要，它就**生成一段特殊格式的结构化文本**（OpenAI 里是 `tool_calls` 字段，Claude 里是 `tool_use` content block）。
3. **你的代码**读到这个结构，真正去执行函数，把结果塞回 `role=tool` 的消息里，再发一次请求。

模型全程只在「预测下一个 token」，它预测出的是「我现在应该输出一个调用 `search_weather`、参数 `{"city":"北京"}` 的标记」。执行在你这边。

**推论**：工具的能力来自模型对工具**描述**的理解。描述写得烂，模型就不会用、或者乱用。参数调优救不了烂的工具定义——这是 Agent 开发里性价比最高的一条认知。

## 2. 一个完整的工具定义

```python
tools = [{
    "type": "function",
    "function": {
        "name": "search_weather",
        "description": "查询指定城市当前天气。仅支持中国境内地级市。",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名，如「北京」"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"], "description": "温度单位"}
            },
            "required": ["city"]
        }
    }
}]
```

写好工具定义的四条规则：

1. **name 是给模型看的**：动词开头、语义明确、无歧义。`search_weather` 比 `get_data` 好。
2. **description 是唯一的说明书**：写清「能干什么」+「什么时候用」+「边界」（不支持什么）。
3. **每个参数都要有 description**：模型靠它决定填什么值。
4. **用 enum 收窄取值**：能枚举的一律枚举，比在 prompt 里写「只能是 A 或 B」可靠得多。

## 3. tool_choice：把决策权抢回来

| 值 | 行为 | 典型用法 |
|---|---|---|
| `"auto"`（默认） | 模型自己决定要不要调用、调用哪个 | 常规 Agent 循环 |
| `"none"` | 禁止调用任何工具，等价于本次不带工具 | 让模型做最终总结时用 |
| `"required"` | 必须调用至少一个工具 | 强制走一遍流程，比如强制先查库再回答 |
| `{"type":"function","function":{"name":"X"}}` | 强制调用指定工具 X | 流程编排、测试、约束输出 |

Claude 的写法是对象形式：`tool_choice={"type": "auto"}`，以及 `"any"`（对应 required）、`"tool"`（对应指定），并可设 `disable_parallel_tool_use`。

**工程价值**：`tool_choice` 是你把「概率性行为」变成「确定性行为」的主要手段。

- 最后一步要输出给用户看的自然语言 → 设 `none`，避免模型又跑去调工具。
- 某一步必须先做权限校验 → 指定调用 `check_permission`。
- 想让模型输出结构化结果而不是自由文本 → 定义一个 `submit_result` 工具并设为 required，这招比 `response_format` 更可控，因为 Schema 完全由你写。

## 4. parallel_tool_calls

默认 `true`：模型可以在一轮里返回多个工具调用（比如同时查北京和上海的天气）。

- 好处：减少往返轮次，显著降延迟。
- 风险：多个调用之间如果有依赖（第二个依赖第一个的结果），并行会出错。
- 处理：执行层要**并发执行 + 按 `tool_call_id` 回填**，顺序无所谓，但 id 必须对上。

想关掉就设 `parallel_tool_calls=false`（Claude 用 `disable_parallel_tool_use=true`），强制一次只调一个，逻辑更简单但更慢。

## 5. response_format：让输出一定合法

### json_object

要求模型输出**合法的 JSON**。注意两点：

- 只保证「是合法 JSON」，**不保证符合你的业务 Schema**。
- 必须在 prompt 里同时说明要输出 JSON，否则某些模型会报错或输出空白。

### json_schema（Structured Outputs）

你给一份 JSON Schema，模型输出**严格符合**该 Schema。

原理是**约束解码（constrained decoding / grammar-based sampling）**：

```
普通采样：从整个词表里抽下一个 token
约束解码：先根据 Schema 算出「当前位置哪些 token 合法」，
          把非法 token 的 logits 直接置为 -inf，
          再只在合法集合里采样
```

具体做法是维护一个**状态机 / 文法**：生成 `{` 之后，下一个合法 token 只能是 `"`（属性名开头）；生成 `"city":` 之后，若 Schema 说 city 是 string，那下一个只能是 `"`……逐 token 把搜索空间剪到合法分支上。

结果：**格式 100% 合法**（不是「大概率」）。

代价：

- 首次请求要编译 Schema，有一点延迟（通常可缓存）。
- Schema 有支持范围限制（嵌套深度、属性数量、`additionalProperties` 等），太复杂会被拒。

**Agent 视角**：凡是「模型的输出要被代码直接解析」的地方，优先用 json_schema。顺带一提，`tools` 的参数生成也是靠同一套机制保证合法的。

### 那 tools 和 response_format 该怎么选

| 需求 | 选哪个 |
|---|---|
| 要执行副作用（查库、发请求、写文件） | `tools` |
| 只要结构化结果，不需要执行任何东西 | `response_format: json_schema` |
| 想让「结构化输出」出现在推理之后 | 定义 `submit_result` 工具 + `tool_choice` 控制 |
| 模型能力弱、不支持 json_schema | 用 `tools` 兜底（多数模型都支持 function calling） |

## 6. 跨家对比速查

| 能力 | OpenAI（Chat Completions） | Anthropic Claude | DeepSeek / 通义等国产 |
|---|---|---|---|
| 工具定义 | `tools[].function` + JSON Schema | `tools[]` 的 `name` / `description` / `input_schema` | 基本对齐 OpenAI |
| 结果回填 | `role=tool` + `tool_call_id` | user 消息里的 `tool_result` content block | 对齐 OpenAI |
| 强制调用 | `tool_choice`（字符串或对象） | `tool_choice` 对象形式 | 对齐 OpenAI |
| 并行调用 | `parallel_tool_calls` | `disable_parallel_tool_use` | 多数支持 |
| 结构化输出 | `response_format: json_schema` | 结构化输出 / `output_format`（新版） | 多数支持 json_object，json_schema 支持度不一 |
| system 位置 | messages 里的 `role=system` | 顶层 `system` 字段 | messages 里 |
| temperature 范围 | 0-2 | 0-1 | 0-2（各家略不同） |
| top_k | 不支持 | 支持 | 部分支持 |
| 采样参数注意 | 推理模型不支持 | Opus 4.7 及以上不支持 temperature / top_p / top_k | 各家自查 |

## 7. 一个最小 Agent 循环（伪代码）

把前四篇串起来：

```python
messages = [{"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}]

for step in range(MAX_STEPS):            # 最大步数，死循环保险
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",              # C1-4
        temperature=0,                   # C1-2
        max_completion_tokens=2048,      # C1-3
        parallel_tool_calls=True,        # C1-4
    )
    choice = resp.choices[0]
    messages.append(choice.message)      # assistant 消息（可能含 tool_calls）

    if choice.finish_reason == "tool_calls":        # C1-3 的方向盘
        for call in choice.message.tool_calls:
            result = execute(call.function.name,
                             json.loads(call.function.arguments))
            messages.append({"role": "tool",
                             "tool_call_id": call.id,     # 按 id 回填
                             "content": json.dumps(result, ensure_ascii=False)})
        continue                                     # 继续循环

    if choice.finish_reason == "length":
        raise RuntimeError("输出被截断，增大 max_completion_tokens")

    return choice.message.content                    # finish_reason == "stop"
```

这段代码里每一个参数，都能对应回前四篇讲的内容。

## 8. 下一篇

C1-5 把所有内容压成一张速查表，配 12 道自测题。读完那篇，这门课就结课了。
