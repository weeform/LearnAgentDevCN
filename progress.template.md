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

---

## 后续阶段（正文尚未整理）

| 阶段 | 状态 | 计划产出 |
|---|---|---|
| `04-stage-3-memory-state.md` | ⬜ 未开始 | 会话记忆 + 长期记忆检索跑通 |
| `05-stage-4-multi-agent-orchestration.md` | ⬜ 未开始 | 一个可拆任务、可并行的小型多 Agent 系统 |
| `06-stage-5-production-engineering.md` | ⬜ 未开始 | 全链路 trace + 一个回归评测集 |
| `07-stage-6-capstone.md` | ⬜ 未开始 | 3 个能放进作品集的项目 |

已知捷径（`00-curriculum-overview.md` 第 5 节）：

- 阶段 2 一动手就要有 trace，**5.1 可观测性提前到阶段 2 一起做**，不要等阶段 5。
- 阶段 6 的项目不用等全部学完：**6.1 在学完阶段 3 后就能开工**。

---

## 待办 / 想深挖

> 累积 3 条「想深挖」就考虑新开一个专题目录。

- （待补充）

---

## 已知缺口（`08-review-course-health-check.md` 第二节）

按严重程度排序，开新课时优先补这些：

1. **MCP（Model Context Protocol）** — 完全缺失，最严重缺口
2. **模型选型与路由** — 薄弱
3. **长上下文 vs RAG 的取舍** — 缺失
4. 应强化：上下文装配（Context Assembly）、人在回路（HITL）
