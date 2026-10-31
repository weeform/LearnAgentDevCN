# C19-4 · 用现成工具落地
> 阅读约 18 分钟。目标：在「继续手写 trace」和「上现成工具」之间做出清醒取舍，而不是跟风上最火的那个。

## 1. 三种落地路径

| 路径 | 代表 | 成本 | 适合 |
|---|---|---|---|
| 手写最小 trace | 自己写 span + 落盘 | 低（半天） | 学习、单人小项目、阶段 6 的 demo |
| 开源标准库 | OpenTelemetry（OTel） | 中（1–2 天接入） | 要标准化、要换供应商、生产自建 |
| 托管平台 | LangSmith / Langfuse / Phoenix 等 | 中（按量计费） | 团队协作、要可视化与评测一体 |

三者的关系不是「越贵越好」，而是**按你的阶段选**：单人 demo 手写就够；要上线且有团队，再考虑后两者。

## 2. 什么时候继续手写

- 项目还在原型期，trace 需求就是「回看一次任务的步骤」。
- 不想引入新依赖、新计费。
- 阶段 6 三个项目正是这个阶段——**手写 trace 完全够**，重点是把字段设计对（C19-2），而不是工具多高级。

> 判断标准很朴素：**当你开始问「我能不能查、能不能聚合、能不能告警」时，手写就到头了**，该上工具了。

## 3. OpenTelemetry：标准化的价值

OpenTelemetry 是「可观测性的事实标准」——它定义了一套**中立的 API 和数据格式**，你的代码只对接 OTel 一次，后面导出到哪个后端（Jaeger、Grafana、Datadog、自家存储）都能换。

对 Agent 场景的核心价值：

1. **自动埋点**：主流 LLM SDK（OpenAI、Anthropic、LangChain 等）已有 OTel 插件，模型调用、token、耗时自动打点，不用自己包 span。
2. **供应商锁定风险低**：换后端只改 exporter，不动业务代码。
3. **与现有微服务观测打通**：Agent 和它调用的服务在同一个 trace 图里看。

代价：概念多（tracer/provider/exporter）、要自己搭后端存数据。个人项目会显得「重」。

接入大致长这样（20 行以内，比想象的轻）：

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

provider = TracerProvider()
provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")))
trace.set_tracer_provider(provider)

# 模型调用自动埋点（以 OpenAI SDK 为例），token / 耗时 / 模型名不用自己打
from opentelemetry.instrumentation.openai import OpenAIInstrumentor
OpenAIInstrumentor().instrument()

tracer = trace.get_tracer("agent")
with tracer.start_as_current_span("agent.run") as run:
    run.set_attribute("agent.prompt_version", "v3")   # 业务维度：自己补
    with tracer.start_as_current_span("tool.search") as s:
        s.set_attribute("tool.name", "search")
        s.set_attribute("tool.hits", len(results))     # 业务维度：自己补
```

**注意 `set_attribute` 那两行**——自动埋点只覆盖「模型调用」这一层，它不知道你的 prompt 是哪一版、这次检索命中了几条。而这些恰恰是排查时最想看的字段（C19-2 讲的业务维度）。只接自动埋点、不补业务维度，trace 会变成一堆长得一样的 HTTP 调用记录。

## 4. LangSmith 类托管平台：评测一体

LangSmith（LangChain 出品）这类平台，把 trace 可视化、评测、数据集管理做成了一个产品。它的独特价值不是「记 trace」，而是**把 trace 直接变成评测样本**：

> 你在平台上看到某次运行 trace，点一下就能「把这条存成评测用例」，下次改动后自动回归。这个闭环正是 C20 要讲的东西，托管平台替你串好了。

代价：

1. **按量计费**，数据量大后成本上升。
2. **数据出域**：trace 含敏感信息，托管意味着你的 prompt 和用户数据进第三方平台（呼应 C19-3 的脱敏，也见 C23 的数据外泄）。
3. **锁定**：评测集、数据集沉淀在平台里，迁移有成本。

## 5. 接入后最常见的三个坑

工具装上不等于可观测。这三个坑几乎每个团队都会踩一次。

**坑一：默认采样把失败样本采没了。** 多数 SDK 默认「按比例随机采样」（head sampling），设 10% 就是随机丢 90%。问题在于：**请求刚开始时，你还不知道这次会不会失败**，于是失败样本也按 10% 被丢掉——恰好在最需要证据的时候没有证据。

解法是尾部采样（tail sampling）：先缓存整条 trace，等它结束、看到状态是 error 或超出阈值再决定留不留。更省事的土办法是——**错误与超预算的 trace 强制 100% 保留**，正常的按比例采。

**坑二：PII 顺着 prompt 进了 trace 后端。** system prompt 里有客户名单，工具返回里有手机号，这些都会原样写进 span。走托管平台就意味着这些数据出了你的边界（见 C23-4）。正确做法是在 exporter 前加一层 redaction，而不是赌「没人会去翻」。

**坑三：字段膨胀，写了没人查。** trace 字段一旦堆到 40 个，就没人愿意读了。**每个字段都要能回答「我会用它做哪个查询」**，答不上来的先别加——这比事后清理便宜得多。

三个坑的共同点：都不是技术难题，而是**没人对「trace 该长什么样」负责**。所以工具选型之前，先把 C19-2 的字段清单定下来。

## 6. 一个务实的建议

| 你的处境 | 我的建议 |
|---|---|
| 个人学习 / 阶段 6 项目 | 手写最小 trace，把 C19-2 的字段设计练熟 |
| 要上线、单人/小团队 | 先接 OTel 自动埋点 + 一个自建/开源后端（如 Langfuse 自托管） |
| 有团队、要评测协作 | 上 LangSmith 类托管，把「trace→评测」闭环用起来 |
| 数据敏感、不许出域 | OTel + 自托管后端，绝不走第三方托管 |

> 一句话：**先把手写 trace 的字段设计做对，工具只是放大器和存储层**。别指望工具替你补「该记什么」的课。

## 7. 小结

- 三条路径：手写 / OTel / 托管平台，按阶段选，不是越贵越好。
- 手写的尽头是「我想查、聚合、告警了」；OTel 的价值是标准化、可换后端、自动埋点。
- 自动埋点只覆盖模型调用，业务维度（prompt 版本、检索命中数）必须自己 set_attribute。
- LangSmith 类平台的独门价值是「trace 一键转评测样本」，代价是计费 + 数据出域 + 锁定。
- 三个坑：head sampling 丢失败样本、PII 出域、字段膨胀。
- 数据敏感就别走托管，OTel + 自托管是底线。

## 思考题

> 先自己答，再展开参考思路。这三问不考记忆，考的是你能不能把它用在自己的项目上。

1. 手写、OTel、托管平台三条路径，各在什么阶段切换？切换的触发条件是什么？
2. 自动埋点为什么覆盖不到你最想看的业务维度？怎么补？
3. 「数据敏感就别走托管」——这条的判断依据是什么？

<details>
<summary>参考思路</summary>

1. 手写 → 当你想「查询、聚合、告警」时就该上 OTel；OTel → 当你需要「trace 一键转评测样本」时再考虑托管。触发条件是需求，不是团队规模。
2. 自动埋点只知道「调了模型、用了多少 token」，不知道「这次检索命中几个 chunk、prompt 是哪个版本」。必须自己 set_attribute 补业务字段。
3. 看数据是否能出域：用户数据、密钥、内部文档出境意味着合规与泄露风险，托管平台的便利换不来。底线是 OTel + 自托管后端。

</details>

## 下一篇

C19-5 是速查表与自测：把本课的核心结论固化成一张表，并用 5 道题检验。
