# C12-2 · 怎么用：把现成 MCP server 接进 Agent
> 阅读约 12 分钟，建议在电脑前跟着敲。目标：把别人打包好的 MCP server，变成你自己 Agent 里的工具。

## 1. 四步思路

接入一个现成 MCP server，本质是把「MCP 工具」翻译成「function calling 工具」：

```
连上 server → list_tools 拉工具清单 → 转成 function calling 的 tools 定义
           → 模型决定调用后，用 call_tool 执行 → 结果喂回模型
```

翻译这步是核心：MCP 工具自带 `name` / `description` / `inputSchema`，它们**正好对应** function calling 工具定义的三个字段（见 C1-4）——注意 `inputSchema` 对应的是 `parameters`，字段名不同、语义一致。所以转换几乎是机械的。

## 2. 一个最小示例（Python SDK）

接一个本地文件系统 MCP server（`@modelcontextprotocol/server-filesystem`），把它暴露的文件工具接进 Agent。示例需要 Node.js 环境（`npx` 启动 server；Windows 下部分环境要写 `npx.cmd`），`/tmp/a.txt` 请换成你的实际路径：

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # 1. 描述要启动的 server（这里是 npx 启动的本地进程）
    server = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
    )
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 2. 拉工具清单，转成 function calling 的 tools 定义
            tools = await session.list_tools()
            fc_tools = [
                {"type": "function", "function": {
                    "name": t.name,
                    "description": t.description or "",
                    "parameters": t.inputSchema,
                }}
                for t in tools.tools
            ]
            # 现在 fc_tools 可以直接放进 chat.completions 的 tools= 参数

            # 3. 模型决定调用某个工具后，执行它
            result = await session.call_tool("read_file", {"path": "/tmp/a.txt"})
            # CallToolResult.content 是 content block 列表，文本取 .text
            print(result.content[0].text)

asyncio.run(main())
```

## 3. 三个关键点

1. **`list_tools()` 返回的工具就是「现成的工具定义」**。`name` / `description` / `inputSchema` 三件套直接对应 function calling 的字段，不用自己重写。工具描述质量（C10）同样适用——server 作者写得烂，你接进来模型照样乱调。

2. **MCP 工具和原生 function calling 工具可以混用**。你可以一半工具来自自己写的函数，一半来自接进来的 MCP server，只要把它们都塞进同一个 `tools` 数组、用同一个执行器分发即可。判断「该调哪个」交给模型。

3. **`inputSchema` 可能很复杂**。有些 server 的工具参数嵌套很深，转换时要留意 `inputSchema` 是否符合目标模型的 schema 支持范围（见 C4-3 的规模上限）；必要时做一层「白名单工具 + 精简 schema」的包装。

## 4. 执行层的统一

接 MCP 后，你的 `execute()` 要能同时处理两类工具：

```python
async def execute(name, args):
    if name in my_native_tools:          # 自己写的函数
        return my_native_tools[name](**args)
    if name in mcp_tools:                 # MCP 暴露的工具
        return await session.call_tool(name, args)
    return {"error": f"未知工具：{name}"}
```

不管工具来自哪里，**对模型来说都是「一个能调用的工具」**——这就是 MCP 的意义：接入对模型透明。

> 注意：按 `name` 分发隐含「工具名全局唯一」的前提。接多个 server、或混用原生工具时若出现同名冲突，用命名空间前缀（如 `fs.read_file`）区分。

## 5. 小结

- 四步：连 server → list_tools → 转 function calling → call_tool。
- `name/description/inputSchema` 三件套直接对应 function calling，转换近乎机械。
- MCP 工具与原生工具可混用，执行层统一分发。
- 工具描述质量（C10）对 MCP 工具同样适用。

## 下一篇

C12-3 反过来：怎么把自己的工具包成 MCP server，让别人（和所有主流 Agent 客户端）都能复用。
