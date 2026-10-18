# C9-3 · 手写 100 行 ReAct 循环
> 阅读约 15 分钟，建议在电脑前跟着敲。目标：写出一个能跑、带终止条件与错误处理的最小 Agent。

## 1. 完整代码

下面的代码约 95 行，跑通 3 个工具（查询 / 写入 / 计算）。协议用 OpenAI 兼容格式，换 `base_url` 即可接 DeepSeek、通义等 OpenAI 兼容服务；**Claude 走 Anthropic 协议（`/v1/messages`、`tool_result`、无 `role=tool`），不能只换 base_url，需单独适配（见 C9-1 第 5 节）**。

```python
import json
from openai import OpenAI

client = OpenAI()   # 设 base_url / api_key 可接 DeepSeek、通义等兼容服务

SYSTEM_PROMPT = """你是一个能用工具完成任务的助手。
规则：先判断当前状态，需要信息就调用工具；工具全部完成后直接给最终答案，不要再调工具。"""

MAX_STEPS = 8       # 最大步数，死循环保险

TOOLS = [
    {"type": "function", "function": {
        "name": "search_weather",
        "description": "查询指定城市当前天气，返回温度和天气状况。",
        "parameters": {"type": "object",
            "properties": {"city": {"type": "string", "description": "城市名"}},
            "required": ["city"]}}},
    {"type": "function", "function": {
        "name": "save_note",
        "description": "把一段文本保存为笔记，返回保存状态。",
        "parameters": {"type": "object",
            "properties": {"content": {"type": "string", "description": "笔记内容"}},
            "required": ["content"]}}},
    {"type": "function", "function": {
        "name": "calculate",
        "description": "计算数学表达式，如 3*7+2，返回结果。",
        "parameters": {"type": "object",
            "properties": {"expression": {"type": "string", "description": "表达式"}},
            "required": ["expression"]}}},
]


def search_weather(city: str):
    return {"city": city, "temp": 18, "condition": "晴"}


def save_note(content: str):
    # 生产里应写文件/库；这里演示
    return {"status": "saved", "length": len(content)}


def calculate(expression: str):
    # 演示用 eval；生产务必换成受限求值（见正文第 3 节）
    return {"expression": expression, "result": eval(expression)}


def execute(name: str, args: dict):
    funcs = {"search_weather": search_weather,
             "save_note": save_note,
             "calculate": calculate}
    try:
        return funcs[name](**args)
    except Exception as e:
        return {"error": str(e)}   # 报错回传，让模型自我修正


def run_agent(user_input: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]
    for step in range(MAX_STEPS):
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0,
            max_completion_tokens=2048,   # 防输出被截断（见 C1-3）
        )
        msg = resp.choices[0].message
        messages.append(msg)

        if msg.tool_calls:                    # 模型要调工具
            for call in msg.tool_calls:
                try:
                    args = json.loads(call.function.arguments)
                    result = execute(call.function.name, args)
                except json.JSONDecodeError:
                    result = {"error": f"工具参数不是合法 JSON：{call.function.arguments[:50]}…"}
                messages.append({"role": "tool",
                                 "tool_call_id": call.id,
                                 "content": json.dumps(result, ensure_ascii=False)})
            continue                          # 结果喂回模型，继续循环

        if resp.choices[0].finish_reason == "length":
            raise RuntimeError("输出被截断，增大 max_completion_tokens 后重试")
        return msg.content                     # finish_reason == "stop"：最终答案

    return "达到最大步数，任务未完成。"


print(run_agent("帮我查北京天气，算一下 18*3，并把结果记下来"))
```

## 2. 逐段拆解

| 代码块 | 作用 | 对应前文 |
|---|---|---|
| `SYSTEM_PROMPT` | 明确「先判断、后调工具、完成即止」 | C6-1 的目标/约束段 |
| `MAX_STEPS` | 死循环保险，到顶强制停 | C9-4 |
| `TOOLS` | 3 个工具定义，参数带 description | C1-4 / C10 |
| `execute()` | 统一执行 + **报错回传** | C11-2 |
| `messages.append(msg)` | 把 assistant 的 tool_calls 存进历史 | C9-1 |
| `tool_call_id` | 回填的钥匙，一一对应 | C9-1 |
| `msg.tool_calls` 分支 | `有`=继续循环，`无`=最终答案 | C9-4 |
| `finish_reason=="length"` | 截断防护，绝不硬解析 | C9-4 |

> 说明：这里用 `msg.tool_calls` 的真假做「继续 / 结束」分支，是教学简化；严格做法应看 `finish_reason`（见 C9-4）。`messages.append(msg)` 直接把 SDK 的消息对象混塞 dict 是官方示例做法，可跑通；更严格的做法见 C9-1。

## 3. 三个必须知道的坑

1. **`eval` 是演示，不是实现**。`calculate` 用 `eval` 会因为「参数里藏了 `__import__('os')...`」而变成代码执行漏洞。生产里要换成**受限求值**，例如用 `ast` 白名单只放行四则运算：

```python
import ast, operator

_ALLOWED = {ast.Add: operator.add, ast.Sub: operator.sub,
            ast.Mult: operator.mul, ast.Div: operator.truediv}

def safe_calc(expr: str):
    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED:
            return _ALLOWED[type(node.op)](visit(node.left), visit(node.right))
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("不支持的表达式")
    return visit(ast.parse(expr, mode="eval"))
```

用 `safe_calc` 替换 `calculate` 里的 `eval` 即可。这同时是 C8 注入防御和 C10 参数校验的交叉点。

2. **报错要回传，不要吞掉**。`execute()` 里 `except` 返回 `{"error": ...}` 而不是 `raise`，是为了让模型「看到失败、自己修正」（详见 C11-2）。吞掉报错，模型会以为成功了，继续在错误基础上胡编。

3. **`temperature=0` + 单步上限**。Agent 循环要的是「可复现」（三条暗线之二），采样参数走稳定档（见 C1-2）；`max_completion_tokens` 兜住输出长度（见 C1-3）。

## 4. 一个最小 trace

阶段出口标准要求「能回看一次任务的完整步骤」。最朴素的实现是**在循环里打日志**：

```python
        print(f"[step {step}] tool_calls: {msg.tool_calls}")
        ...
        print(f"[step {step}] result: {result}")
```

完整的 trace / span 体系留到阶段 5，但**现在就要养成记录每一步的习惯**——没有 trace，Agent 一旦跑偏你只能干瞪眼。

## 5. 小结

- 约 95 行：消息数组 + 工具定义 + 执行器 + 循环 + 终止条件。
- 三个坑：eval 有注入风险（换 ast 受限求值）、报错要回传、采样走稳定档 + 限长。
- 现在就开始记录每一步，别等阶段 5 补 trace。

## 下一篇

C9-4 专门讲「让循环可靠停下来」：finish_reason 分支、最大步数怎么定、停止信号怎么设计。
