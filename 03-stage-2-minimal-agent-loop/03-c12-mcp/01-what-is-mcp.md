# C12-1 · MCP 是什么、解决什么问题
> 阅读约 10 分钟。目标：理解 MCP 的定位、架构和传输，知道它和「自己写 function calling」是什么关系。

## 1. 从 N×M 集成问题说起

假设你有 5 个 Agent 客户端（Claude Desktop、Cursor、自己的 App……），要接 6 个工具源（文件系统、数据库、GitHub、天气 API……）。

**没有标准协议**：每个客户端 × 每个工具源，都要各自写一套适配 → 5 × 6 = 30 份适配代码。每加一个新工具源，所有客户端都要跟着改。

**有了 MCP**：工具源按一个标准协议暴露能力，客户端按同一个协议接入 → 5 + 6 = 11 份工作。加新工具源，所有客户端零改动就能用。

这就是 MCP（Model Context Protocol）要解决的问题：**把「模型 ↔ 工具/数据」的集成，从 N×M 变成 N+M。**

## 2. MCP 的定位：与 function calling 互补的「生态层」

先厘清它和前面课程的关系：

- **function calling**（工具定义见 C1-4，调用协议见 C9）是「模型如何表达调用意图」——单次请求里的协议。
- **MCP** 是「工具如何被标准地暴露和发现」——工具生态的协议。

换句话说，MCP 不替代 function calling，而是**与它互补**：一个 MCP server 暴露的工具，最终还是要翻译成 function calling 的工具定义喂给模型（名字、描述、参数三件套，见 C1-4）。MCP 的价值在**标准化接入**，不在替代底层调用。

## 3. 三个角色：Host / Client / Server

| 角色 | 是谁 | 职责 |
|---|---|---|
| Host | 你的应用（Claude Desktop、Cursor、自定义 Agent） | 发起交互，最终消费工具结果 |
| Client | Host 内部的一个协议连接 | 与单个 Server 建立 1:1 连接 |
| Server | 暴露能力的进程/服务 | 提供 tools / resources / prompts |

一个 Host 可以同时连多个 Server（每个 Server 一个 Client），把多个工具源的能力聚合起来。

打个比方：Host 是你的应用，Client 是它连某个 Server 的一根「专属连接」。分成两层，是为了让一个 Host 能**并行连多个 Server 而不互相串线**——每个 Server 对应一个独立的 Client。

## 4. 两种传输方式

| 传输 | 适用 | 特点 |
|---|---|---|
| **STDIO** | 本地 | Server 作为子进程启动，走标准输入输出；简单、无网络暴露 |
| **Streamable HTTP** | 远程 | Server 作为 HTTP 服务；可跨机器 |

选哪个的判据：工具源在本机就跑 STDIO；要共享给他人或跨机器，就上 HTTP。远程部署时通常要**自行加鉴权/网关**——鉴权是部署要求，不是传输本身的属性。

## 5. Server 暴露的三类能力

一个 MCP server 可以暴露三种东西：

- **tools**：可调用的函数（对应 function calling 的工具），由**模型决定何时调用**。
- **resources**：由**应用**（而非模型）决定读取、作为上下文注入模型的数据/内容，只读；要改数据应走 tools。
- **prompts**：可复用的提示模板（预置的提示词片段）。

对 Agent 开发者来说，**最常用的是 tools**；resources 和 prompts 是加分项。

## 6. 一个关键事实：MCP 已经中立化

> 版本说明：MCP 当前最新修订版是 **2026-07-28**（上一版 2025-11-25；2026-07-28 把 2025-11-25 及更早统称 legacy）。这一版的核心变化是**协议级无状态化**：去掉 Streamable HTTP 的会话与 `Mcp-Session-Id`、去掉 `initialize` / `notifications/initialized` 握手，版本与客户端能力改为每个请求带在 `_meta` 里，并新增 `server/discover` 让客户端先探版本。
>
> 对读本篇的影响只有一条：**跟随官方 SDK 稳定版即可**。SDK 同时兼容 legacy 与新代（dual-era）server，会自行选择握手方式；存量 server 绝大多数仍是 legacy，所以本篇示例保留了 `session.initialize()`，不必自己判断走哪一代。

MCP 由 Anthropic 于 2024-11 发布，**2025-12 已捐给 Linux 基金会旗下的 Agentic AI Foundation**（联合创始方含 Anthropic、OpenAI、Block，AWS/Google/Microsoft 等均为成员）。这意味着它已从「某家的协议」变成**中立的基础设施标准**，OpenAI、Google Gemini、Microsoft Copilot、Cursor、VS Code 均原生支持。

对开发者的直接含义：

> **现在接工具的第一选择，往往不是自己写 function calling，而是接现成的 MCP server；把自己的能力包成 MCP server，则能被所有主流 Agent 客户端复用。**

## 7. 小结

- MCP 把「模型↔工具」的集成从 N×M 降到 N+M。
- 它站在 function calling 之上，是「工具生态」的标准，不替代底层调用。
- 三角色（Host/Client/Server）、两种传输（STDIO/HTTP）、三类能力（tools/resources/prompts）。
- 已中立化，主流客户端原生支持。

## 思考题

> 先自己答，再展开参考思路。这三问不考记忆，考的是你能不能把它用在自己的项目上。

1. N×M 集成问题具体指什么？MCP 把它降成 N+M 的机制是什么？
2. MCP 与 function calling 是什么关系？说「MCP 替代 function calling」错在哪？
3. tools / resources / prompts 三类能力，各对应什么使用场景？

<details>
<summary>参考思路</summary>

1. N 个客户端要接 M 个工具就要写 N×M 份适配；有了统一协议，每个客户端实现一次、每个工具实现一次，变成 N+M。
2. MCP 站在 function calling 之上：底层仍然是模型输出 tool_calls、你执行。MCP 标准化的是「工具从哪来、怎么发现、怎么调」，不是替代调用机制。
3. tools 是可执行动作；resources 是可读的数据/文件（更像上下文注入）；prompts 是可复用的提示模板。

</details>

## 下一篇

C12-2 讲怎么用：把一个现成的 MCP server 接进你自己的 Agent，让它的工具变成你能调用的工具。
