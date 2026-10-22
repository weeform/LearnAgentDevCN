# 00 · 学习路径总纲
> 这份文档是
> 总纲
> ：它不教知识，只回答三个问题 —— 课程地图长什么样、下一课是什么、为什么是这个顺序。每新增一门课，这里的课程地图会同步更新；**你个人学到哪了，记在 progress.md，不写在这里**。

## 1. 怎么用这份总纲

- 入口在第 3 节「课程地图」：从阶段 0 开始，按顺序一门门读下去；读完一篇就在 progress.md 勾一篇。
- 每篇按 8–15 分钟设计，正好一趟地铁；超过这个长度的篇目会在开头标注「建议分两次读」。
- 每门课最后一篇是「速查表 + 自测」。回程做自测，比再读一遍有用得多。
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
- [阶段 1 · Prompt 与上下文工程](02-stage-1-prompt-context/README.md) — 3 门课 / 13 篇
- [阶段 2 · Agent 最小闭环](03-stage-2-minimal-agent-loop/README.md) — 4 门课 / 18 篇
- [阶段 3 · 记忆与状态](04-stage-3-memory-state/README.md) — 3 门课 / 15 篇
- [阶段 4 · 多 Agent 与编排](05-stage-4-multi-agent-orchestration/README.md) — 3 门课 / 13 篇
- [阶段 5 · 工程化](06-stage-5-production-engineering/README.md) — 5 门课 / 23 篇
- [阶段 6 · 实战项目](07-stage-6-capstone/README.md) — 3 门课 / 15 篇

## 4. 课程地图

资料库里所有内容按「阶段 → 课程 → 单篇」三层放，**课程不会直接铺在根目录，都挂在所属阶段文件夹下**。已整理：阶段 0（6 门课 / 27 篇）、阶段 1（3 门课 / 13 篇）、阶段 2（4 门课 / 18 篇）、阶段 3（3 门课 / 15 篇）、阶段 4（3 门课 / 13 篇）、阶段 5（5 门课 / 23 篇）、阶段 6（3 门课 / 15 篇），各含相应课程索引。

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

**阶段 1 · Prompt 与上下文工程**— 3 门课 / 13 篇 · 约 2.5–3.5 小时

**C6 · System Prompt 工程与提示词模式**— 5 篇 · 每篇 8–15 分钟 → [打开课程](02-stage-1-prompt-context/00-c6-system-prompt-patterns/README.md)

- [C6-1 五段式模板](02-stage-1-prompt-context/00-c6-system-prompt-patterns/01-system-prompt-five-part.md)
- [C6-2 约束 > 角色](02-stage-1-prompt-context/00-c6-system-prompt-patterns/02-constraints-over-persona.md)
- [C6-3 少样本 / 思维链 / 自一致性](02-stage-1-prompt-context/00-c6-system-prompt-patterns/03-few-shot-cot-self-consistency.md)
- [C6-4 CoT 的反例与提示词模式清单](02-stage-1-prompt-context/00-c6-system-prompt-patterns/04-cot-pitfalls-and-pattern-library.md)
- [C6-5 速查表与自测](02-stage-1-prompt-context/00-c6-system-prompt-patterns/05-cheatsheet-and-quiz.md)

**C7 · 上下文管理与压缩**— 4 篇 · 每篇 10–15 分钟 → [打开课程](02-stage-1-prompt-context/01-c7-context-management/README.md)

- [C7-1 上下文预算](02-stage-1-prompt-context/01-c7-context-management/01-context-budget.md)
- [C7-2 裁剪与 KV Cache](02-stage-1-prompt-context/01-c7-context-management/02-truncation-and-kv-cache.md)
- [C7-3 摘要与压缩](02-stage-1-prompt-context/01-c7-context-management/03-summarization-and-compression.md)
- [C7-4 上下文装配与裁剪策略](02-stage-1-prompt-context/01-c7-context-management/04-context-assembly-and-quiz.md)

**C8 · 提示词安全与注入防御**— 4 篇 · 每篇 8–12 分钟 → [打开课程](02-stage-1-prompt-context/02-c8-prompt-security/README.md)

- [C8-1 注入全景](02-stage-1-prompt-context/02-c8-prompt-security/01-injection-taxonomy.md)
- [C8-2 间接注入防御](02-stage-1-prompt-context/02-c8-prompt-security/02-indirect-injection-defense.md)
- [C8-3 防御清单](02-stage-1-prompt-context/02-c8-prompt-security/03-defense-checklist.md)
- [C8-4 速查与自测](02-stage-1-prompt-context/02-c8-prompt-security/04-cheatsheet-and-quiz.md)

**阶段 2 · Agent 最小闭环**— 4 门课 / 18 篇 · 约 3.5–4.5 小时（含动手）

**C9 · 工具调用协议与 ReAct 手写**— 5 篇 · 每篇 10–15 分钟 → [打开课程](03-stage-2-minimal-agent-loop/00-c9-tool-calling-react/README.md)

- [C9-1 工具调用协议细节](03-stage-2-minimal-agent-loop/00-c9-tool-calling-react/01-tool-calling-protocol-detail.md)
- [C9-2 ReAct 三段式](03-stage-2-minimal-agent-loop/00-c9-tool-calling-react/02-react-loop-anatomy.md)
- [C9-3 手写 100 行 ReAct](03-stage-2-minimal-agent-loop/00-c9-tool-calling-react/03-react-implementation.md)
- [C9-4 循环终止条件](03-stage-2-minimal-agent-loop/00-c9-tool-calling-react/04-loop-termination.md)
- [C9-5 速查表与自测](03-stage-2-minimal-agent-loop/00-c9-tool-calling-react/05-cheatsheet-and-quiz.md)

**C10 · 工具设计：粒度、描述与参数校验**— 4 篇 · 每篇 10–15 分钟 → [打开课程](03-stage-2-minimal-agent-loop/01-c10-tool-design/README.md)

- [C10-1 工具粒度](03-stage-2-minimal-agent-loop/01-c10-tool-design/01-tool-granularity.md)
- [C10-2 命名与描述](03-stage-2-minimal-agent-loop/01-c10-tool-design/02-tool-naming-description.md)
- [C10-3 参数校验](03-stage-2-minimal-agent-loop/01-c10-tool-design/03-tool-param-validation.md)
- [C10-4 设计清单与自测](03-stage-2-minimal-agent-loop/01-c10-tool-design/04-cheatsheet-and-quiz.md)

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

**阶段 3 · 记忆与状态**— 3 门课 / 15 篇 · 约 3.5–4.5 小时

**C13 · 会话记忆与压缩**— 5 篇 · 每篇 8–15 分钟 → [打开课程](04-stage-3-memory-state/00-c13-conversation-memory/README.md)

- [C13-1 消息数组就是短期记忆](04-stage-3-memory-state/00-c13-conversation-memory/01-message-array-as-memory.md)
- [C13-2 压缩三法：摘要/删除/保留](04-stage-3-memory-state/00-c13-conversation-memory/02-compression-strategies.md)
- [C13-3 工具返回的预算黑洞](04-stage-3-memory-state/00-c13-conversation-memory/03-tool-result-budget.md)
- [C13-4 压缩的代价怎么量](04-stage-3-memory-state/00-c13-conversation-memory/04-compression-cost.md)
- [C13-5 速查表与自测](04-stage-3-memory-state/00-c13-conversation-memory/05-cheatsheet-and-quiz.md)

**C14 · 检索与长期记忆（RAG 全链路）**— 5 篇 · 每篇 10–15 分钟 → [打开课程](04-stage-3-memory-state/01-c14-rag-long-term-memory/README.md)

- [C14-1 什么时候根本不需要 RAG](04-stage-3-memory-state/01-c14-rag-long-term-memory/01-when-not-to-rag.md)
- [C14-2 切分与 Embedding](04-stage-3-memory-state/01-c14-rag-long-term-memory/02-chunking-and-embedding.md)
- [C14-3 检索与向量库选型](04-stage-3-memory-state/01-c14-rag-long-term-memory/03-retrieval-and-vector-db.md)
- [C14-4 重排与记忆维护](04-stage-3-memory-state/01-c14-rag-long-term-memory/04-rerank-and-memory-maintenance.md)
- [C14-5 速查表与自测](04-stage-3-memory-state/01-c14-rag-long-term-memory/05-cheatsheet-and-quiz.md)

**C15 · 外部状态与断点续跑**— 5 篇 · 每篇 8–15 分钟 → [打开课程](04-stage-3-memory-state/02-c15-external-state-checkpoint/README.md)

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

**阶段 5 · 工程化（观测 / 评测 / 成本 / 安全）**— 5 门课 / 23 篇 · 约 4.5–6 小时

**C19 · 可观测性：trace 与日志规范**— 5 篇 · 每篇 10–15 分钟 → [打开课程](06-stage-5-production-engineering/00-c19-observability/README.md)

- [C19-1 为什么 Agent 必须可观测](06-stage-5-production-engineering/00-c19-observability/01-why-agent-observability.md)
- [C19-2 trace / span 结构与字段设计](06-stage-5-production-engineering/00-c19-observability/02-trace-span-structure.md)
- [C19-3 日志规范与采样](06-stage-5-production-engineering/00-c19-observability/03-logging-sampling.md)
- [C19-4 用现成工具落地](06-stage-5-production-engineering/00-c19-observability/04-tooling-otel-langsmith.md)
- [C19-5 速查表与自测](06-stage-5-production-engineering/00-c19-observability/05-cheatsheet-and-quiz.md)

**C20 · 评测：评测集、LLM-as-judge、回归**— 5 篇 · 每篇 10–15 分钟 → [打开课程](06-stage-5-production-engineering/01-c20-evaluation/README.md)

- [C20-1 评测集怎么造](06-stage-5-production-engineering/01-c20-evaluation/01-building-eval-set.md)
- [C20-2 LLM-as-judge 评分维度设计](06-stage-5-production-engineering/01-c20-evaluation/02-llm-as-judge-design.md)
- [C20-3 judge 自带哪些偏差](06-stage-5-production-engineering/01-c20-evaluation/03-judge-bias.md)
- [C20-4 评测接入 CI 与回归](06-stage-5-production-engineering/01-c20-evaluation/04-eval-in-ci-regression.md)
- [C20-5 速查表与自测](06-stage-5-production-engineering/01-c20-evaluation/05-cheatsheet-and-quiz.md)

**C21 · 成本工程：预算、分级与告警**— 4 篇 · 每篇 10–15 分钟 → [打开课程](06-stage-5-production-engineering/02-c21-cost-engineering/README.md)

- [C21-1 单位任务成本核算](06-stage-5-production-engineering/02-c21-cost-engineering/01-unit-cost-accounting.md)
- [C21-2 token 预算与告警](06-stage-5-production-engineering/02-c21-cost-engineering/02-budget-alerting.md)
- [C21-3 缓存命中率监控](06-stage-5-production-engineering/02-c21-cost-engineering/03-cache-hit-monitoring.md)
- [C21-4 模型分级 + 速查自测](06-stage-5-production-engineering/02-c21-cost-engineering/04-model-tiering-and-quiz.md)

**C22 · 模型选型与路由**— 4 篇 · 每篇 10–13 分钟 → [打开课程](06-stage-5-production-engineering/03-c22-model-selection-routing/README.md)

- [C22-1 选型四维度](06-stage-5-production-engineering/03-c22-model-selection-routing/01-selection-dimensions.md)
- [C22-2 四维度怎么打架](06-stage-5-production-engineering/03-c22-model-selection-routing/02-dimension-tradeoffs.md)
- [C22-3 分级路由](06-stage-5-production-engineering/03-c22-model-selection-routing/03-tiered-routing.md)
- [C22-4 长上下文成本曲线与开源临界点](06-stage-5-production-engineering/03-c22-model-selection-routing/04-long-context-open-source-and-quiz.md)

**C23 · 安全：权限、沙箱与人工确认**— 5 篇 · 每篇 10–15 分钟 → [打开课程](06-stage-5-production-engineering/04-c23-security/README.md)

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

## 5. 依赖关系

主干是线性的：0 → 1 → 2 → 3 → 4 → 5 → 6。三条已知捷径：

- 阶段 2 一动手就得有 trace：5.1 可观测性提前到阶段 2 一起做，不要等阶段 5。
- C0 是 C1 和 C2 的原理前置，完全不懂大模型的话先读 C0-1 / C0-2；读 C2 前必须过 C0-4（注意力与 Q / K / V）。C2 本身停在缓存机制，读不下去可以先跳，等阶段 1 讲上下文裁剪时再回来补。
- 阶段 6 的项目不用等全部学完：6.1 在学完阶段 3 之后就能开工。

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

→ [进入阶段 1](02-stage-1-prompt-context/README.md) — 3 门课 / 13 篇

- C6 System Prompt 工程与提示词模式（覆盖 1.1 五段式模板、1.2 少样本/思维链/自一致性）
- C7 上下文管理与压缩（覆盖 1.4 窗口、裁剪、压缩、摘要）
- C8 提示词安全与注入防御（覆盖 1.5 注入与防御）
- 1.3 结构化输出进阶 已在阶段 0 的 C4 完整覆盖，不单开课程

### 阶段 2 · Agent 最小闭环（已有正文）

→ [进入阶段 2](03-stage-2-minimal-agent-loop/README.md) — 4 门课 / 18 篇

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

→ [进入阶段 5](06-stage-5-production-engineering/README.md) — 5 门课 / 23 篇

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

阶段 0–6 正文已全部补齐，课程完结。按顺序推进：

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
