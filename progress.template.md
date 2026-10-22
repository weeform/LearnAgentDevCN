# 学习进度看板

> ## ⚠️ 这是模板文件，不要直接编辑
>
> 本文件进版本库（所有人共享同一份骨架）。**真正的进度记录写在 `progress.md`**，
> 而 `progress.md` 已被 `.gitignore` 排除 —— 你的勾选状态只存在本地，不上传、不和别人冲突。
>
> **第一次使用**：先生成属于你自己的进度文件
>
> ```bash
> python scripts/init-progress.py        # 推荐，幂等：已存在则不动
> cp progress.template.md progress.md    # 或手动复制（Windows 用 copy）
> ```
>
> 之后所有进度的读写，都针对 `progress.md`。
> 若发现 `progress.md` 不存在（换了机器 / 重新克隆），重新跑一次上面的命令即可。

---

> 状态图例：`⬜` 未开始 · `🔵` 在读 · `✅` 已读完 · `⏭️` 跳过（标「可跳」且暂缓）
>
> 更新规则：读完一篇改一行，并可加一条备注（读完了 / 卡在哪 / 想深挖什么）。
> 累积 3 条「想深挖」就考虑新开一个专题目录。

记录者：<!-- 填你的名字或昵称，可选 -->
开始日期：<!-- YYYY-MM-DD -->

---

## 当前位置

**阶段 0 · 模型调用与参数原理** — 未开始

建议起点：`00-curriculum-overview.md`（先看全局学习路线）

下一课：`01-stage-0-model-api/01-c1-call-parameters/01-parameter-map.md`

---

## 阶段 0 · 模型调用与参数原理

> 出口标准见 `01-stage-0-model-api/README.md`：产出一次带工具调用的对话。

### C0 · 大模型工作原理速成（前置课） ⬜ 未开始

> 读书顺序提示：完全不懂模型原理先读 C0-1 / C0-2；**读 C2 前必须过 C0-4**。

- [ ] `01-stage-0-model-api/00-c0-llm-fundamentals/01-what-llm-actually-does.md`
- [ ] `01-stage-0-model-api/00-c0-llm-fundamentals/02-token-and-vector.md`
- [ ] `01-stage-0-model-api/00-c0-llm-fundamentals/03-transformer-block-anatomy.md`
- [ ] `01-stage-0-model-api/00-c0-llm-fundamentals/04-attention-qkv.md`
- [ ] `01-stage-0-model-api/00-c0-llm-fundamentals/05-full-inference-pipeline.md`

### C1 · 大模型调用参数与原理 ⬜ 未开始

- [ ] `01-stage-0-model-api/01-c1-call-parameters/01-parameter-map.md`
- [ ] `01-stage-0-model-api/01-c1-call-parameters/02-sampling-temperature-top-p.md`
- [ ] `01-stage-0-model-api/01-c1-call-parameters/03-input-length-stop.md`
- [ ] `01-stage-0-model-api/01-c1-call-parameters/04-agent-core-parameters.md`
- [ ] `01-stage-0-model-api/01-c1-call-parameters/05-cheatsheet-and-quiz.md`

### C2 · KV Cache 机制与 Agent 上下文复用 ⬜ 未开始（可跳）

- [ ] `01-stage-0-model-api/02-c2-kv-cache/01-why-kv-cache.md`
- [ ] `01-stage-0-model-api/02-c2-kv-cache/02-kv-cache-mechanics.md`
- [ ] `01-stage-0-model-api/02-c2-kv-cache/03-prefill-and-decode.md`
- [ ] `01-stage-0-model-api/02-c2-kv-cache/04-gqa-mla-pagedattention.md`
- [ ] `01-stage-0-model-api/02-c2-kv-cache/05-agent-practice-kv-cache.md`

### C3 · Token、分词与成本模型 ⬜ 未开始

- [ ] `01-stage-0-model-api/03-c3-tokenization-cost/01-bpe-tokenization-pitfalls.md`
- [ ] `01-stage-0-model-api/03-c3-tokenization-cost/02-counting-tokens.md`
- [ ] `01-stage-0-model-api/03-c3-tokenization-cost/03-cost-breakdown.md`
- [ ] `01-stage-0-model-api/03-c3-tokenization-cost/04-context-budget-and-quiz.md`

### C4 · 流式输出与结构化输出 ⬜ 未开始

- [ ] `01-stage-0-model-api/04-c4-streaming-structured-output/01-sse-streaming.md`
- [ ] `01-stage-0-model-api/04-c4-streaming-structured-output/02-streaming-tool-calls.md`
- [ ] `01-stage-0-model-api/04-c4-streaming-structured-output/03-json-schema-strict.md`
- [ ] `01-stage-0-model-api/04-c4-streaming-structured-output/04-parsing-fallback-and-quiz.md`

### C5 · 稳定性：错误、重试、限流与降级 ⬜ 未开始

- [ ] `01-stage-0-model-api/05-c5-reliability/01-error-taxonomy.md`
- [ ] `01-stage-0-model-api/05-c5-reliability/02-retry-backoff-idempotency.md`
- [ ] `01-stage-0-model-api/05-c5-reliability/03-ratelimit-concurrency-degradation.md`
- [ ] `01-stage-0-model-api/05-c5-reliability/04-stage-0-review-and-quiz.md`

---

## 阶段 1 · Prompt 与上下文工程

> 出口标准见 `02-stage-1-prompt-context/README.md`：一套 system prompt 模板 + 上下文裁剪策略 + 注入防御清单。

### C6 · System Prompt 工程与提示词模式 ⬜ 未开始

- [ ] `02-stage-1-prompt-context/00-c6-system-prompt-patterns/01-system-prompt-five-part.md`
- [ ] `02-stage-1-prompt-context/00-c6-system-prompt-patterns/02-constraints-over-persona.md`
- [ ] `02-stage-1-prompt-context/00-c6-system-prompt-patterns/03-few-shot-cot-self-consistency.md`
- [ ] `02-stage-1-prompt-context/00-c6-system-prompt-patterns/04-cot-pitfalls-and-pattern-library.md`
- [ ] `02-stage-1-prompt-context/00-c6-system-prompt-patterns/05-cheatsheet-and-quiz.md`

### C7 · 上下文管理与压缩 ⬜ 未开始

- [ ] `02-stage-1-prompt-context/01-c7-context-management/01-context-budget.md`
- [ ] `02-stage-1-prompt-context/01-c7-context-management/02-truncation-and-kv-cache.md`
- [ ] `02-stage-1-prompt-context/01-c7-context-management/03-summarization-and-compression.md`
- [ ] `02-stage-1-prompt-context/01-c7-context-management/04-context-assembly-and-quiz.md`

### C8 · 提示词安全与注入防御 ⬜ 未开始

- [ ] `02-stage-1-prompt-context/02-c8-prompt-security/01-injection-taxonomy.md`
- [ ] `02-stage-1-prompt-context/02-c8-prompt-security/02-indirect-injection-defense.md`
- [ ] `02-stage-1-prompt-context/02-c8-prompt-security/03-defense-checklist.md`
- [ ] `02-stage-1-prompt-context/02-c8-prompt-security/04-cheatsheet-and-quiz.md`

---

## 阶段 2 · Agent 最小闭环

> 出口标准见 `03-stage-2-minimal-agent-loop/README.md`：手写 100 行 ReAct + 3 工具 + trace + 失败复盘。

### C9 · 工具调用协议与 ReAct 手写 ⬜ 未开始

- [ ] `03-stage-2-minimal-agent-loop/00-c9-tool-calling-react/01-tool-calling-protocol-detail.md`
- [ ] `03-stage-2-minimal-agent-loop/00-c9-tool-calling-react/02-react-loop-anatomy.md`
- [ ] `03-stage-2-minimal-agent-loop/00-c9-tool-calling-react/03-react-implementation.md`
- [ ] `03-stage-2-minimal-agent-loop/00-c9-tool-calling-react/04-loop-termination.md`
- [ ] `03-stage-2-minimal-agent-loop/00-c9-tool-calling-react/05-cheatsheet-and-quiz.md`

### C10 · 工具设计：粒度、描述与参数校验 ⬜ 未开始

- [ ] `03-stage-2-minimal-agent-loop/01-c10-tool-design/01-tool-granularity.md`
- [ ] `03-stage-2-minimal-agent-loop/01-c10-tool-design/02-tool-naming-description.md`
- [ ] `03-stage-2-minimal-agent-loop/01-c10-tool-design/03-tool-param-validation.md`
- [ ] `03-stage-2-minimal-agent-loop/01-c10-tool-design/04-cheatsheet-and-quiz.md`

### C11 · Agent 失效模式与恢复 ⬜ 未开始

- [ ] `03-stage-2-minimal-agent-loop/02-c11-agent-failure-recovery/01-failure-taxonomy.md`
- [ ] `03-stage-2-minimal-agent-loop/02-c11-agent-failure-recovery/02-error-feedback-self-correction.md`
- [ ] `03-stage-2-minimal-agent-loop/02-c11-agent-failure-recovery/03-loop-guard-deadlock-timeout.md`
- [ ] `03-stage-2-minimal-agent-loop/02-c11-agent-failure-recovery/04-when-not-to-use-agent.md`
- [ ] `03-stage-2-minimal-agent-loop/02-c11-agent-failure-recovery/05-stage-2-review-and-quiz.md`

### C12 · 工具生态：MCP 与能力复用 ⬜ 未开始

- [ ] `03-stage-2-minimal-agent-loop/03-c12-mcp/01-what-is-mcp.md`
- [ ] `03-stage-2-minimal-agent-loop/03-c12-mcp/02-use-mcp-server.md`
- [ ] `03-stage-2-minimal-agent-loop/03-c12-mcp/03-write-mcp-server.md`
- [ ] `03-stage-2-minimal-agent-loop/03-c12-mcp/04-mcp-security-and-quiz.md`

---

## 阶段 3 · 记忆与状态

> 出口标准见 `04-stage-3-memory-state/README.md`：会话压缩 + 长期记忆检索 + 可断点续跑的任务。

### C13 · 会话记忆与压缩 ⬜ 未开始

- [ ] `04-stage-3-memory-state/00-c13-conversation-memory/01-message-array-as-memory.md`
- [ ] `04-stage-3-memory-state/00-c13-conversation-memory/02-compression-strategies.md`
- [ ] `04-stage-3-memory-state/00-c13-conversation-memory/03-tool-result-budget.md`
- [ ] `04-stage-3-memory-state/00-c13-conversation-memory/04-compression-cost.md`
- [ ] `04-stage-3-memory-state/00-c13-conversation-memory/05-cheatsheet-and-quiz.md`

### C14 · 检索与长期记忆（RAG 全链路） ⬜ 未开始

- [ ] `04-stage-3-memory-state/01-c14-rag-long-term-memory/01-when-not-to-rag.md`
- [ ] `04-stage-3-memory-state/01-c14-rag-long-term-memory/02-chunking-and-embedding.md`
- [ ] `04-stage-3-memory-state/01-c14-rag-long-term-memory/03-retrieval-and-vector-db.md`
- [ ] `04-stage-3-memory-state/01-c14-rag-long-term-memory/04-rerank-and-memory-maintenance.md`
- [ ] `04-stage-3-memory-state/01-c14-rag-long-term-memory/05-cheatsheet-and-quiz.md`

### C15 · 外部状态与断点续跑 ⬜ 未开始

- [ ] `04-stage-3-memory-state/02-c15-external-state-checkpoint/01-task-state-machine.md`
- [ ] `04-stage-3-memory-state/02-c15-external-state-checkpoint/02-checkpoint-resume.md`
- [ ] `04-stage-3-memory-state/02-c15-external-state-checkpoint/03-on-demand-loading-partition.md`
- [ ] `04-stage-3-memory-state/02-c15-external-state-checkpoint/04-subagent-context-isolation.md`
- [ ] `04-stage-3-memory-state/02-c15-external-state-checkpoint/05-stage-3-review-and-quiz.md`

---

## 阶段 4 · 多 Agent 与编排

> 出口标准见 `05-stage-4-multi-agent-orchestration/README.md`：一个可拆/可并行的小型系统 + 对比数据 + 负结果记录。

### C16 · 拆分信号与编排模式 ⬜ 未开始

- [ ] `05-stage-4-multi-agent-orchestration/00-c16-decomposition-orchestration/01-when-to-decompose.md`
- [ ] `05-stage-4-multi-agent-orchestration/00-c16-decomposition-orchestration/02-decomposition-cost.md`
- [ ] `05-stage-4-multi-agent-orchestration/00-c16-decomposition-orchestration/03-routing-pipeline.md`
- [ ] `05-stage-4-multi-agent-orchestration/00-c16-decomposition-orchestration/04-master-slave-blackboard.md`
- [ ] `05-stage-4-multi-agent-orchestration/00-c16-decomposition-orchestration/05-cheatsheet-and-quiz.md`

### C17 · 框架横评与自研取舍 ⬜ 未开始

- [ ] `05-stage-4-multi-agent-orchestration/01-c17-framework-evaluation/01-evaluation-dimensions.md`
- [ ] `05-stage-4-multi-agent-orchestration/01-c17-framework-evaluation/02-framework-comparison.md`
- [ ] `05-stage-4-multi-agent-orchestration/01-c17-framework-evaluation/03-escape-hatch-and-diy.md`
- [ ] `05-stage-4-multi-agent-orchestration/01-c17-framework-evaluation/04-cheatsheet-and-quiz.md`

### C18 · Agent 间通信与结果聚合 ⬜ 未开始

- [ ] `05-stage-4-multi-agent-orchestration/02-c18-agent-communication/01-structured-vs-natural-language.md`
- [ ] `05-stage-4-multi-agent-orchestration/02-c18-agent-communication/02-fanout-aggregation.md`
- [ ] `05-stage-4-multi-agent-orchestration/02-c18-agent-communication/03-avoid-telephone-game.md`
- [ ] `05-stage-4-multi-agent-orchestration/02-c18-agent-communication/04-stage-4-review-and-quiz.md`

---

## 阶段 5 · 工程化（观测 / 评测 / 成本 / 安全）

> 出口标准见 `06-stage-5-production-engineering/README.md`：全链路 trace + 回归评测集 + 成本看板 + 模型选型与路由策略。
> 已知捷径：5.1 可观测性建议提前到阶段 2 一起做，不要等阶段 5。

### C19 · 可观测性：trace 与日志规范 ⬜ 未开始

- [ ] `06-stage-5-production-engineering/00-c19-observability/01-why-agent-observability.md`
- [ ] `06-stage-5-production-engineering/00-c19-observability/02-trace-span-structure.md`
- [ ] `06-stage-5-production-engineering/00-c19-observability/03-logging-sampling.md`
- [ ] `06-stage-5-production-engineering/00-c19-observability/04-tooling-otel-langsmith.md`
- [ ] `06-stage-5-production-engineering/00-c19-observability/05-cheatsheet-and-quiz.md`

### C20 · 评测：评测集、LLM-as-judge、回归 ⬜ 未开始

- [ ] `06-stage-5-production-engineering/01-c20-evaluation/01-building-eval-set.md`
- [ ] `06-stage-5-production-engineering/01-c20-evaluation/02-llm-as-judge-design.md`
- [ ] `06-stage-5-production-engineering/01-c20-evaluation/03-judge-bias.md`
- [ ] `06-stage-5-production-engineering/01-c20-evaluation/04-eval-in-ci-regression.md`
- [ ] `06-stage-5-production-engineering/01-c20-evaluation/05-cheatsheet-and-quiz.md`

### C21 · 成本工程：预算、分级与告警 ⬜ 未开始

- [ ] `06-stage-5-production-engineering/02-c21-cost-engineering/01-unit-cost-accounting.md`
- [ ] `06-stage-5-production-engineering/02-c21-cost-engineering/02-budget-alerting.md`
- [ ] `06-stage-5-production-engineering/02-c21-cost-engineering/03-cache-hit-monitoring.md`
- [ ] `06-stage-5-production-engineering/02-c21-cost-engineering/04-model-tiering-and-quiz.md`

### C22 · 模型选型与路由 ⬜ 未开始

- [ ] `06-stage-5-production-engineering/03-c22-model-selection-routing/01-selection-dimensions.md`
- [ ] `06-stage-5-production-engineering/03-c22-model-selection-routing/02-dimension-tradeoffs.md`
- [ ] `06-stage-5-production-engineering/03-c22-model-selection-routing/03-tiered-routing.md`
- [ ] `06-stage-5-production-engineering/03-c22-model-selection-routing/04-long-context-open-source-and-quiz.md`

### C23 · 安全：权限、沙箱与人工确认 ⬜ 未开始

- [ ] `06-stage-5-production-engineering/04-c23-security/01-least-privilege.md`
- [ ] `06-stage-5-production-engineering/04-c23-security/02-sandbox-execution.md`
- [ ] `06-stage-5-production-engineering/04-c23-security/03-human-in-the-loop.md`
- [ ] `06-stage-5-production-engineering/04-c23-security/04-system-reliability-data-exfil.md`
- [ ] `06-stage-5-production-engineering/04-c23-security/05-cheatsheet-and-quiz.md`

---

## 阶段 6 · 实战项目

> 出口标准见 `07-stage-6-capstone/README.md`：3 个能放进作品集的项目，每个交付「仓库 + 评测结果 + 成本数据 + 设计复盘」。
> 已知捷径：**6.1（C24）在学完阶段 3 后就能开工**，不用等全部学完。
> 提醒：这是动手 lab，建议在电脑前边读边做，不适合通勤刷。

### C24 · 项目一：知识库问答 Agent（RAG + 引用） ⬜ 未开始

- [ ] `07-stage-6-capstone/00-c24-knowledge-base-qa/01-requirements-and-acceptance.md`
- [ ] `07-stage-6-capstone/00-c24-knowledge-base-qa/02-system-design.md`
- [ ] `07-stage-6-capstone/00-c24-knowledge-base-qa/03-implementation.md`
- [ ] `07-stage-6-capstone/00-c24-knowledge-base-qa/04-evaluation-and-cost.md`
- [ ] `07-stage-6-capstone/00-c24-knowledge-base-qa/05-retrospective-and-portfolio.md`

### C25 · 项目二：数据分析 Agent（代码执行 + 沙箱） ⬜ 未开始

- [ ] `07-stage-6-capstone/01-c25-data-analysis/01-requirements-and-acceptance.md`
- [ ] `07-stage-6-capstone/01-c25-data-analysis/02-system-design.md`
- [ ] `07-stage-6-capstone/01-c25-data-analysis/03-implementation.md`
- [ ] `07-stage-6-capstone/01-c25-data-analysis/04-evaluation-and-cost.md`
- [ ] `07-stage-6-capstone/01-c25-data-analysis/05-retrospective-and-portfolio.md`

### C26 · 项目三：自动化工作流 Agent（多步 + 长时任务） ⬜ 未开始

- [ ] `07-stage-6-capstone/02-c26-automation-workflow/01-requirements-and-acceptance.md`
- [ ] `07-stage-6-capstone/02-c26-automation-workflow/02-system-design.md`
- [ ] `07-stage-6-capstone/02-c26-automation-workflow/03-implementation.md`
- [ ] `07-stage-6-capstone/02-c26-automation-workflow/04-evaluation-and-cost.md`
- [ ] `07-stage-6-capstone/02-c26-automation-workflow/05-retrospective-and-portfolio.md`

---

## 待办 / 想深挖

> 累积 3 条「想深挖」就考虑新开一个专题目录。

- （待补充）

---

## 已补齐缺口（`08-review-course-health-check.md` 第二节）

体检报告列出的必修缺口与强化项，现已全部落地：

1. **MCP** → 阶段 2 的 C12（工具生态：MCP 与能力复用）
2. **模型选型与路由** → 阶段 5 的 C22
3. **长上下文 vs RAG 的取舍** → 阶段 3 的 C14-1 开篇
4. **上下文装配** → 阶段 1 的 C7-4；**人在回路（HITL）** → 阶段 5 的 C23-3
