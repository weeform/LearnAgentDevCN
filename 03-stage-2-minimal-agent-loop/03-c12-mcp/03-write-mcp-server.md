# C12-3 · 怎么写：把工具包成 MCP server
> 阅读约 12 分钟，建议在电脑前跟着敲。目标：把自己写好的工具，打包成一个能被任何 Agent 客户端复用的 MCP server。

## 1. 为什么值得包成 MCP server

你在 C9 里写的 `search_weather`，只能你自己的 Agent 用。包成 MCP server 后，它变成：

> 一个标准的工具提供方，Claude Desktop、Cursor、任何支持 MCP 的 Agent 客户端，**都能直接接进来用**。

一次打包，处处复用——这正是 MCP 从 N×M 降到 N+M 的另一半。

## 2. 用 FastMCP 最小实现

官方 SDK 提供 `FastMCP`，把「定义工具」简化成「写一个带注解的函数」：

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")          # server 名，给客户端识别用

@mcp.tool()
def search_weather(city: str) -> dict:
    """查询指定城市当前天气，返回温度和天气状况。"""
    return {"city": city, "temp": 18, "condition": "晴"}

@mcp.tool()
def save_note(content: str) -> dict:
    """把一段文本保存为笔记。"""
    return {"status": "saved", "length": len(content)}

if __name__ == "__main__":
    mcp.run()                      # 默认走 stdio 传输
```

就这么短。`@mcp.tool()` 会自动把函数签名转成 `inputSchema`，把 docstring 转成 `description`。

## 3. 工具定义的三件套仍然关键

注意：FastMCP 帮你生成的是 `name`（函数名）、`description`（docstring）、`inputSchema`（类型注解）。**这三样，就是 C10 讲的工具设计三件套**——换个载体，原则不变：

- **name** 动宾结构、无歧义（`search_weather` 不是 `get_data`）。
- **description** 写清能干什么、什么时候用、边界——MCP server 的 description 是**写给所有潜在使用者**看的，更要写清楚。
- **参数** 用类型注解 + 文档说明，能枚举就枚举。

一个写烂 description 的 MCP server，接进来之后模型照样乱调——工具设计质量（C10）在这里原封不动地生效。

## 4. 传输与部署

- **本地用**：`mcp.run()` 默认 stdio，客户端把它当子进程拉起即可。
- **共享用**：切到 Streamable HTTP——`mcp.run(transport="streamable-http")`，起一个 HTTP 服务，配鉴权/网关，别人通过 URL 接入。

选型判据和 C12-1 一致：本机自己用走 stdio，跨机器共享走 HTTP。

## 5. 与 C9/C10 串起来

把整条链理顺：

- **C9**：模型怎么表达「我要调工具」→ function calling。
- **C10**：工具本身怎么设计 → 粒度、命名、描述、校验。
- **C12**：工具怎么**复用和分发** → 包成 MCP server，跨客户端复用。

三者不冲突，是「调用 → 设计 → 复用」的递进。你写的工具，既可以直接给模型用（C9），也可以包成 MCP server 给别人用（C12）——底层是同一套工具设计原则（C10）。

## 6. 小结

- FastMCP 让「定义工具」=「写带注解的函数」，自动生成三件套。
- MCP server 的 name/description/参数，就是 C10 的工具设计原则换了个载体。
- 本地 stdio、共享 HTTP，选型按「本机还是跨机器」。
- 一次打包，处处复用，是 MCP 的另一半价值。

## 下一篇

C12-4 讲 MCP 的特有安全风险——投毒的工具描述、间接注入、过度授权、仿冒 server——并做阶段 2 的全段总复习。
