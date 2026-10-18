# 大模型与 Agent 开发学习

一套自学的 **Agent 开发课程库**，按 **阶段 → 课程 → 单篇** 三层组织。当前已整理阶段 0–2 共 54 篇正文（另含 12 篇课程索引）。
目标：**系统掌握 Agent 开发**；大模型理论只学「够用」的那一层。
主场景：手机端通勤阅读，每篇 8–15 分钟。

> 本仓库已全部本地化：文档内的原资料库链接**已全部改写为本地相对路径**，离线可读、可被 Agent 直接检索引用。

---

## 开始使用

```bash
git clone https://github.com/weeform/LearnAgentDevCN.git
cd LearnAgentDevCN

# 生成属于你自己的进度文件（幂等，重复跑不会覆盖记录）
python scripts/init-progress.py
```

读法顺序：**先 `00 · 学习路径总纲`，再按阶段推进**。每篇结尾都有「下一篇」或「自测」，读完立刻知道接哪篇。

---

## 进度怎么记（多人共用同一份课程，各记各的）

`progress.md` 是**你自己的**勾选记录，已被 `.gitignore` 排除，**不会上传**，也不会和别人冲突。

| 文件 | 入库？ | 作用 |
|---|---|---|
| `progress.template.md` | ✅ 入库 | 54 篇正文的空勾选骨架，所有人共享同一份 |
| `progress.md` | ❌ 本地私有 | 你的真实进度，来自模板的一次性复制 |

**第一次一定要跑 `scripts/init-progress.py`**——clone 下来是没有 `progress.md` 的，
自己新建空文件会丢掉模板里完整的篇目清单。换机器或重新 clone，再跑一次即可。

之后读 / 改进度都针对 `progress.md`：

- 读完一篇勾一行，并顺手记一条：读完了 / 卡在哪 / 想深挖什么
- 累积 3 条「想深挖」就考虑新开一个专题文件夹

> 有 AI 助手（Claude Code / CodeBuddy / WorkBuddy 等）帮忙的话，`AGENTS.md` 第 5 节写了硬性规则：
> 它在动进度前会先检查并完成这步自举。

---

## 目录树

```
LearnAgentDevCN
├── 00-curriculum-overview.md        学习路径总纲（从这里开始看）
├── 01-stage-0-model-api/            阶段 0 · 模型调用与参数原理
│   ├── 00-c0-llm-fundamentals/      C0 · 大模型工作原理速成（前置课）
│   ├── 01-c1-call-parameters/       C1 · 大模型调用参数与原理
│   ├── 02-c2-kv-cache/              C2 · KV Cache 机制与上下文复用
│   ├── 03-c3-tokenization-cost/     C3 · Token、分词与成本模型
│   ├── 04-c4-streaming-structured-output/   C4 · 流式输出与结构化输出
│   └── 05-c5-reliability/           C5 · 稳定性：错误、重试、限流与降级
├── 02-stage-1-prompt-context/       阶段 1 · Prompt 与上下文工程
│   ├── 00-c6-system-prompt-patterns/   C6 · System Prompt 工程与提示词模式
│   ├── 01-c7-context-management/       C7 · 上下文管理与压缩
│   └── 02-c8-prompt-security/          C8 · 提示词安全与注入防御
├── 03-stage-2-minimal-agent-loop/   阶段 2 · Agent 最小闭环
│   ├── 00-c9-tool-calling-react/       C9 · 工具调用协议与 ReAct 手写
│   ├── 01-c10-tool-design/             C10 · 工具设计：粒度、描述与参数校验
│   └── 02-c11-agent-failure-recovery/  C11 · Agent 失效模式与恢复
├── 04…07-stage-*.md                 阶段 3–6（仅大纲）
├── 08-review-course-health-check.md 全课程体检
├── progress.template.md             进度模板
├── scripts/init-progress.py         进度自举脚本
└── AGENTS.md                        给 AI 助手的协作规则
```

一门课 = 一个文件夹，编号 `Cn`；课内文档编号 `Cn-k`。

---

## 隐私边界

以下内容**不会**进版本库，可以放心在里面写个人笔记：

- `progress.md` —— 你的勾选与备注
- `.workbuddy/memory/` —— AI 助手的本地项目记忆
- `.tmp_probe/` —— 导出期的临时脚本与缓存

反过来，`README.md`、各阶段正文、`progress.template.md` 是共享内容，**别写本机路径、Token、密钥**。

---

## 贡献声明

- 欢迎 Issue / PR：勘误、补充我不到的知识点、把某篇讲得更明白。
- 改动建议：**新主题 = 新文件夹**，不往已有文件夹里塞散文档；一个主题超过 3 篇必须建子文件夹。
- 编号与命名规则见 `AGENTS.md` 第 3 节，**不要擅自重排编号**；结构调整先在 Issue 里提方案。
- 新增篇目后，同步更新 `00-curriculum-overview.md` 的课程地图、`progress.template.md`、本级 `README.md`。

## 许可证

MIT License —— 见 [LICENSE](./LICENSE)。自由使用、修改、转载、商用均可，保留版权声明即可。
