# C26-3 · 实现
> 建议在电脑前边读边做。阅读约 15 分钟。目标：写出一个能跑的长时任务骨架，进程随时可 kill、重启能续跑、超预算会熔断、敏感步骤会等人。

## 1. 一条总原则：状态外置，进程无状态

本课所有代码围绕一句话展开：

> **进程里不留任何「丢了会心疼」的东西。** 任务进度、已完成的批、预算、待确认事项，全部落盘。进程只是一台「读状态 → 干一步 → 写状态」的机器，随时可以被 kill，重启后从盘上接着干。

这也是 C15-1 的核心结论：状态机是真相源，进程是从它派生的执行器。下面骨架约 100 行，五个组件一一对应 C26-2 的五节。

## 2. 完整代码骨架

```python
"""长时任务骨架：状态外置 + 断点续跑 + 幂等 + 人工确认 + 成本熔断"""
import json, os, time
from pathlib import Path

DIR = Path("run"); DIR.mkdir(exist_ok=True)
STATE_F = DIR / "state.json"
IDEM_F = DIR / "idem.json"

# ---------- 1. 状态持久化：原子写，进程挂了不留半截 ----------
def _atomic_write(path, obj):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)                      # 原子替换，见 C15-2 第 1 节

def load_state():
    return json.loads(STATE_F.read_text(encoding="utf-8")) if STATE_F.exists() else None

def save_state(s):
    s["updated_at"] = time.time()
    _atomic_write(STATE_F, s)

# ---------- 2. 状态机：合法迁移 ----------
ALLOWED = {
    "pending":           {"running"},
    "running":           {"awaiting_approval", "applying", "done",
                          "failed", "failed_over_budget", "rolled_back"},
    "awaiting_approval": {"applying", "rolled_back", "failed"},
    "applying":          {"running", "done", "rolled_back", "failed"},
    "failed":            {"running"},          # 外部重试：人工或调度器拉起
}
def transition(s, to):
    cur = s["status"]
    assert to in ALLOWED.get(cur, set()), f"非法迁移 {cur} -> {to}"
    s["status"] = to
    save_state(s)

# ---------- 3. 幂等键：intent / done 两点 ----------
def _idem():
    return json.loads(IDEM_F.read_text(encoding="utf-8")) if IDEM_F.exists() else {}

def idem_status(key):
    return _idem().get(key)                    # None / "intent" / "done"

def idem_mark(key, status):
    m = _idem(); m[key] = status
    _atomic_write(IDEM_F, m)

# ---------- 4. 成本熔断：花之前判，花之后记账 ----------
class BudgetExceeded(Exception):
    pass

EST_PER_BATCH = 0.004                          # 单批成本估算

def check_budget(s, next_est):
    """调模型之前调用。超了就停——绝不先花再判。"""
    if s["budget"]["spent_usd"] + next_est > s["budget"]["cap_usd"]:
        transition(s, "failed_over_budget")
        raise BudgetExceeded(s["budget"])

def spend(s, usd):
    """调完之后按实际发生额入账。只记账，不再判熔断。"""
    s["budget"]["spent_usd"] = round(s["budget"]["spent_usd"] + usd, 6)
    save_state(s)

# ---------- 5. 各步骤（伪实现，真实步骤换成你的工具/模型调用） ----------
def step_fetch(s):
    if "fetch" in s["artifacts"]:
        return                                 # 已做过，跳过（幂等）
    s["artifacts"]["fetch"] = "run/items.jsonl"
    save_state(s)

def step_process(s):
    done = s["progress"]["batches_done"]
    batch_count = s["progress"]["total"] // 20
    for b in range(len(done), batch_count):    # 幂等操作，靠 len(done) 从上次继续
        check_budget(s, EST_PER_BATCH)         # 先判预算
        cost = call_model_for_batch(b)         # 再花钱（真实：调模型）
        spend(s, cost)                         # 按实际额记账
        done.append(f"batch_{b}")
        save_state(s)                          # 每批结束打 checkpoint

def step_apply(s):
    if s["artifacts"].get("apply_done"):
        return                                 # 批过了、也写完了，别再来一次
    # 先把「要人确认什么」写全，再迁状态：transition 内部只 save 一次，
    # 状态与摘要同时落盘。两次 save 之间的空档，正是 checkpoint 最该防的半截状态。
    s["pending_approval"] = {
        "step": "apply",
        "summary": f"将写入 {len(s['progress']['batches_done']) * 20} 条",
    }
    transition(s, "awaiting_approval")         # 进程在这里可以安全退出

def apply_rows(s):
    for key in s["progress"]["batches_done"]:
        st = idem_status(key)
        if st == "done":
            continue                           # 确实写完了，跳过
        if st == "intent":
            # 「已开始、结果未知」：不能盲目重写（会重复插入），也不能当它成功。
            # 交对账或人工判定——这正是两点打点买回来的信息。
            s["needs_reconcile"].append(key)
            save_state(s)
            continue
        idem_mark(key, "intent")               # 执行前打 intent（C15-2 第 3 节）
        write_batch(key)                       # 真实：事务写入 + 记 batch→主键映射
        idem_mark(key, "done")                 # 执行后打 done
    s["artifacts"]["apply_done"] = True
    save_state(s)

def step_report(s):
    if s["artifacts"].get("report"):
        return
    s["artifacts"]["report"] = "run/report.md"
    save_state(s)

# ---------- 6. 恢复与主循环 ----------
PLAN = [step_fetch, step_process, step_apply, step_report]

def resume(approved: bool = None):
    s = load_state()
    if s["status"] == "awaiting_approval":
        if not approved:
            transition(s, "rolled_back")
            return
        transition(s, "applying")
        apply_rows(s)
        transition(s, "running")               # 写完回主流程，别直接跳终态
    main()                                     # 从 PLAN 头重走：各步自己判断做没做过

def main():
    s = load_state() or {
        "task_id": "t_001", "status": "pending", "schema_version": 1,
        "artifacts": {}, "needs_reconcile": [],
        "progress": {"total": 500, "batches_done": []},
        "budget": {"spent_usd": 0.0, "cap_usd": 1.0},
    }
    if s["status"] in ("done", "failed", "failed_over_budget", "rolled_back"):
        return                                 # 终态不自动跑
    if s["status"] == "awaiting_approval":
        return                                 # 等人点头，别自己往下走
    if s["status"] == "applying":              # 上次写到一半崩了
        apply_rows(s)                          # 靠 intent/done 精确续，不会重复写
        transition(s, "running")
    if s["status"] == "pending":
        transition(s, "running")
    for step in PLAN:
        step(s)
        if s["status"] in ("awaiting_approval", "failed", "failed_over_budget", "rolled_back"):
            return                             # 暂停或失败，等 resume / 人工
    transition(s, "done")
``````

## 3. 逐段拆解

| 代码块 | 作用 | 对应前文 |
|---|---|---|
| `_atomic_write` | 先写临时文件再 `os.replace`，进程中途被杀不会留半截 JSON | C15-2 第 1 节 |
| `ALLOWED` + `transition` | 非法迁移直接 `assert` 崩掉，而不是静默进入脏状态 | C26-2 第 1 节 |
| `idem_status / idem_mark` | 幂等键存**两态**（`intent` / `done`），不是只存「见过没有」 | C26-2 第 4 节、C26-5 取舍三 |
| `check_budget` + `spend` | **判断和记账分成两个函数**：花之前按估算判，花之后按实际额记 | C26-2 第 5 节 |
| `step_fetch` 判产物存在、`step_process` 用 `len(done)` 起点 | **每步自己判断「做没做过」**，这是进程无状态的关键 | C26-2 第 2 节 |
| `step_apply` 先写 `pending_approval` 再 `transition` | 敏感步骤不真写；摘要和状态在同一次落盘里，不留半截 | C26-2 第 3 节 |
| `resume(approved)` | approve 后 `applying` → 写完 → 回 `running` 继续剩余步骤；reject 直接 `rolled_back` | C26-2 第 3、6 节 |
| `main` 里每步后检查状态 | 一旦 `awaiting_approval` / 终态就 `return`，不继续往下跑 | C26-2 第 1 节 |

## 4. 五个必须知道的坑

1. **「进程无状态」是靠「每步幂等」换来的**。`main()` 每次重启都从头走 `PLAN`，之所以不重复干活，是因为每一步开头都问「这步做过了吗」。丢掉这个判断，续跑就变成重跑。

2. **状态落盘要用原子写**。`save_state` 里如果直接 `open(w)` 写，进程恰好在写一半时被杀，盘上就是半截 JSON，下次 `load_state` 直接解析失败。`tmp + os.replace` 一行之差，决定续跑是救星还是二次灾难。

3. **`transition` 里的 `assert` 是故意的**。它让「非法状态迁移」当场崩掉，而不是把脏状态存进盘里留给下一轮猜。生产里可以把 `assert` 换成「记错误日志 + 置 `failed`」，但**绝不允许静默迁移**。

4. **熔断的判断和记账必须分开**。合在一个 `spend()` 里写成「先加钱、再判断超没超」，就是典型的**先花再判**——你已经在超支那一刻之后才喊停，最后那一跳的钱已经花掉了。正确顺序是：调用前 `check_budget(s, 估算)`，超了直接停、这一跳根本不会发生；调用后 `spend(s, 实际额)` 只负责入账。C26-2 第 5 节那句「不是花完了才停」，落到代码就是这两个函数的分工。

5. **`intent` 不等于 `done`，这两态必须分开存**。只记「这个键见过没有」，会让「上次开始了但没写完」的批次被当成已完成、静默跳过——数据就永久少了一块，而且不报错。所以 `idem_status` 返回三值（`None` / `intent` / `done`）：`done` 才跳过，`intent` 送进 `needs_reconcile` 交人工对账。**两点打点买的就是这个「结果未知」信息**，图省事合成一态，C26-5 取舍三就白讲了。

## 5. 何时从 JSON 升级到 SQLite

本骨架用 JSON 文件，够单人单任务用。当出现下面任一信号，换 SQLite（或直接上带事务的数据库）：

- 需要**并发**：多个任务同时读写同一个状态文件会互相覆盖。
- 需要**按批次查询**：JSON 里 `batches_done` 越堆越大，要查「某批到底 done 没」得全量加载。
- 需要**事务**：幂等键 + 业务写入要「同生共死」，靠文件做不到原子。

> 升级的边界很清晰：**「状态」从「存下来」变成「查出来、并发改」的时候，就是 JSON 的尽头**。学习阶段 JSON 完全够，别提前上 SQLite。

## 小结

- 总原则：状态外置、进程无状态；进程是「读状态 → 干一步 → 写状态」的执行器。
- 五个组件一一对应设计：原子落盘、状态机、幂等键、成本熔断、暂停/恢复。
- 续跑不重跑的前提是「每步幂等 + 开头判断做没做过」；原子写是续跑不翻车的底线。
- JSON 够单人单任务；要并发/查询/事务时再上 SQLite。
- 两处最容易写反：熔断要在花钱前判（判断与记账分开）、幂等键要分 intent/done 两态（不然「结果未知」被当成成功）。

## 思考题

> 先自己答，再展开参考思路。这三问不考记忆，考的是你能不能把它用在自己的项目上。

1. 「进程是读状态 → 干一步 → 写状态 的执行器」——这句话怎么让续跑变简单？
2. 原子写为什么是「续跑不翻车的底线」？非原子会发生什么？
3. 什么时候该从 JSON 升级到 SQLite？触发条件是什么？

<details>
<summary>参考思路</summary>

1. 因为进程本身不持有任何进度，杀掉重启后读到的就是真实进度。续跑不需要「恢复内存」，只需要「重新读一遍文件」。
2. 写到一半被 kill 会留下半个 JSON，下次启动解析失败——任务永久卡死且无法诊断。原子写（临时文件 + rename）保证状态要么是旧的、要么是新的。
3. 出现并发写、需要按状态查询、或需要事务性多表更新时。单人单任务用 JSON 完全够，提前上 SQLite 只是多一层复杂度。

</details>

## 下一篇

C26-4 讲评测与成本数据：怎么用 kill 进程和注入故障来测续跑、怎么验证熔断、三个失败案例，以及长任务的 token 分布和熔断省下的钱。
