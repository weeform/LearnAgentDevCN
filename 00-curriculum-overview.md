# 00 · 学习路径总纲
> 这份文档是
> 总纲
> ：它不教知识，只回答三个问题 —— 课程地图长什么样、下一课是什么、为什么是这个顺序。每新增一门课，这里的课程地图会同步更新；**你个人学到哪了，记在 progress.md，不写在这里**。

## 1. 怎么用这份总纲

- 入口在第 3 节「课程地图」：从阶段 0 开始，按顺序一门门读下去；读完一篇就在 progress.md 勾一篇。
- **赶时间、想先做出东西**：直接走第 5.2 节的 MVP 路径（20 篇 / 4 个晚上），别从头啃。第 5.3 节列了 12 组「故意不学」的内容和回来的触发信号。
- 每篇按 8–15 分钟设计，正好一趟地铁；超过这个长度的篇目会在开头标注「建议分两次读」。
- 每篇正文末尾有 3 道**思考题**（附折叠的参考思路），不用写下来，在地铁上想一遍就够；每门课最后一篇是「速查表 + 自测」，回程做自测，比再读一遍有用得多。
- 顺序可以跳：标了「可跳」的课不影响后续理解，读不下去就先过，别卡在原地。

## 2. 为什么第一门课是「调用参数」

Agent 的本质：**用代码反复调用大模型，并根据返回结果决定下一步。**

所以第一个要搞清楚的，不是 Transformer，而是「一次 API 调用里我到底能拧哪几个旋钮，拧下去模型行为会怎么变」。这决定了你后面写的 Agent 稳不稳、贵不贵、能不能复现、能不能调试。

理论只取「够用」的部分，唯一的例外是 C2（KV Cache）：它是「成本与上下文」这条暗线的地基，也是 Agent 工程里少数能直接换算成钱的原理。其余理论一律推到阶段 5 之后再补。

## 3. 路径总览

- **阶段 0 · 模型调用与参数原理** → 产出：一次带工具调用的对话
- **阶段 1 · Prompt 与上下文工程** → 产出：一套可复用的 system prompt 模板 + 上下文裁剪策略
- **阶段 2 · Agent 最小闭环** → 产出：手写一个 100 行以内的 ReAct 循环
- **阶段 3 · 记忆与状态** → 产出：会话记忆 + 长期记忆检索跑通
- **阶段 4 · 多 Agent 与编排** → 产出：一个可拆任务、可并行的小型多 Agent 系统
- **阶段 5 · 工程化（观测 / 评测 / 成本 / 安全）** → 产出：全链路 trace + 一个回归评测集
- **阶段 6 · 实战项目** → 产出：3 个能放进作品集的项目

**阶段直达**：

- [阶段 0 · 模型调用与参数原理](01-stage-0-model-api/README.md) — 6 门课 / 27 篇
- [阶段 1 · Prompt 与上下文工程](02-stage-1-prompt-context/README.md) — 3 门课 / 14 篇
- [阶段 2 · Agent 最小闭环](03-stage-2-minimal-agent-loop/README.md) — 4 门课 / 20 篇
- [阶段 3 · 记忆与状态](04-stage-3-memory-state/README.md) — 3 门课 / 15 篇
- [阶段 4 · 多 Agent 与编排](05-stage-4-multi-agent-orchestration/README.md) — 3 门课 / 13 篇
- [阶段 5 · 工程化](06-stage-5-production-engineering/README.md) — 5 门课 / 24 篇
- [阶段 6 · 实战项目](07-stage-6-capstone/README.md) — 3 门课 / 15 篇

## 4. 课程地图

资料库里所有内容按「阶段 → 课程 → 单篇」三层放，**课程不会直接铺在根目录，都挂在所属阶段文件夹下**。已整理：阶段 0（6 门课 / 27 篇）、阶段 1（3 门课 / 14 篇）、阶段 2（4 门课 / 20 篇）、阶段 3（3 门课 / 15 篇）、阶段 4（3 门课 / 13 篇）、阶段 5（5 门课 / 24 篇）、阶段 6（3 门课 / 15 篇），各含相应课程索引。

**阶段 0 · 模型调用与参数原理**— 6 门课 / 27 篇 · 约 5–6 小时

**C0 · 大模型工作原理速成（前置课）**— 5 篇 · 每篇 10–15 分钟 → [打开课程](01-stage-0-model-api/00-c0-llm-fundamentals/README.md)

- [C0-1 大模型到底在做什么](01-stage-0-model-api/00-c0-llm-fundamentals/01-what-llm-actually-does.md)
- [C0-2 Token 与向量：模型只认数字](01-stage-0-model-api/00-c0-llm-fundamentals/02-token-and-vector.md)
- [C0-3 Transformer 骨架：一层在做什么](01-stage-0-model-api/00-c0-llm-fundamentals/03-transformer-block-anatomy.md)
- [C0-4 注意力与 Q / K / V](01-stage-0-model-api/00-c0-llm-fundamentals/04-attention-qkv.md)
- [C0-5 一次推理的完整流程](01-stage-0-model-api/00-c0-llm-fundamentals/05-full-inference-pipeline.md)

**读书顺序提示**：C0 在 C1 之前。完全不懂模型原理的话先读它；已经懂 Q / K / V 和注意力的话可以直接跳过，但读 C2 前必须过 C0-4。

**C1 · 大模型调用参数与原理**— 5 篇 · 每篇 8–15 分钟 → [打开课程](01-stage-0-model-api/01-c1-call-parameters/README.md)

- [C1-1 课程导览与参数全景图](01-stage-0-model-api/01-c1-call-parameters/01-parameter-map.md)
- [C1-2 采样参数：temperature 与 top_p 的原理](01-stage-0-model-api/01-c1-call-parameters/02-sampling-temperature-top-p.md)
- [C1-3 输入、长度与停止：messages / max_tokens / stop / stream](01-stage-0-model-api/01-c1-call-parameters/03-input-length-stop.md)
- [C1-4 Agent 核心参数：tools / tool_choice / response_format](01-stage-0-model-api/01-c1-call-parameters/04-agent-core-parameters.md)
- [C1-5 速查表与自测题](01-stage-0-model-api/01-c1-call-parameters/05-cheatsheet-and-quiz.md)

**C2 · KV Cache 机制与 Agent 上下文复用**— 5 篇 · 每篇 10–15 分钟 · 可跳 → [打开课程](01-stage-0-model-api/02-c2-kv-cache/README.md)

- [C2-1 为什么需要 KV Cache](01-stage-0-model-api/02-c2-kv-cache/01-why-kv-cache.md)
- [C2-2 KV Cache 原理：Q / K / V](01-stage-0-model-api/02-c2-kv-cache/02-kv-cache-mechanics.md)
- [C2-3 模型内部流程：prefill 与 decode](01-stage-0-model-api/02-c2-kv-cache/03-prefill-and-decode.md)
- [C2-4 压缩与优化：GQA / MLA / PagedAttention / 量化](01-stage-0-model-api/02-c2-kv-cache/04-gqa-mla-pagedattention.md)
- [C2-5 Agent 实战：如何利用 KV Cache](01-stage-0-model-api/02-c2-kv-cache/05-agent-practice-kv-cache.md)

**C3 · Token、分词与成本模型**— 4 篇 · 每篇 10–13 分钟 → [打开课程](01-stage-0-model-api/03-c3-tokenization-cost/README.md)

- [C3-1 Token 与分词：BPE 直觉与 6 个坑](01-stage-0-model-api/03-c3-tokenization-cost/01-bpe-tokenization-pitfalls.md)
- [C3-2 怎么数 token：工具、误差与估算公式](01-stage-0-model-api/03-c3-tokenization-cost/02-counting-tokens.md)
- [C3-3 成本结构：一次调用的钱花在哪](01-stage-0-model-api/03-c3-tokenization-cost/03-cost-breakdown.md)
- [C3-4 上下文预算表、降本优先级与自测](01-stage-0-model-api/03-c3-tokenization-cost/04-context-budget-and-quiz.md)

**C4 · 流式输出与结构化输出**— 4 篇 · 每篇约 12 分钟 → [打开课程](01-stage-0-model-api/04-c4-streaming-structured-output/README.md)

- [C4-1 流式输出：SSE 协议与增量解析](01-stage-0-model-api/04-c4-streaming-structured-output/01-sse-streaming.md)
- [C4-2 工具调用的流式拼接](01-stage-0-model-api/04-c4-streaming-structured-output/02-streaming-tool-calls.md)
- [C4-3 结构化输出：JSON Schema 与 strict 模式](01-stage-0-model-api/04-c4-streaming-structured-output/03-json-schema-strict.md)
- [C4-4 解析容错、失败恢复与自测](01-stage-0-model-api/04-c4-streaming-structured-output/04-parsing-fallback-and-quiz.md)

**C5 · 稳定性：错误、重试、限流与降级**— 4 篇 · 每篇 11–15 分钟 → [打开课程](01-stage-0-model-api/05-c5-reliability/README.md)

- [C5-1 错误全景：状态码与可重试性](01-stage-0-model-api/05-c5-reliability/01-error-taxonomy.md)
- [C5-2 重试策略：退避、jitter 与幂等](01-stage-0-model-api/05-c5-reliability/02-retry-backoff-idempotency.md)
- [C5-3 限流、并发、超时与降级](01-stage-0-model-api/05-c5-reliability/03-ratelimit-concurrency-degradation.md)
- [C5-4 阶段 0 总复习：速查表、交付物与综合自测](01-stage-0-model-api/05-c5-reliability/04-stage-0-review-and-quiz.md)

**阶段 1 · Prompt 与上下文工程**— 3 门课 / 14 篇 · 约 3.5–4.5 小时

**C6 · System Prompt 工程与提示词模式**— 6 篇 · 每篇 10–14 分钟 → [打开课程](02-stage-1-prompt-context/00-c6-system-prompt-patterns/README.md)

- [C6-1 五段式模板](02-stage-1-prompt-context/00-c6-system-prompt-patterns/01-system-prompt-five-part.md)
- [C6-2 约束 > 角色](02-stage-1-prompt-context/00-c6-system-prompt-patterns/02-constraints-over-persona.md)
- [C6-3 少样本 / 思维链 / 自一致性](02-stage-1-prompt-context/00-c6-system-prompt-patterns/03-few-shot-cot-self-consistency.md)
- [C6-4 CoT 的反例与提示词模式清单](02-stage-1-prompt-context/00-c6-system-prompt-patterns/04-cot-pitfalls-and-pattern-library.md)
- [C6-5 Prompt 版本管理与回归测试](02-stage-1-prompt-context/00-c6-system-prompt-patterns/05-prompt-versioning-and-regression.md)
- [C6-6 速查表与自测](02-stage-1-prompt-context/00-c6-system-prompt-patterns/06-cheatsheet-and-quiz.md)

**C7 · 上下文管理与压缩**— 4 篇 · 每篇 14–17 分钟 → [打开课程](02-stage-1-prompt-context/01-c7-context-management/README.md)

- [C7-1 上下文预算](02-stage-1-prompt-context/01-c7-context-management/01-context-budget.md)
- [C7-2 裁剪与 KV Cache](02-stage-1-prompt-context/01-c7-context-management/02-truncation-and-kv-cache.md)
- [C7-3 摘要与压缩](02-stage-1-prompt-context/01-c7-context-management/03-summarization-and-compression.md)
- [C7-4 上下文装配与裁剪策略](02-stage-1-prompt-context/01-c7-context-management/04-context-assembly-and-quiz.md)

**C8 · 提示词安全与注入防御**— 4 篇 · 每篇 10–13 分钟 → [打开课程](02-stage-1-prompt-context/02-c8-prompt-security/README.md)

- [C8-1 注入全景](02-stage-1-prompt-context/02-c8-prompt-security/01-injection-taxonomy.md)
- [C8-2 间接注入防御](02-stage-1-prompt-context/02-c8-prompt-security/02-indirect-injection-defense.md)
- [C8-3 防御清单](02-stage-1-prompt-context/02-c8-prompt-security/03-defense-checklist.md)
- [C8-4 速查与自测](02-stage-1-prompt-context/02-c8-prompt-security/04-cheatsheet-and-quiz.md)

**阶段 2 · Agent 最小闭环**— 4 门课 / 20 篇 · 约 4–5.5 小时（含动手）

**C9 · 工具调用协议与 ReAct 手写**— 5 篇 · 每篇 10–15 分钟 → [打开课程](03-stage-2-minimal-agent-loop/00-c9-tool-calling-react/README.md)

- [C9-1 工具调用协议细节](03-stage-2-minimal-agent-loop/00-c9-tool-calling-react/01-tool-calling-protocol-detail.md)
- [C9-2 ReAct 三段式](03-stage-2-minimal-agent-loop/00-c9-tool-calling-react/02-react-loop-anatomy.md)
- [C9-3 手写 100 行 ReAct](03-stage-2-minimal-agent-loop/00-c9-tool-calling-react/03-react-implementation.md)
- [C9-4 循环终止条件](03-stage-2-minimal-agent-loop/00-c9-tool-calling-react/04-loop-termination.md)
- [C9-5 速查表与自测](03-stage-2-minimal-agent-loop/00-c9-tool-calling-react/05-cheatsheet-and-quiz.md)

**C10 · 工具设计：粒度、描述、参数校验与操作型工具**— 6 篇 · 每篇 10–15 分钟 → [打开课程](03-stage-2-minimal-agent-loop/01-c10-tool-design/README.md)

- [C10-1 工具粒度](03-stage-2-minimal-agent-loop/01-c10-tool-design/01-tool-granularity.md)
- [C10-2 命名与描述](03-stage-2-minimal-agent-loop/01-c10-tool-design/02-tool-naming-description.md)
- [C10-3 参数校验](03-stage-2-minimal-agent-loop/01-c10-tool-design/03-tool-param-validation.md)
- [C10-4 操作型工具：computer use 与浏览器](03-stage-2-minimal-agent-loop/01-c10-tool-design/04-computer-use-and-browser.md)
- [C10-5 多模态输入：什么时候必须「看」](03-stage-2-minimal-agent-loop/01-c10-tool-design/05-multimodal-input.md)
- [C10-6 设计清单与自测](03-stage-2-minimal-agent-loop/01-c10-tool-design/06-cheatsheet-and-quiz.md)

**C11 · Agent 失效模式与恢复**— 5 篇 · 每篇 10–15 分钟 → [打开课程](03-stage-2-minimal-agent-loop/02-c11-agent-failure-recovery/README.md)

- [C11-1 失效模式全景](03-stage-2-minimal-agent-loop/02-c11-agent-failure-recovery/01-failure-taxonomy.md)
- [C11-2 错误回传与自我修正](03-stage-2-minimal-agent-loop/02-c11-agent-failure-recovery/02-error-feedback-self-correction.md)
- [C11-3 步数 / 死循环 / 超时](03-stage-2-minimal-agent-loop/02-c11-agent-failure-recovery/03-loop-guard-deadlock-timeout.md)
- [C11-4 什么时候不该用 Agent](03-stage-2-minimal-agent-loop/02-c11-agent-failure-recovery/04-when-not-to-use-agent.md)
- [C11-5 失效模式速查与自测](03-stage-2-minimal-agent-loop/02-c11-agent-failure-recovery/05-stage-2-review-and-quiz.md)

**C12 · 工具生态：MCP 与能力复用**— 4 篇 · 每篇 10–13 分钟 → [打开课程](03-stage-2-minimal-agent-loop/03-c12-mcp/README.md)

- [C12-1 MCP 是什么、解决什么问题](03-stage-2-minimal-agent-loop/03-c12-mcp/01-what-is-mcp.md)
- [C12-2 怎么用：接现成 MCP server](03-stage-2-minimal-agent-loop/03-c12-mcp/02-use-mcp-server.md)
- [C12-3 怎么写：把工具包成 MCP server](03-stage-2-minimal-agent-loop/03-c12-mcp/03-write-mcp-server.md)
- [C12-4 MCP 安全与阶段 2 总复习](03-stage-2-minimal-agent-loop/03-c12-mcp/04-mcp-security-and-quiz.md)

**阶段 3 · 记忆与状态**— 3 门课 / 15 篇 · 约 4–5 小时

**C13 · 会话记忆与压缩**— 5 篇 · 每篇 12–13 分钟 → [打开课程](04-stage-3-memory-state/00-c13-conversation-memory/README.md)

- [C13-1 消息数组就是短期记忆](04-stage-3-memory-state/00-c13-conversation-memory/01-message-array-as-memory.md)
- [C13-2 压缩三法：摘要/删除/保留](04-stage-3-memory-state/00-c13-conversation-memory/02-compression-strategies.md)
- [C13-3 工具返回的预算黑洞](04-stage-3-memory-state/00-c13-conversation-memory/03-tool-result-budget.md)
- [C13-4 压缩的代价怎么量](04-stage-3-memory-state/00-c13-conversation-memory/04-compression-cost.md)
- [C13-5 速查表与自测](04-stage-3-memory-state/00-c13-conversation-memory/05-cheatsheet-and-quiz.md)

**C14 · 检索与长期记忆（RAG 全链路）**— 5 篇 · 每篇 12–14 分钟 → [打开课程](04-stage-3-memory-state/01-c14-rag-long-term-memory/README.md)

- [C14-1 什么时候根本不需要 RAG](04-stage-3-memory-state/01-c14-rag-long-term-memory/01-when-not-to-rag.md)
- [C14-2 切分与 Embedding](04-stage-3-memory-state/01-c14-rag-long-term-memory/02-chunking-and-embedding.md)
- [C14-3 检索与向量库选型](04-stage-3-memory-state/01-c14-rag-long-term-memory/03-retrieval-and-vector-db.md)
- [C14-4 重排与记忆维护](04-stage-3-memory-state/01-c14-rag-long-term-memory/04-rerank-and-memory-maintenance.md)
- [C14-5 速查表与自测](04-stage-3-memory-state/01-c14-rag-long-term-memory/05-cheatsheet-and-quiz.md)

**C15 · 外部状态与断点续跑**— 5 篇 · 每篇 12–14 分钟 → [打开课程](04-stage-3-memory-state/02-c15-external-state-checkpoint/README.md)

- [C15-1 状态外置：任务状态机](04-stage-3-memory-state/02-c15-external-state-checkpoint/01-task-state-machine.md)
- [C15-2 断点续跑：checkpoint 与恢复](04-stage-3-memory-state/02-c15-external-state-checkpoint/02-checkpoint-resume.md)
- [C15-3 按需加载与上下文分区](04-stage-3-memory-state/02-c15-external-state-checkpoint/03-on-demand-loading-partition.md)
- [C15-4 子 Agent 隔离上下文](04-stage-3-memory-state/02-c15-external-state-checkpoint/04-subagent-context-isolation.md)
- [C15-5 阶段 3 总复习与自测](04-stage-3-memory-state/02-c15-external-state-checkpoint/05-stage-3-review-and-quiz.md)

**阶段 4 · 多 Agent 与编排**— 3 门课 / 13 篇 · 约 3–4 小时

**C16 · 拆分信号与编排模式**— 5 篇 · 每篇 8–15 分钟 → [打开课程](05-stage-4-multi-agent-orchestration/00-c16-decomposition-orchestration/README.md)

- [C16-1 拆分信号：先判断该不该拆](05-stage-4-multi-agent-orchestration/00-c16-decomposition-orchestration/01-when-to-decompose.md)
- [C16-2 拆分的代价](05-stage-4-multi-agent-orchestration/00-c16-decomposition-orchestration/02-decomposition-cost.md)
- [C16-3 编排模式一：路由与流水线](05-stage-4-multi-agent-orchestration/00-c16-decomposition-orchestration/03-routing-pipeline.md)
- [C16-4 编排模式二：主从与黑板](05-stage-4-multi-agent-orchestration/00-c16-decomposition-orchestration/04-master-slave-blackboard.md)
- [C16-5 速查表与自测](05-stage-4-multi-agent-orchestration/00-c16-decomposition-orchestration/05-cheatsheet-and-quiz.md)

**C17 · 框架横评与自研取舍**— 4 篇 · 每篇 10–15 分钟 → [打开课程](05-stage-4-multi-agent-orchestration/01-c17-framework-evaluation/README.md)

- [C17-1 评判框架的三个维度](05-stage-4-multi-agent-orchestration/01-c17-framework-evaluation/01-evaluation-dimensions.md)
- [C17-2 LangGraph / AutoGen / CrewAI 横评](05-stage-4-multi-agent-orchestration/01-c17-framework-evaluation/02-framework-comparison.md)
- [C17-3 逃生舱与自研取舍](05-stage-4-multi-agent-orchestration/01-c17-framework-evaluation/03-escape-hatch-and-diy.md)
- [C17-4 速查表与自测](05-stage-4-multi-agent-orchestration/01-c17-framework-evaluation/04-cheatsheet-and-quiz.md)

**C18 · Agent 间通信与结果聚合**— 4 篇 · 每篇 10–15 分钟 → [打开课程](05-stage-4-multi-agent-orchestration/02-c18-agent-communication/README.md)

- [C18-1 结构化消息 vs 自然语言](05-stage-4-multi-agent-orchestration/02-c18-agent-communication/01-structured-vs-natural-language.md)
- [C18-2 扇出与聚合](05-stage-4-multi-agent-orchestration/02-c18-agent-communication/02-fanout-aggregation.md)
- [C18-3 避免传话游戏](05-stage-4-multi-agent-orchestration/02-c18-agent-communication/03-avoid-telephone-game.md)
- [C18-4 阶段 4 总复习与自测](05-stage-4-multi-agent-orchestration/02-c18-agent-communication/04-stage-4-review-and-quiz.md)

**阶段 5 · 工程化（观测 / 评测 / 成本 / 安全）**— 5 门课 / 24 篇 · 约 5.5–7.5 小时

**C19 · 可观测性：trace 与日志规范**— 5 篇 · 每篇 12–18 分钟 → [打开课程](06-stage-5-production-engineering/00-c19-observability/README.md)

- [C19-1 为什么 Agent 必须可观测](06-stage-5-production-engineering/00-c19-observability/01-why-agent-observability.md)
- [C19-2 trace / span 结构与字段设计](06-stage-5-production-engineering/00-c19-observability/02-trace-span-structure.md)
- [C19-3 日志规范与采样](06-stage-5-production-engineering/00-c19-observability/03-logging-sampling.md)
- [C19-4 用现成工具落地](06-stage-5-production-engineering/00-c19-observability/04-tooling-otel-langsmith.md)
- [C19-5 速查表与自测](06-stage-5-production-engineering/00-c19-observability/05-cheatsheet-and-quiz.md)

**C20 · 评测：评测集、LLM-as-judge、回归**— 6 篇 · 每篇 12–15 分钟 → [打开课程](06-stage-5-production-engineering/01-c20-evaluation/README.md)

- [C20-1 评测集怎么造](06-stage-5-production-engineering/01-c20-evaluation/01-building-eval-set.md)
- [C20-2 LLM-as-judge 评分维度设计](06-stage-5-production-engineering/01-c20-evaluation/02-llm-as-judge-design.md)
- [C20-3 judge 自带哪些偏差](06-stage-5-production-engineering/01-c20-evaluation/03-judge-bias.md)
- [C20-4 评测接入 CI 与回归](06-stage-5-production-engineering/01-c20-evaluation/04-eval-in-ci-regression.md)
- [C20-5 上线之后：在线质量监控与失败样本回流](06-stage-5-production-engineering/01-c20-evaluation/05-online-quality-and-data-flywheel.md)
- [C20-6 速查表与自测](06-stage-5-production-engineering/01-c20-evaluation/06-cheatsheet-and-quiz.md)

**C21 · 成本工程：预算、分级与告警**— 4 篇 · 每篇 12–14 分钟 → [打开课程](06-stage-5-production-engineering/02-c21-cost-engineering/README.md)

- [C21-1 单位任务成本核算](06-stage-5-production-engineering/02-c21-cost-engineering/01-unit-cost-accounting.md)
- [C21-2 token 预算与告警](06-stage-5-production-engineering/02-c21-cost-engineering/02-budget-alerting.md)
- [C21-3 缓存命中率监控](06-stage-5-production-engineering/02-c21-cost-engineering/03-cache-hit-monitoring.md)
- [C21-4 模型分级 + 速查自测](06-stage-5-production-engineering/02-c21-cost-engineering/04-model-tiering-and-quiz.md)

**C22 · 模型选型与路由**— 4 篇 · 每篇 12–14 分钟 → [打开课程](06-stage-5-production-engineering/03-c22-model-selection-routing/README.md)

- [C22-1 选型四维度](06-stage-5-production-engineering/03-c22-model-selection-routing/01-selection-dimensions.md)
- [C22-2 四维度怎么打架](06-stage-5-production-engineering/03-c22-model-selection-routing/02-dimension-tradeoffs.md)
- [C22-3 分级路由](06-stage-5-production-engineering/03-c22-model-selection-routing/03-tiered-routing.md)
- [C22-4 长上下文成本曲线与开源临界点](06-stage-5-production-engineering/03-c22-model-selection-routing/04-long-context-open-source-and-quiz.md)

**C23 · 安全：权限、沙箱与人工确认**— 5 篇 · 每篇 12–14 分钟 → [打开课程](06-stage-5-production-engineering/04-c23-security/README.md)

- [C23-1 最小权限与工具权限分级](06-stage-5-production-engineering/04-c23-security/01-least-privilege.md)
- [C23-2 沙箱执行](06-stage-5-production-engineering/04-c23-security/02-sandbox-execution.md)
- [C23-3 人工确认与人在回路（HITL）](06-stage-5-production-engineering/04-c23-security/03-human-in-the-loop.md)
- [C23-4 系统级稳定性与数据外泄](06-stage-5-production-engineering/04-c23-security/04-system-reliability-data-exfil.md)
- [C23-5 速查表与自测](06-stage-5-production-engineering/04-c23-security/05-cheatsheet-and-quiz.md)

**阶段 6 · 实战项目**— 3 门课 / 15 篇 · 动手为主，约 20–30 小时

**C24 · 项目一：知识库问答 Agent（RAG + 引用）**— 5 篇 · 动手 lab → [打开课程](07-stage-6-capstone/00-c24-knowledge-base-qa/README.md)

- [C24-1 需求与验收标准](07-stage-6-capstone/00-c24-knowledge-base-qa/01-requirements-and-acceptance.md)
- [C24-2 系统设计](07-stage-6-capstone/00-c24-knowledge-base-qa/02-system-design.md)
- [C24-3 实现](07-stage-6-capstone/00-c24-knowledge-base-qa/03-implementation.md)
- [C24-4 评测与成本数据](07-stage-6-capstone/00-c24-knowledge-base-qa/04-evaluation-and-cost.md)
- [C24-5 复盘与作品集呈现](07-stage-6-capstone/00-c24-knowledge-base-qa/05-retrospective-and-portfolio.md)

**C25 · 项目二：数据分析 Agent（代码执行 + 沙箱）**— 5 篇 · 动手 lab → [打开课程](07-stage-6-capstone/01-c25-data-analysis/README.md)

- [C25-1 需求与验收标准](07-stage-6-capstone/01-c25-data-analysis/01-requirements-and-acceptance.md)
- [C25-2 系统设计](07-stage-6-capstone/01-c25-data-analysis/02-system-design.md)
- [C25-3 实现](07-stage-6-capstone/01-c25-data-analysis/03-implementation.md)
- [C25-4 评测与成本数据](07-stage-6-capstone/01-c25-data-analysis/04-evaluation-and-cost.md)
- [C25-5 复盘与作品集呈现](07-stage-6-capstone/01-c25-data-analysis/05-retrospective-and-portfolio.md)

**C26 · 项目三：自动化工作流 Agent（多步 + 长时任务）**— 5 篇 · 动手 lab → [打开课程](07-stage-6-capstone/02-c26-automation-workflow/README.md)

- [C26-1 需求与验收标准](07-stage-6-capstone/02-c26-automation-workflow/01-requirements-and-acceptance.md)
- [C26-2 系统设计](07-stage-6-capstone/02-c26-automation-workflow/02-system-design.md)
- [C26-3 实现](07-stage-6-capstone/02-c26-automation-workflow/03-implementation.md)
- [C26-4 评测与成本数据](07-stage-6-capstone/02-c26-automation-workflow/04-evaluation-and-cost.md)
- [C26-5 复盘与作品集呈现](07-stage-6-capstone/02-c26-automation-workflow/05-retrospective-and-portfolio.md)

目录规则：第一层是**阶段**（阶段 N · 主题），第二层是**课程**（CN · 主题），第三层是**单篇**（CN-M）。**C 编号全局连续，不按阶段重新从 1 开始**—— 阶段 1 从 C6 起、阶段 2 从 C9 起、阶段 3 从 C13 起、阶段 4 从 C16 起、阶段 5 从 C19 起、阶段 6 从 C24 起，这样「C3」永远只指一门课，不会重名。

## 5. 依赖关系与 MVP 路径

### 5.1 主干是线性的

0 → 1 → 2 → 3 → 4 → 5 → 6。三条已知捷径：

- 阶段 2 一动手就得有 trace：把阶段 5 的可观测性（C19）提前到阶段 2 一起做，不要等阶段 5。
- C0 是 C1 和 C2 的原理前置，完全不懂大模型的话先读 C0-1 / C0-2；读 C2 前必须过 C0-4（注意力与 Q / K / V）。C2 本身停在缓存机制，读不下去可以先跳，等阶段 1 讲上下文裁剪时再回来补。
- 阶段 6 的项目不用等全部学完：知识库问答（C24）在学完阶段 3 之后就能开工。

### 5.2 MVP 路径：最短能用的 20 篇

**128 篇不值得按顺序硬啃。** 如果你的目标是「尽快做出一个能给别人看的 Agent」，先走这条 20 篇的路线——约 5 小时（篇均 15 分钟），可分 4 个晚上。

**毕业标准**（四条，都能当着别人面验证）：

1. 一个自带 3 个工具的 Agent 能跑通一个真实任务，且**卡住时自己会停**，不会无限重试；
2. 你能报出**这个任务花了多少钱**（不是「大概几毛」，是算出来的数）；
3. 出问题时你能调出**那一次的完整步骤**，指出它在第几步判断错了；
4. 它有**权限边界**：能做什么、不能做什么、什么必须等你点确认，是写死的而不是靠它自觉。

用完这 20 篇，再看第 6 节的大纲决定往哪深挖。

#### 第 1 站 · 会调模型（2 篇，约 30 分钟）

- [C1-1 参数全景图](01-stage-0-model-api/01-c1-call-parameters/01-parameter-map.md) —— **省掉**：你不知道 `tools` / `tool_choice` / `response_format` 这些旋钮存在，后面所有「它就是不肯调工具」的问题都只能靠猜。
- [C1-4 Agent 核心参数](01-stage-0-model-api/01-c1-call-parameters/04-agent-core-parameters.md) —— **省掉**：会误以为模型真的「执行」了工具；实际上它只输出一个调用意图，执行的是你的代码。

> 顺带读结论即可：C1-2 只取「Agent 循环走 `temperature=0`」这一条，不必细读 top_p / seed 的推导。

#### 第 2 站 · 把指令写对（2 篇，约 30 分钟）

- [C6-1 五段式模板](02-stage-1-prompt-context/00-c6-system-prompt-patterns/01-system-prompt-five-part.md) —— **省掉**：system prompt 会写成一段散文，同一句话每次理解都不一样，且没法验收。
- [C6-2 约束 > 角色](02-stage-1-prompt-context/00-c6-system-prompt-patterns/02-constraints-over-persona.md) —— **省掉**：会把时间花在「你是一个资深专家」上，而它改的只是语气，不是能力。

#### 第 3 站 · 跑起循环（5 篇，约 1.5 小时）

- [C9-1 协议细节](03-stage-2-minimal-agent-loop/00-c9-tool-calling-react/01-tool-calling-protocol-detail.md) —— **省掉**：`tool` 消息漏填、并行结果串台，表现为「它明明调了工具却说没数据」。
- [C9-3 手写 100 行 ReAct](03-stage-2-minimal-agent-loop/00-c9-tool-calling-react/03-react-implementation.md) —— **这是 MVP 的核心一步**，不手写一遍，后面所有框架都只是黑盒。
- [C9-4 终止条件](03-stage-2-minimal-agent-loop/00-c9-tool-calling-react/04-loop-termination.md) —— **省掉**：第一次跑真实任务就会撞上死循环，账单在你发现之前已经烧掉。
- [C10-2 命名与描述](03-stage-2-minimal-agent-loop/01-c10-tool-design/02-tool-naming-description.md) —— **省掉**：工具都在，但模型总是选错那个；描述是它唯一的说明书。
- [C10-3 参数校验](03-stage-2-minimal-agent-loop/01-c10-tool-design/03-tool-param-validation.md) —— **省掉**：schema 只保证「类型对」，金额传 `-1`、路径传 `../../` 它一概放行。

#### 第 4 站 · 不崩、不烧钱（4 篇，约 1 小时）

- [C7-1 上下文预算](02-stage-1-prompt-context/01-c7-context-management/01-context-budget.md) —— **省掉**：不知道历史会被重复计费，第 10 轮之后成本按平方涨，而你以为是「模型变贵了」。
- [C13-3 工具返回的黑洞](04-stage-3-memory-state/00-c13-conversation-memory/03-tool-result-budget.md) —— **省掉**：一次工具返回几十 KB 塞进上下文，后面每一步都在为它重复付钱。
- [C11-2 错误回传](03-stage-2-minimal-agent-loop/02-c11-agent-failure-recovery/02-error-feedback-self-correction.md) —— **省掉**：报错被吞掉，模型以为成功了，继续在错误数据上编——这是最难查的一类故障。
- [C3-3 成本结构](01-stage-0-model-api/03-c3-tokenization-cost/03-cost-breakdown.md) —— **省掉**：算不出「一次任务多少钱」，也就无法判断某个功能值不值得上。

#### 第 5 站 · 出事能查（1 篇，约 20 分钟）

- [C19-2 trace / span 结构](06-stage-5-production-engineering/00-c19-observability/02-trace-span-structure.md) —— **省掉**：Agent 出错时你只能重跑一遍碰运气，而它非确定，碰不到；九个字段照着抄，一晚上就能加上。

#### 第 6 站 · 敢给人用（3 篇，约 45 分钟）

- [C8-3 防御清单](02-stage-1-prompt-context/02-c8-prompt-security/03-defense-checklist.md) —— **省掉**：一次间接注入就能让它把数据发到别人服务器，而你只会去改 prompt。
- [C23-1 最小权限](06-stage-5-production-engineering/04-c23-security/01-least-privilege.md) —— **省掉**：「读数据的」和「能花钱的」是同一个 Agent，等于把钱包交给一个会被说服的人。
- [C23-3 人工确认](06-stage-5-production-engineering/04-c23-security/03-human-in-the-loop.md) —— **省掉**：确认框只问「是否同意」，用户闭眼点下去，等于没有确认。

#### 第 7 站 · 走通一个、讲得出来（3 篇，约 1 小时）

- [C24-1 需求与验收](07-stage-6-capstone/00-c24-knowledge-base-qa/01-requirements-and-acceptance.md) —— **省掉**：做完了说不清「算不算做成了」，作品集里只剩「我用了 RAG」。
- [C24-2 系统设计](07-stage-6-capstone/00-c24-knowledge-base-qa/02-system-design.md) —— 两段式架构 + 引用 id 贯穿全链路，这套骨架换个题目也能用。
- [C24-3 实现](07-stage-6-capstone/00-c24-knowledge-base-qa/03-implementation.md) —— **先跑通最小闭环再加料**，这是唯一的正确顺序。

#### 排法建议

| 晚上 | 内容 | 产出 |
|---|---|---|
| 第 1 晚 | 第 1–2 站 | 一个写对的 system prompt + 一次带工具的调用 |
| 第 2 晚 | 第 3 站 | 能跑的 100 行循环（这是唯一必须动手的一晚） |
| 第 3 晚 | 第 4–5 站 | 预算表 + trace 字段，循环不再烧钱、出事能查 |
| 第 4 晚 | 第 6–7 站 | 权限边界 + 一个能演示的 capstone |

### 5.3 MVP 故意不学的（以及什么时候必须回来补）

跳过的判据不是「不重要」，而是「**现在学了也用不上**」。每条都给了回来补的**触发信号**——用现象触发，别用时间表触发。

| 跳过 | 为什么现在可以跳 | 出现什么就必须回来补 |
|---|---|---|
| C0 全 5 篇（大模型原理） | MVP 里不碰 KV Cache，不懂注意力也能跑通循环 | 开始怀疑「为什么改一个字就全变慢了」→ 读 C0-4 |
| C2 全 5 篇（KV Cache） | 省钱深水区，没有账单就没有痛感 | 账单里出现「缓存命中」这一行却看不懂 → 读 C2-1 → C2-5 |
| C4 全 4 篇（流式与结构化） | 体验优化，MVP 可以整段等 | 用户抱怨「点了没反应」→ C4-1；输出 JSON 老解析失败 → C4-3 |
| C5 全 4 篇（重试与限流） | 先写最朴素的一次超时，够用 | 第一次遇到 429 / 连接重置 → C5-1 → C5-2 |
| C12 全 4 篇（MCP） | 自己写 3 个函数比接 server 更快 | 同一批工具要在第二个项目复用 → C12-1 |
| C14 全 5 篇（RAG） | MVP 不需要长期记忆 | 用户开始问「上个月那份文档里怎么说」→ C14-1（先判断是否真需要 RAG） |
| C15 全 5 篇（状态与断点） | 任务几分钟跑完，挂了重跑即可 | 任务开始跑超过一次会话、或重跑代价明显 → C15-1 |
| C16 / C18（拆分与通信） | **前三个月都不要拆**，拆了只会多付 3–10 倍钱 | 出现「上下文污染 / 必须并行 / 职责互斥」三个信号之一 → C16-1 |
| C17（框架选型） | 没手写过就没有判断力，容易被框架带着走 | 手写循环开始重复造轮子 → C17-1（三维度） |
| C20 全 5 篇（评测） | 手上还没有 20 条真实用例 | 改了 prompt 说不清变好还是变差 → C20-1 |
| C21 / C22（成本与选型） | 一个模型跑到底，先不折腾 | 单任务成本超过一杯咖啡、或延迟被投诉 → C21-1 / C22-1 |
| C25 / C26（另两个 capstone） | 先做完一个，别三个都开 | 想做数据分析或长时自动化时再回来 |

> 一句话：**MVP 只欠三类债——原理债、规模债、体验债。** 原理债等「看不懂现象」时还，规模债等「第一次被打脸」时还，体验债等「用户抱怨」时还。三类债都不会因为拖延而变贵。

## 6. 各阶段详细大纲

## 阶段 0 · 模型调用与参数原理

- C1-1 一次调用的完整生命周期 + 参数全景图
- C1-2 采样参数：temperature / top_p / top_k / seed / penalty
- C1-3 输入与长度：messages / system / max_tokens / stop / stream / finish_reason
- C1-4 结构化与工具：response_format / tools / tool_choice / parallel_tool_calls
- C1-5 速查表 + 自测
- C2-1 ~ C2-5 KV Cache 机制与 Agent 上下文复用（理论加深，可跳）
- C3-1 ~ C3-4 Token、分词与成本模型（回答「钱花在哪」）
- C4-1 ~ C4-4 流式输出与结构化输出（回答「怎么可靠地拿到结果」）
- C5-1 ~ C5-4 稳定性：错误、重试、限流与降级（回答「失败了怎么办」，含阶段 0 总复习）

### 阶段 1 · Prompt 与上下文工程（已有正文）

→ [进入阶段 1](02-stage-1-prompt-context/README.md) — 3 门课 / 14 篇

- C6 System Prompt 工程与提示词模式（覆盖 1.1 五段式模板、1.2 少样本/思维链/自一致性）
- C7 上下文管理与压缩（覆盖 1.4 窗口、裁剪、压缩、摘要）
- C8 提示词安全与注入防御（覆盖 1.5 注入与防御）
- 1.3 结构化输出进阶 已在阶段 0 的 C4 完整覆盖，不单开课程

### 阶段 2 · Agent 最小闭环（已有正文）

→ [进入阶段 2](03-stage-2-minimal-agent-loop/README.md) — 4 门课 / 20 篇

- C9 工具调用协议与 ReAct 手写（覆盖 2.1 协议细节、2.2 ReAct 循环）
- C10 工具设计：粒度、描述与参数校验（覆盖 2.3）
- C11 Agent 失效模式与恢复（覆盖 2.4 失败恢复、2.5 何时不该用 Agent）
- C12 工具生态：MCP 与能力复用（补体检报告「缺口一」：MCP）

### 阶段 3 · 记忆与状态（已有正文）

→ [进入阶段 3](04-stage-3-memory-state/README.md) — 3 门课 / 15 篇

- C13 会话记忆与压缩（覆盖 3.1 短期记忆：消息数组管理、摘要/删除/保留、工具返回黑洞）
- C14 检索与长期记忆（覆盖 3.2；开篇答「什么时候不需要 RAG」，含记忆更新与污染）
- C15 外部状态与断点续跑（覆盖 3.3 状态机/断点续跑、3.4 按需加载与子 Agent 隔离）

### 阶段 4 · 多 Agent 与编排（已有正文）

→ [进入阶段 4](05-stage-4-multi-agent-orchestration/README.md) — 3 门课 / 13 篇

- C16 拆分信号与编排模式（覆盖 4.1 拆分信号与代价、4.2 四种编排模式）
- C17 框架横评与自研取舍（覆盖 4.3；按三维度评判，结论标注「以写作为准」）
- C18 Agent 间通信与结果聚合（覆盖 4.4；结构化消息、扇出聚合、防传话游戏）

### 阶段 5 · 工程化（已有正文）

→ [进入阶段 5](06-stage-5-production-engineering/README.md) — 5 门课 / 24 篇

- C19 可观测性：trace 与日志规范（覆盖 5.1，建议提前到阶段 2）
- C20 评测：评测集、LLM-as-judge、回归（覆盖 5.2）
- C21 成本工程：预算、分级与告警（覆盖 5.3）
- C22 模型选型与路由：选型四维度、分级路由、长上下文成本曲线、开源临界点（覆盖 5.6）
- C23 安全：权限、沙箱、人工确认（覆盖 5.5，含 5.4 系统级稳定性与数据外泄）

### 阶段 6 · 实战项目（已有正文）

→ [进入阶段 6](07-stage-6-capstone/README.md) — 3 门课 / 15 篇

- C24 项目一：知识库问答 Agent（RAG + 引用）（覆盖 6.1，阶段 3 后即可开工）
- C25 项目二：数据分析 Agent（代码执行 + 沙箱）（覆盖 6.2）
- C26 项目三：自动化工作流 Agent（多步 + 长时任务）（覆盖 6.3）

## 7. 贯穿全程的三条暗线

1. **成本意识**：每个设计决策都问一句「这会增加多少 token」。
2. **可复现性**：每个设计决策都问一句「同样的输入，明天还能得到同样的结果吗」。
3. **上下文预算**：每个设计决策都问一句「这段内容值得占用上下文吗？它稳定吗？」—— 只有稳定的前缀才能命中缓存，详见 C2-5。

## 8. 下一步

阶段 0–6 正文已全部补齐，课程完结。两条路选一条：

- **按顺序走**（想系统掌握）：阶段 0 → 1 → 2 → 3 → 4 → 5 → 6。
- **先做出来一遍**（想最快拿到东西）：走第 5.2 节的 20 篇 MVP 路径，缺口按第 5.3 节的触发信号回补。

按顺序走的具体衔接：

- 学完阶段 0 → 进阶段 1（Prompt 与上下文工程）。
- 学完阶段 2 → 进阶段 3（记忆与状态）。
- 学完阶段 3 → 进阶段 4（多 Agent 与编排）；学完阶段 4 → 进阶段 5（工程化）；学完阶段 5 → 进阶段 6（实战项目）。
- 想先补阶段 0 → 建议顺序**C0**（原理，不懂就读）→ C3（成本）→ C4（流式/结构化）→ C5（稳定性）。C2 是理论课，未读完不影响后面几课，可随时回头补。
- 阶段 6 不用等全部学完：6.1（C24）在学完阶段 3 后就能开工。

---

v2 · 2026-09-09 更新：补入 C2 课程地图；移除 mermaid 图与四列表格，改为手机端友好的列表排版；新增第三条暗线「上下文预算」；标明阶段 1.4 与 C2 的衔接关系。

v3 · 2026-09-09 更新：阶段 0 补齐 C3（Token 与成本）、C4（流式与结构化输出）、C5（稳定性工程）三门共 12 篇；C5-4 提供参数速查大表与调用层自检清单。

v4 · 2026-09-09 更新：目录重排为「阶段 → 课程 → 单篇」三层，C1–C5 全部归入「阶段 0 · 模型调用与参数原理」文件夹（原链接均保持有效）；明确 C 编号全局连续，阶段 1 从 C6 起。

v5 · 2026-09-09 更新：建全全部 7 个阶段文件夹（阶段 0–6），每个阶段页含大纲、计划课程、出口标准与阶段间依赖；总纲新增「阶段直达」入口。

v6 · 2026-09-10 更新：新增**C0 · 大模型工作原理速成**（5 篇）作为 C1 / C2 的原理前置，解决「直接用 logits / Q K V 却从未解释」的问题；在 C2-1、C2-2、C1-1 开头加入前置提示与回顾；阶段 0 扩为 6 门课 / 27 篇。

v7 · 2026-10-18 更新：阶段 1、2 补全正文——阶段 1（C6–C8 共 13 篇）、阶段 2（C9–C11 共 14 篇），均改为文件夹结构；课程地图、阶段直达、各阶段大纲同步更新。

v8 · 2026-10-18 更新：阶段 2 新增 C12（工具生态：MCP 与能力复用，4 篇），补齐体检报告「缺口一」（MCP 完全缺失）；阶段 2 扩为 4 门课 / 18 篇，阶段 3 起编号顺延为 C13。

v9 · 2026-10-19 更新：落实体检报告「缺口二」（模型选型与路由，阶段 5 新增 C22）与「缺口三」（长上下文 vs RAG 取舍，阶段 3 的 C14 开篇一节）；阶段 3–6 大纲课程编号随阶段 2 新增 C12 顺延（阶段 3 从 C13 起、阶段 6 从 C24 起）。

v10 · 2026-10-20 更新：阶段 3、4 补全正文——阶段 3（C13–C15 共 15 篇）、阶段 4（C16–C18 共 13 篇），均改为文件夹结构；课程地图、阶段直达、各阶段大纲同步更新。

v11 · 2026-10-22 更新：阶段 5、6 补全正文——阶段 5（C19–C23 共 23 篇）、阶段 6（C24–C26 共 15 篇），均改为文件夹结构；课程地图、阶段直达、各阶段大纲同步更新。至此全课程 7 阶段 / 27 门课 / 124 篇正文全部完成。

v12 · 2026-10-31 更新：① 阶段 2 的 C10 新增 **C10-4「操作型工具：computer use 与浏览器」**（原 C10-4 顺延为 C10-5），补上「操作界面」类工具的设计要点与四条安全底线；阶段 2 扩为 4 门课 / 19 篇，全课程共 **125 篇**。② 阶段 4 全 13 篇补厚（篇均 1265 → 2465 字符），补齐代码骨架、失败案例与验证动作。③ C22-1 增「推理预算（thinking）」一节、C17-2 增「厂商 SDK 分层」一节、C18-1 增「A2A 协议」一节。

v13 · 2026-10-31 更新：阶段 1、3 全 27 篇补厚（阶段 1 篇均 1514 → 3143 字符，阶段 3 篇均 1488 → 3166 字符），补齐可运行代码、量化算账与失败案例：C6 增「约束可验证判据」「症状→病灶对照表」，C7 增「伤一次缓存值不值」的分摊计算与装配代码，C8 增四种真实载荷形态与攻击链拦截点，C13 增「tool_calls 成对」硬约束与压缩悬崖，C14 增 RRF 实现与 Recall/MRR/Precision 分工，C15 增状态转移校验与子 Agent 回传契约。各课程 README 与阶段页的篇目时长同步调整。

v14 · 2026-10-31 更新：阶段 1 的 C6 新增 **C6-5「Prompt 版本管理与回归测试」**（原 C6-5 顺延为 C6-6），补上版本号判据与存放位置、回归集三类样例与三种判据、CI 硬门禁与软指标分工、灰度回滚与漂移监控，落实阶段 1 出口标准「带版本号」一条；阶段 1 扩为 3 门课 / 14 篇，全课程共 **126 篇**。同时统一 C6-1 与 C6-5 的版本号存放口径：变更史进 `meta.yaml`，运行时指纹拼在 prompt 末尾以不伤前缀缓存。

v15 · 2026-10-31 更新：阶段 5 共 12 篇补厚（篇均 1943 → 2467 字符），至此全库 126 篇**已无低于 2000 字符的篇目**，均值 2824。补入的关键内容：C19-1 无 trace 排查的时间账与 trace 的三类盲区、C19-4 OTel 接入骨架与「head sampling 丢失败样本 / PII 出域 / 字段膨胀」三坑、C20-3 第五种偏差（分数尺度漂移）与 raw agreement 的 kappa 陷阱、C20-4 flaky 用例处置、C21-2「预算要事前判」与三类看不见的钱、C21-3 命中率高不等于省钱、C22-2 thinking 作为同时拧动三条曲线的手柄、C23-3 确认与执行之间的时差漏洞、C23-4 外泄四通道。各课程 README 与阶段页时长已按新篇幅同步。

v16 · 2026-10-31 更新：**103 篇正文补「篇末思考题」**（每篇 3 问 + 折叠参考思路，放在「小结」与「下一篇」之间）——此前全库只有 23 篇课末「速查表 + 自测」，正文篇读完没有任何自检环节。这批思考题不考记忆，每问都要求把结论翻译成自己的场景（例如「改了前缀第一个字缓存会怎样」「为什么只能缓 K、V 不能缓 Q」），思路里带交叉引用到相关篇目。至此 126 篇 = 103 篇带思考题的正文 + 23 篇课末自测，全库 411,738 字符、篇均 3267。批量插入用 `scripts/add-thinking-questions.py`（幂等，新篇目可按 JSON 补题）。

v17 · 2026-10-31 更新：第 5 节从「依赖关系」扩为「**依赖关系与 MVP 路径**」，补上体检报告挂了两轮的最后一项欠账（原表里「总纲显式标出 MVP 路径」长期为「仍未做」）。新增 5.2 节「最短能用的 20 篇」：七站（会调模型 2 / 写对指令 2 / 跑起循环 5 / 不崩不烧钱 4 / 出事能查 1 / 敢给人用 3 / 走通演示 3，共约 5 小时），每篇都写了「省掉会怎样」，附四条可当面验证的毕业标准与四晚排法；新增 5.3 节列出故意跳过的 12 组内容，并给出「什么现象出现时必须回来补」的触发信号，而不是时间表。选篇原则：MVP 只欠原理债、规模债、体验债三类，都能等被打脸时再还。

v18 · 2026-11-01 更新（按体检报告第七节执行）：**结构层收口**，篇数 126 → **128**，全库 431,986 字符、篇均 3,374。① **阶段 2 补厚 7 篇**（C9-4、C9-5、C10-1、C10-3、C10-5、C11-1、C11-4），阶段篇均 2,551 → 3,095，从此不再有「最核心的阶段最薄」的问题；补入的内容是终止的假终止与预算型收口、停不下来的四种形态、工具数量 20–30 的坎、读写不同粒度、错误消息四要素、静默错误与污染扩散、以及一个能算的「该不该用 Agent」成本式。② **新增 C10-5「多模态输入」**（原 C10-5 速查顺延为 C10-6）：图片怎么计价、什么时候真的必须看、截图定位的四个误差源——补上 C10-4 computer use 缺的那半截。③ **新增 C20-5「上线之后：在线质量监控与失败样本回流」**（原 C20-5 顺延为 C20-6）：补上「离线评测」与「线上运维」之间的断点，含三个免费在线指标与评测集新陈代谢规则。④ **C9-3 增「这段代码怎么测」一节**：纯函数 / 录制回放 / 端到端评测三层，中间那层不花钱、可进 CI。⑤ 阶段 2 README 增「trace 的最小做法」6 字段表，出口标准不再指向阶段 5；C8-3 与 C23-1/C23-3、C7-3/C7-4 与 C13-2/C13-3 各加一句分工说明，消除「一段内容读两遍」的观感。
