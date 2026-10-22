# C19-2 · trace / span 结构与字段设计
> 阅读约 14 分钟。目标：设计一次 Agent 运行该记哪些字段、怎么分层，让事后「查得到、查得快」。

## 1. 两个核心概念：trace 与 span

借自分布式追踪（OpenTelemetry 的术语，够用即止）：

- **trace**：一次完整任务的全程，从用户输入到最终答案。一个 trace 有一个唯一 ID（`trace_id`）。
- **span**：trace 里的一个阶段，比如「一次模型调用」「一次工具调用」「一次重试」。span 有父子关系，组成一棵树。

```
trace「帮我分析上周销售数据」
├── span: LLM 调用 #1（生成执行计划）
├── span: 工具调用 query_db
│   └── span: LLM 调用 #2（读工具返回，决定下一步）
├── span: 工具调用 run_python（沙箱）
└── span: LLM 调用 #3（输出最终结论）
```

> 分层的好处：问题出在「工具调用」这层，你就只看这层的 span，不用翻整个 trace。而 trace 把散落的 span 串起来，回答「这是哪次任务的哪一步」。

## 2. 一个 span 该记哪些字段

每个 span 至少记下面这些，少了哪一条，查问题都会卡：

| 字段 | 内容 | 缺了会怎样 |
|---|---|---|
| `span_id` / `parent_id` | 自身 ID、父 span ID | 拼不出调用树，串不起任务 |
| `name` | 阶段名，如 `llm.call` / `tool.call` | 分不清这一步在干嘛 |
| `start/end` | 起止时间 | 算不出耗时 |
| `input` | 这一步的输入（prompt 片段 / 工具参数） | 不知道它「看到了什么」 |
| `output` | 这一步的输出（回复 / 工具返回，可截断） | 不知道它「得到了什么」 |
| `tokens` | 输入/输出 token 数 | 算不出成本、定位不到贵在哪 |
| `model` | 用了哪个模型 | 换模型后没法对比 |
| `status` | 成功 / 失败 / 重试 / 超时 | 数不出失败率 |
| `error` | 错误码与消息（若有） | 失败原因要靠猜 |

## 3. 两个最容易被省略的字段

1. **`model`**：很多人只记 token 不记模型名。但阶段 5 的核心动作就是「换模型、看效果」，不记模型名，A/B 对比直接报废。
2. **`input` 的完整性**：为了省钱，常把 input 截断或只记 hash。但要回答「它为什么这么做」，恰恰需要看到完整的工具返回——**那是它做决策的唯一依据**。折中：input/output 全量落盘（存对象存储），trace 里只记前 N 字符 + 全量引用。

## 4. 字段设计的三条原则

1. **能自动记就自动记**：token、耗时、模型名这些，应该由框架/装饰器自动打点，而不是靠开发者手写 `print`。手写一定会漏。
2. **先全量，后采样**：开发期全量记录，数据多了再谈采样（见 C19-3）。别一上来就省那点存储。
3. **为「对比」设计，不为「展示」设计**：字段要能支撑「改 prompt 前后、换模型前后」的横向对比，而不是只为了画一张漂亮的调用图。

## 5. 一个最小结构示例

不引入任何库，用 Python 装饰器就能搭出可用的 trace 骨架：

```python
import time, json, uuid

class Span:
    def __init__(self, name, parent=None):
        self.id = uuid.uuid4().hex[:8]
        self.parent = parent.id if parent else None
        self.name = name
        self.start = time.time()
        self.data = {}

    def finish(self, **fields):
        self.data.update(fields)
        self.data["duration_ms"] = (time.time() - self.start) * 1000
        return self.data

def trace_step(name):
    def deco(fn):
        def wrapper(*a, **kw):
            span = Span(name)
            try:
                result = fn(*a, **kw)
                span.finish(status="ok", output=str(result)[:500])
            except Exception as e:
                span.finish(status="error", error=str(e))
                raise
            print(json.dumps({**{"span": name, "id": span.id}, **span.data},
                             ensure_ascii=False))
            return result
        return wrapper
    return deco
```

> 这只是教学骨架（无并发安全、无落盘）。C19-4 会讲生产里该用 OpenTelemetry 还是 LangSmith 类工具。关键是理解：**每个阶段都套一个 span，自动记字段**。

## 6. 小结

- trace = 一次任务全程；span = 一个阶段，父子成树。
- 每个 span 至少记 9 个字段：ID/父子、名字、起止、输入、输出、token、模型、状态、错误。
- `model` 和完整 `input` 最容易被省，却恰恰是「换模型对比」和「理解决策」的关键。
- 能自动记就自动记；先全量后采样；为对比设计。

## 下一篇

C19-3 讲日志规范与采样：结构化日志长什么样、全量数据爆炸后怎么采样、敏感信息（密钥、用户数据）怎么脱敏。
