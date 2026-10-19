# C15-2 · 断点续跑：checkpoint 与恢复
> 阅读约 12 分钟。目标：让任务在进程被杀后，能从上次状态继续，而不是从头再来。

## 1. checkpoint 是什么

checkpoint 就是**在关键步骤保存一份「完整状态快照」**，包含：当前状态机状态、已完成的步骤、中间产物引用。恢复时读这份快照，接着往下走。

```python
import json, os
from typing import Optional

CHECKPOINT = "checkpoint.json"

def save_checkpoint(state: dict):
    # 先写临时文件再原子替换，避免写入中途被杀留下半截 JSON
    tmp = CHECKPOINT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, CHECKPOINT)

def load_checkpoint() -> Optional[dict]:
    if os.path.exists(CHECKPOINT):
        with open(CHECKPOINT, encoding="utf-8") as f:
            return json.load(f)
    return None
```

## 2. 恢复的三步

启动时先走一遍：

1. **读 checkpoint**：存在且状态是 `running`/`paused`，说明上次没跑完。
2. **从 `current_step` 继续**：跳过 `steps_done` 里已完成的步骤。
3. **读回中间产物**：`artifacts` 里的落盘文件直接复用，不重算。

伪代码：

```python
state = load_checkpoint() or {"status": "pending", "current_step": None,
                              "steps_done": [], "artifacts": {}}
for step in plan:
    if step in state["steps_done"]:
        continue                       # 已完成的跳过
    state["current_step"] = step       # 先标记「正在做这步」
    save_checkpoint(state)             # 执行前打点（非幂等步骤尤其重要）
    result = run_step(step)
    state["artifacts"][step] = save_artifact(result)   # 中间产物落盘
    state["steps_done"].append(step)   # 执行后打「已完成」点
    state["current_step"] = None
    save_checkpoint(state)             # 每步结束都打点
```

## 3. 最容易翻车的点：幂等

恢复意味着「某个步骤可能被执行两次」（第一次执行完没来得及打点就挂了）。所以：

> 每个工具/步骤要么**幂等**（重复执行结果一致、无副作用），要么**打点要足够及时且可重试**。

- **幂等操作**（读数据、算结果）：重复执行没问题。
- **非幂等操作**（发邮件、扣款、写数据库）：用「执行前打 intent 标记 + 执行后打 done 标记」——恢复时若只有 intent 没有 done，说明上次执行结果未知，需人工确认或走幂等键去重，而不是盲目重跑。

一句话：**「能不能安全地重跑一遍」，决定你的断点续跑是救星还是灾难**。这也呼应 C5-2 讲过的幂等思想。

## 4. 中间产物要落盘

断点续跑能省时间的真正来源，不是「记住跑到第几步」，而是「**已经算出来的中间结果不用重算**」：

> 每步的产物都落盘存引用（见 C13-3），恢复时直接从盘上读，而不是重新跑那一步。

所以 `artifacts` 字段不是可有可无的装饰，它是断点续跑「省时」的核心。

## 5. 打点时机

- **每步结束都打点**：粒度细，恢复时重跑得少。
- 太频繁会有 IO 开销，但学习阶段这个开销可忽略。
- 关键：**有副作用的操作要「执行前 intent + 执行后 done」两点**——只打「之后」的一点，仍会留下「执行成功但没来得及打点」的崩溃窗口（见第 3 节）。

## 6. 小结

- checkpoint = 关键步骤的完整状态快照。
- 恢复三步：读快照 → 从 current_step 继续 → 复用落盘产物。
- 幂等是断点续跑的安全前提；中间产物落盘是「省时」的关键；非幂等步骤「执行前 intent + 执行后 done」打点。

## 下一篇

C15-3 讲上下文工程的进阶手法——**按需加载**（先给目录，要用再取）与**上下文分区**（稳定前缀 / 动态中段 / 最新尾部）。
