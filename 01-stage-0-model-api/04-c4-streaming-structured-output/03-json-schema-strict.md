# C4-3 · 结构化输出：JSON Schema 与 strict 模式
> 阅读约 13 分钟。目标：为一个业务对象写出能通过 strict 模式的 schema，并知道三条路线的取舍。

## 1. 三条路线

| 路线 | 做法 | 可靠性 | 成本 |
|---|---|---|---|
| **提示词约束** | 在 prompt 里写"只输出 JSON，不要解释" | 低～中，仍会跑偏 | 低 |
| **JSON 模式** | `response_format: {"type": "json_object"}` | 中：保证是合法 JSON，**不保证结构** | 低 |
| **Schema 模式（strict）** | `response_format: json_schema` + `strict: true` | **高：保证结构完全匹配** | 首次有编译开销 |
| **（隐藏路线）工具当结构体** | 定义一个"输出函数"，用 `tool_choice` 强制调用 | 高，且跨家支持更好 | 低 |

结论：**生产环境优先用后两条**。第一条只适合原型。

## 2. strict 模式怎么开（OpenAI 系）

```python
response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "weather_result",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "city":        {"type": "string"},
                "temperature": {"type": "number"},
                "unit":        {"type": "string", "enum": ["C", "F"]},
                "note":        {"type": ["string", "null"]}   # 可选字段写法
            },
            "required": ["city", "temperature", "unit", "note"],
            "additionalProperties": False
        }
    }
}
```

## 3. strict 模式的硬性规则

1. **所有字段必须进 `required`**——包括"可选"字段；
2. 可选字段用**`"type": ["string", "null"]`**这类联合类型表达，而不是省略；
3. 每个 object 都要写**`additionalProperties: False`**；
4. 根节点必须是 `object`（不能是数组或标量）；
5. 存在**规模上限**：属性数量、嵌套深度、枚举值个数、字符串总长都有约束（具体上限以官方文档为准，别写超深嵌套的 schema）。

违反任一条，API 会返回**400**并在错误信息里指出原因——这是好事，说明它在帮你提前发现问题。

## 4. 为什么 strict 能保证结构：约束解码

原理在 C1-4 讲过，这里补上实践含义：

- 服务端把你的 schema 编译成一个**状态机**，每一步生成时把"不合法"的 token 概率置为 `-inf`，所以模型**物理上不可能**输出不符合 schema 的内容；
- 首次使用某个 schema 时有**一次性的编译延迟**（可能几百毫秒到数秒）。之后服务端会缓存，重复调用不再有这个开销；
- 因此：**schema 要稳定**。每次动态拼接出不同 schema（比如字段名里塞时间戳），会导致反复编译，既慢又浪费。

## 5. 跨家对比

| 厂商 | 机制 | 备注 |
|---|---|---|
| OpenAI | `response_format: json_schema` + `strict` | 原生支持，约束解码 |
| Anthropic | 无原生 json_schema；**用 `tool_choice` 强制调用某个工具** | 社区与 SDK 的主流做法，效果等价 |
| DeepSeek / 通义 / 智谱 | 多提供 `json_object` 模式，部分支持 json_schema | 以各家文档为准 |
| 兼容层（vLLM / Ollama 等） | 多支持 `guided_json` / `response_format` | 开源侧一般用 guided decoding |

**"用工具当结构体"之所以流行**：工具调用是各家支持最一致、约束最强的一条路径。当你需要跨厂商时，把输出定义成一个"伪工具"，是最稳的写法。

## 6. 写 schema 的八条实践

1. **字段名和 `description` 就是 prompt**——模型靠它们理解语义，写得越清楚，抽取越准；
2. **枚举收敛**：能用 `enum` 就别用自由字符串，同时降低出错率和输出长度；
3. **日期用 ISO 8601**，并在描述里写明（`YYYY-MM-DD`）；
4. **数值注明单位**（`temperature_celsius` 而不是 `temperature`）；
5. **别嵌套太深**：2～3 层足够，深层嵌套既容易触发上限，也更易出错；
6. **可选字段全部 nullable**，避免出现"字段缺失"这种需要额外处理的分支；
7. **加一个 `confidence` 或 `reason` 字段**往往能提升准确率——让模型先想再填，比直接填更稳（这是提示词技巧，不是 schema 能力）；
8. **schema 版本化**：把它当成 API 契约管理，改了要跑回归（阶段 5）。

## 7. 完整例子：从"抽取任务"到可信对象

需求：从一段客服对话里抽出结构化工单。

```python
schema = {
    "type": "object",
    "properties": {
        "category": {"type": "string", "enum": ["退款", "物流", "质量", "其他"],
                     "description": "工单类别，只能从给定四项中选择"},
        "urgency":  {"type": "string", "enum": ["low", "medium", "high"]},
        "amount":   {"type": ["number", "null"],
                     "description": "涉及金额，单位人民币元；无则填 null"},
        "summary":  {"type": "string", "description": "不超过 30 字的问题摘要"},
        "evidence": {"type": "array", "items": {"type": "string"},
                     "description": "从原文摘录的支撑句，最多 3 条"}
    },
    "required": ["category", "urgency", "amount", "summary", "evidence"],
    "additionalProperties": False
}
```

注意 `summary` 里写了"不超过 30 字"——**schema 管结构，描述管内容**，两者配合才有效果。

## 8. 小结

- 路线取舍：原型用提示词，生产用**json_schema strict**或**工具当结构体**。
- strict 的硬规则：全 required、nullable 表可选、`additionalProperties: False`、根为 object、有规模上限。
- 约束解码保证结构；**schema 要稳定**，否则反复编译。
- 字段名与 description 是 prompt 的一部分，别敷衍。

## 下一篇

就算开了 strict，也总有需要解析自由输出的时候（尤其跨厂商、或老模型）。C4-4 讲"模型输出 → 可信对象"的容错流水线。
