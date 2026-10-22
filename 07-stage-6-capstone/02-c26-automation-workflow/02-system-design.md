# C26-2 · 系统设计
> 建议在电脑前边读边做。阅读约 14 分钟。目标：把「续跑、熔断、等确认、回滚」四件事，在设计层先想清楚，再动手写代码。

## 1. 状态机：任务状态与合法迁移

状态机是长时任务的骨架（见 C15-1 第 2 节）。本项目给「批量处理反馈」设计下面这些状态：

```
pending → running → awaiting_approval → applying → done
              │            │              │
              ├→ failed（可重试）
              ├→ failed_over_budget（超预算，熔断）
              └→ rolled_back（方向错了，已回滚）
```

| 状态 | 含义 | 能否恢复 |
|---|---|---|
| `pending` | 还没开始 | 可直接跑 |
| `running` | 正在执行某一步 | 进程挂后从 checkpoint 续跑 |
| `awaiting_approval` | 停在敏感步骤前等人确认 | 人 approve / reject |
| `applying` | 正在执行有副作用的写操作 | 需幂等/补偿保护 |
| `done` / `failed` / `failed_over_budget` / `rolled_back` | 终态 | 不再自动迁移 |

两条设计原则：

1. **状态要显式、可判终态**。任何时刻读状态，能立刻回答「它现在在哪、下一步去哪、还能不能继续」。模糊状态（如「差不多好了」）是灾难。
2. **迁移要合法**。`done` 之后不能再 `running`，`awaiting_approval` 只有人点头才能进 `applying`。用代码里一个 `ALLOWED` 字典约束，别靠自觉。

```python
ALLOWED = {
    "pending": {"running"},
    "running": {"awaiting_approval", "applying", "done", "failed", "failed_over_budget"},
    "awaiting_approval": {"applying", "rolled_back", "failed"},   # approve→applying；reject→rolled_back
    "applying": {"done", "rolled_back", "failed"},
}
def transition(state, to):
    assert to in ALLOWED[state["status"]], f"非法迁移 {state['status']} -> {to}"
    state["status"] = to
```

## 2. checkpoint：什么时候打点、存什么

checkpoint 是「完整状态快照」（见 C15-2 第 1 节）。本项目的打点时机，比 C15-2 的「每步结束」再细化一档：

- **每个批次处理完**打一次点：粒度 = 一批（20 条）。批太小，IO 频繁；批太大，挂了重跑得多。
- **副作用步骤执行前，打 intent 点**（`status=applying`，记下幂等键），执行后打 done 点。这是 C15-2 第 3 节讲的「执行前 intent + 执行后 done」，恢复时能分辨「结果未知」的步骤。

存什么：不是存消息数组，而是存**最小真相**——`status / current_step / progress / budget / artifacts / pending_approval`。消息数组可以靠 checkpoint 重建，反过来不行。

> 真相源是 checkpoint，消息是派生的视图（见 C15-1 第 4 节）。恢复时从 checkpoint 重建上下文，而不是把整个聊天记录存进 checkpoint。

## 3. 人工介入点：哪些步骤要暂停

不是所有步骤都要人确认——确认太频繁，长任务会变成「人肉陪跑」。判断标准一句话：

> **「这一步做错了，恢复成本是否高到需要人兜底」。** 恢复成本高的（不可逆、影响面大、涉及真金白银或对外可见），设确认点；可逆、可重跑、影响小的，让 Agent 自己跑。

本项目只设一个确认点：**「批量写入系统」之前**。写库不可逆（或回滚成本高），一旦方向错了，500 条脏数据要一条条救。而「拉数据、分类、抽取」错了可以重跑，不设卡。

确认点要落到状态机：跑到 apply 前，`transition(awaiting_approval)`，把「要做什么」摘要写进 `pending_approval`，然后**进程可以安全退出**，人回来 approve 再恢复。人机分离是长时任务的关键——确认点不能要求人守着屏幕（呼应 C23-3 的人工确认思路）。

## 4. 幂等与补偿

断点续跑意味着「某一步可能被执行两次」。分两类处理（见 C15-2 第 3 节）：

- **幂等操作**（读、分类、抽取）：重复执行结果一致，直接重跑无害。
- **非幂等操作**（写库、发通知）：靠**幂等键**去重——每个批次一个唯一键，执行时「键不存在才写」，重跑时键已存在则跳过。

```python
def apply_batch(batch_id, rows):
    if idempotency_seen(batch_id):      # 幂等键已存在 → 上次其实成功了
        return "already_done"
    mark_intent(batch_id)               # 先标记 intent（执行前）
    write_rows(rows)                    # 执行
    mark_done(batch_id)                 # 标记 done
```

**补偿**处理「执行到一半失败」：如果写库写了一半挂了，恢复时不能盲目重跑（会重复插入）。做法是：写库本身用「事务 + 幂等键」，要么全成要么全不成；已经写进去但后续步骤失败的，靠**回滚脚本**按幂等键精确删除该批，而不是回滚整个任务。

> 幂等是「重跑无害」的保证；补偿是「重跑有害时，把害处精确撤销」的手段。两者一起才兜得住「部分失败」。

## 5. 成本上限与预算熔断

长任务的 token 会滚雪球：每轮调用都把历史重发一遍，越到后面越贵（见 C21-2 的成本归因）。所以任务必须带**预算上限**，且熔断要在「花钱之前」判断：

```python
def check_budget(state, next_call_est):
    if state["budget"]["spent_usd"] + next_call_est > state["budget"]["cap_usd"]:
        transition(state, "failed_over_budget")
        raise BudgetExceeded(state["budget"])
```

三点：

1. 每次模型调用前估算下一跳成本（token 估 × 单价），花超了就停，**不是花完了才停**。
2. 熔断是终态，不是「暂停一下继续」——继续只会更贵。
3. 预算花到哪了要可查（每个 span 记 token，见 C19-2），否则熔断了也不知道钱烧在哪。

## 6. 「方向错了」的回滚策略

这是本项目比 C15 多出来的难点：**续跑只能「接着往下」，但长任务可能在半路发现「一开始就理解错了，前面白做甚至做错了」**。

回滚分三档，由轻到重：

| 档位 | 场景 | 做法 |
|---|---|---|
| 未产生副作用 | 还没到 apply 就发现错了 | 直接置 `rolled_back`，清掉中间产物 |
| 已部分写库 | apply 进行到一半 | 按幂等键精确删回（补偿脚本） |
| 已全部写库且对外可见 | 已经全写完才发现错 | 记「反向操作」补偿，或人工介入处理 |

设计要点：

1. **副作用必须可逆**。写库时记录 `batch_id → 写入的 row 主键`，回滚时按这个映射精确删，而不是「全库删除」。
2. **发现错误要尽早**。在 apply 之前插一个「dry-run 校验」步骤，把「方向错了」挡在副作用发生之前——能挡住 90% 的回滚需求。

> 回滚的本质是：**你必须在写的时候，就想好怎么删。** 等方向错了再想，往往已经删不干净了。

## 小结

- 状态机显式、可判终态、迁移合法；代码用 ALLOWED 字典约束。
- checkpoint 存最小真相（状态/进度/预算/产物引用），每批打点 + 副作用步骤 intent/done 两点。
- 确认点只设「恢复成本高」的步骤；人机分离，确认点允许进程退出。
- 幂等靠幂等键，补偿靠「写时记录映射、删时精确撤销」；熔断在花钱前判断；回滚分三档，写之前就想好怎么删。

## 下一篇

C26-3 把这套设计落成代码骨架：状态持久化、checkpoint 读写、幂等键、暂停/恢复接口、成本熔断。
