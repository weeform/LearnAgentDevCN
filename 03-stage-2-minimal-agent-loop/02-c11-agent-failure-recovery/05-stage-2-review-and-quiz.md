# C11-5 · 阶段 2 总复习：速查、失败复盘与综合自测
> 阅读约 12 分钟。这一篇收尾阶段 2：把 C9–C11 压成能查、能交付、能自测的东西。

## 1. 阶段 2 知识地图

| 课 | 回答的问题 | 一句话结论 |
|---|---|---|
| C9 | 循环怎么转 | 模型输出 → 解析 → 执行 → 回填 → 再问，手写一遍就懂框架 |
| C10 | 工具怎么设计 | 调用成功率八成取决于工具描述，而非模型强弱 |
| C11 | 坏了怎么办 / 该不该用 | 反馈缺失是一切失效的温床；能写死就别用 Agent |

## 2. 最小 Agent 循环速查

```
for step in range(MAX_STEPS):
    resp = create(messages, tools, tool_choice="auto", temperature=0)
    msg = resp.choices[0].message
    messages.append(msg)
    if msg.tool_calls:
        for call in msg.tool_calls:
            result = execute(call.function.name, json.loads(call.function.arguments))
            messages.append({"role": "tool", "tool_call_id": call.id,
                             "content": json.dumps(result, ensure_ascii=False)})
        continue
    return msg.content
```

关键点：`tool_call_id` 一一对应、报错回传不吞、`temperature=0`、末步 `tool_choice="none"` 收口。

## 3. 阶段 2 交付物：失败复盘作业

阶段出口标准要求「一次失败复盘」。按这个模板做一次：

1. **场景**：让 `search_weather("不存在的城市")` 故意返回错误。
2. **观察**：模型下一轮做了什么？（换参数？换工具？直接编结果？）
3. **记录**：它自我修正成功了吗？失败时是「脑补」还是「诚实说不知道」？
4. **结论**：你的工具报错信息写得够不够「可行动」？不够就改。

这个作业的价值：**亲眼验证一次「错误回传 → 自我修正」的边界**，比读十遍 C11-2 都管用。

## 4. 综合自测（12 道）

> 覆盖 C9–C11。答对 8 道以上，可进入阶段 3。

1. 一轮工具调用，消息数组要经历哪几步？`tool` 消息是谁塞进去的？
2. 并行工具调用回填靠什么不串？流式 `arguments` 怎么处理？
3. ReAct 三段式是什么？为什么 Observation 决定循环质量？
4. `finish_reason=length` 时该怎么做？
5. 工具粒度「太细」和「太粗」各有什么代价？
6. 工具的 description 要覆盖哪三件事？
7. 为什么 JSON Schema 管不了参数语义？举例。
8. 工具报错时，「raise / 吞掉 / 回传」该选哪个？为什么？
9. 自我修正的边界在哪？反复修不好怎么办？
10. 死循环怎么检测？检测到之后做什么？
11. 单步超时应该「直接崩」还是「回传」？为什么？
12. 举两类「不该用 Agent」的场景，说明原因。

### 答案要点

1. system/user → assistant(tool_calls) → 执行 → tool(result) → 再请求；`tool` 消息是你的代码塞的。
2. 靠 `tool_call_id` 一一对应；流式 `arguments` 按 index 累加、`finish_reason=tool_calls` 后再 `json.loads`。
3. Thought/Action/Observation；Observation 是模型看世界的唯一窗口，含糊或报错不清会带偏下一步。
4. 输出被截断，报错并重试（提高 max_completion_tokens 或压缩输出），不硬解析。
5. 太细→轮次多、成本平方涨；太粗→参数爆炸、难选、难复用。
6. 能干什么、什么时候用、边界（不支持什么）。
7. schema 只保证类型和必填，管不了值合法与否；如 `age: 150`。
8. 回传；raise 会让循环崩，吞掉会让模型脑补，回传能让模型自我修正。
9. 反复 2–3 次修不好就说明模型不会了，应主动终止 + 降级（换模型/转人工/兜底）。
10. 记录最近 N 步动作签名，重复超阈值即打断 + 提示换思路，仍无进展则终止降级。
11. 回传；让模型决定重试/换工具/放弃，直接崩会中断任务且浪费已完成的步骤。
12. 确定性任务（用代码）、可枚举流程（用工作流）——任举两类并说明「不需要动态决策」。

## 5. 阶段 2 完成

到这里，你手写了一个能跑的 ReAct 循环，掌握了工具设计和失效恢复，也学会了「该不该用 Agent」的判断。

下一阶段（阶段 3 · 记忆与状态）要解决的是：**让 Agent 记住上下文之外的东西**——会话记忆怎么管理、长期记忆怎么检索、断点怎么续跑。
