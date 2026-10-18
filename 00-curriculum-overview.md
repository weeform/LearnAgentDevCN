# 00 · 学习路径总纲
> 这份文档是
> 总纲
> ：它不教知识，只回答三个问题 —— 课程地图长什么样、下一课是什么、为什么是这个顺序。每开一门新课，这里的课程地图会同步更新；**你个人学到哪了，记在 progress.md，不写在这里**。

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
- **阶段 1 · Prompt 与上下文工程**｜未开课 → 产出：一套可复用的 system prompt 模板 + 上下文裁剪策略
- **阶段 2 · Agent 最小闭环**｜未开课 → 产出：手写一个 100 行以内的 ReAct 循环
- **阶段 3 · 记忆与状态**｜未开课 → 产出：会话记忆 + 长期记忆检索跑通
- **阶段 4 · 多 Agent 与编排**｜未开课 → 产出：一个可拆任务、可并行的小型多 Agent 系统
- **阶段 5 · 工程化（观测 / 评测 / 成本 / 安全）**｜未开课 → 产出：全链路 trace + 一个回归评测集
- **阶段 6 · 实战项目**｜未开课 → 产出：3 个能放进作品集的项目

**阶段直达**（未开课的阶段点进去看大纲、计划课程与出口标准）：

- [阶段 0 · 模型调用与参数原理](01-stage-0-model-api/README.md) — 6 门课 / 27 篇
- [阶段 1 · Prompt 与上下文工程](02-stage-1-prompt-context.md) — 未开课：计划 3 门课
- [阶段 2 · Agent 最小闭环](03-stage-2-minimal-agent-loop.md) — 未开课：计划 3 门课
- [阶段 3 · 记忆与状态](04-stage-3-memory-state.md) — 未开课：计划 3 门课
- [阶段 4 · 多 Agent 与编排](05-stage-4-multi-agent-orchestration.md) — 未开课：计划 3 门课
- [阶段 5 · 工程化](06-stage-5-production-engineering.md) — 未开课：计划 4 门课（5.1 建议提前）
- [阶段 6 · 实战项目](07-stage-6-capstone.md) — 未开课：3 个项目

## 4. 课程地图

资料库里所有内容按「阶段 → 课程 → 单篇」三层放，**课程不会直接铺在根目录，都挂在所属阶段文件夹下**。已开 1 个阶段 / 6 门课 / 27 篇正文（另含 6 篇课程索引）。

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

目录规则：第一层是**阶段**（阶段 N · 主题），第二层是**课程**（CN · 主题），第三层是**单篇**（CN-M）。**C 编号全局连续，不按阶段重新从 1 开始**—— 阶段 1 从 C6 起，这样「C3」永远只指一门课，不会重名。

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

### 阶段 1 · Prompt 与上下文工程（下一步）

→ [进入阶段 1](02-stage-1-prompt-context.md) — 未开课，可先看大纲；这是下一个开课的阶段

- 1.1 system prompt 的结构化写法（角色 / 目标 / 约束 / 输出格式 / 示例）
- 1.2 少样本、思维链、自一致性：什么时候值得用，成本如何
- 1.3 结构化输出：JSON Schema 约束解码 vs 提示词约束
- 1.4 上下文管理：窗口、裁剪、压缩、摘要（缓存与 KV Cache 原理见 C2）
- 1.5 提示词注入与防御

### 阶段 2 · Agent 最小闭环

→ [进入阶段 2](03-stage-2-minimal-agent-loop.md) — 未开课

- 2.1 Function Calling / Tool Use 协议细节
- 2.2 ReAct 循环手写实现（Thought / Action / Observation）
- 2.3 工具设计原则：粒度、命名、描述、参数校验
- 2.4 失败恢复：重试、报错回传、最大步数、死循环检测
- 2.5 什么时候不该用 Agent

### 阶段 3 · 记忆与状态

→ [进入阶段 3](04-stage-3-memory-state.md) — 未开课

- 3.1 短期记忆：消息数组的管理与压缩
- 3.2 长期记忆：向量库、检索、重排
- 3.3 外部状态：任务状态机、断点续跑
- 3.4 上下文工程进阶：按需加载、子 Agent 隔离上下文

### 阶段 4 · 多 Agent 与编排

→ [进入阶段 4](05-stage-4-multi-agent-orchestration.md) — 未开课

- 4.1 单 Agent 够不够：拆分信号与代价
- 4.2 编排模式：路由 / 流水线 / 主从 / 黑板
- 4.3 框架横评：LangGraph、AutoGen、CrewAI、自研
- 4.4 Agent 间通信与结果聚合

### 阶段 5 · 工程化

→ [进入阶段 5](06-stage-5-production-engineering.md) — 未开课；5.1 建议提前到阶段 2

- 5.1 可观测性：trace、span、日志规范（建议提前到阶段 2）
- 5.2 评测：离线评测集、LLM-as-judge、回归
- 5.3 成本：token 预算、缓存、模型分级
- 5.4 稳定性：超时、限流、重试、幂等
- 5.5 安全：最小权限、沙箱、人工确认

### 阶段 6 · 实战项目

→ [进入阶段 6](07-stage-6-capstone.md) — 未开课；6.1 在阶段 3 后即可开工

- 6.1 个人知识库问答 Agent（RAG + 引用）
- 6.2 数据分析 Agent（代码执行 + 沙箱）
- 6.3 自动化工作流 Agent（多步 + 长时任务）

## 7. 贯穿全程的三条暗线

1. **成本意识**：每个设计决策都问一句「这会增加多少 token」。
2. **可复现性**：每个设计决策都问一句「同样的输入，明天还能得到同样的结果吗」。
3. **上下文预算**：每个设计决策都问一句「这段内容值得占用上下文吗？它稳定吗？」—— 只有稳定的前缀才能命中缓存，详见 C2-5。

## 8. 下一步

开阶段 1 · Prompt 与上下文工程，第一篇讲 system prompt 的结构化写法。

- 先补完阶段 0 → 建议顺序**C0**（原理，不懂就读）→ C3（成本）→ C4（流式/结构化）→ C5（稳定性）。C2 是理论课，未读完不影响后面几课，可随时回头补。
- 想直接推进 → 从阶段 1 开始，等开课。

---

v2 · 2026-09-09 更新：补入 C2 课程地图；移除 mermaid 图与四列表格，改为手机端友好的列表排版；新增第三条暗线「上下文预算」；标明阶段 1.4 与 C2 的衔接关系。

v3 · 2026-09-09 更新：阶段 0 补齐 C3（Token 与成本）、C4（流式与结构化输出）、C5（稳定性工程）三门共 12 篇；C5-4 提供参数速查大表与调用层自检清单。

v4 · 2026-09-09 更新：目录重排为「阶段 → 课程 → 单篇」三层，C1–C5 全部归入「阶段 0 · 模型调用与参数原理」文件夹（原链接均保持有效）；明确 C 编号全局连续，阶段 1 从 C6 起。

v5 · 2026-09-09 更新：建全全部 7 个阶段文件夹（阶段 0–6），每个阶段页含大纲、计划课程、出口标准与阶段间依赖；总纲新增「阶段直达」入口。

v6 · 2026-09-10 更新：新增**C0 · 大模型工作原理速成**（5 篇）作为 C1 / C2 的原理前置，解决「直接用 logits / Q K V 却从未解释」的问题；在 C2-1、C2-2、C1-1 开头加入前置提示与回顾；阶段 0 扩为 6 门课 / 27 篇。
