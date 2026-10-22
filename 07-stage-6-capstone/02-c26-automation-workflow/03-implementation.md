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
IDEM_F = DIR / "idempotency.json"

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
    "pending": {"running"},
    "running": {"awaiting_approval", "applying", "done", "failed", "failed_over_budget"},
    "awaiting_approval": {"applying", "rolled_back", "failed"},
    "applying": {"done", "rolled_back", "failed"},
}
def transition(s, to):
    assert to in ALLOWED[s["status"]], f"非法迁移 {s['status']} -> {to}"
    s["status"] = to
    save_state(s)

# ---------- 3. 幂等键 ----------
def _idem():
    return json.loads(IDEM_F.read_text(encoding="utf-8")) if IDEM_F.exists() else {}

def idem_seen(key):
    return key in _idem()

def idem_mark(key, status):
    m = _idem(); m[key] = status
    _atomic_write(IDEM_F, m)

# ---------- 4. 成本熔断 ----------
class BudgetExceeded(Exception):
    pass

def spend(s, usd):
    s["budget"]["spent_usd"] += usd
    save_state(s)
    if s["budget"]["spent_usd"] > s["budget"]["cap_usd"]:
        transition(s, "failed_over_budget")
        raise BudgetExceeded(s["budget"])

# ---------- 5. 各步骤（伪实现，真实步骤换成你的工具/模型调用） ----------
def step_fetch(s):
    if "fetch" in s["artifacts"]:
        return                                   # 已做过，跳过（幂等）
    items = [f"item_{i}" for i in range(s["progress"]["total"])]
    s["artifacts"]["fetch"] = "run/items.jsonl"
    save_state(s)

def step_process(s):
    done = s["progress"]["batches_done"]
    batch_count = s["progress"]["total"] // 20
    for b in range(len(done), batch_count):      # 幂等操作，靠 len(done) 从上次继续
        spend(s, 0.004)                          # 真实：调模型，估算成本
        s["progress"]["batches_done"].append(f"batch_{b}")
        save_state(s)                            # 每批结束打 checkpoint

def step_apply(s):
    # 敏感步骤：先暂停等人确认（见 C26-2 第 3 节）
    transition(s, "awaiting_approval")
    s["pending_approval"] = {
        "step": "apply",
        "summary": f"将写入 {len(s['progress']['batches_done']) * 20} 条",
    }
    save_state(s)                                # 进程在这里可以安全退出

def apply_rows(s):
    for key in s["progress"]["batches_done"]:
        if idem_seen(key):
            continue                             # 幂等去重
        idem_mark(key, "intent")                 # 执行前 intent（C15-2 第 3 节）
        # 真实：事务写入，并记 batch_id -> row 主键映射用于回滚
        idem_mark(key, "done")

def step_report(s):
    s["artifacts"]["report"] = "run/report.md"
    save_state(s)

# ---------- 6. 恢复与主循环 ----------
PLAN = [step_fetch, step_process, step_apply, step_report]

def resume(approved: bool):
    s = load_state()
    if s["status"] == "awaiting_approval":
        if not approved:
            transition(s, "rolled_back"); return
        transition(s, "applying"); apply_rows(s); transition(s, "done")
        return
    main()                                       # 其他情况从 checkpoint 继续

def main():
    s = load_state() or {
        "task_id": "t_001", "status": "pending",
        "artifacts": {}, "progress": {"total": 500, "batches_done": []},
        "budget": {"spent_usd": 0.0, "cap_usd": 1.0},
    }
    if s["status"] in ("done", "failed", "failed_over_budget", "rolled_back"):
        return                                   # 终态不再跑
    if s["status"] == "pending":
        transition(s, "running")
    for step in PLAN:
        step(s)
        if s["status"] in ("awaiting_approval", "failed", "failed_over_budget", "rolled_back"):
            return                               # 暂停或失败，等 resume / 人工
    transition(s, "done")
```

## 3. 逐段拆解

| 代码块 | 作用 | 对应前文 |
|---|---|---|
| `_atomic_write` | 先写临时文件再 `os.replace`，进程中途被杀不会留半截 JSON | C15-2 第 1 节 |
| `ALLOWED` + `transition` | 非法迁移直接 `assert` 崩掉，而不是静默进入脏状态 | C26-2 第 1 节 |
| `idem_seen / idem_mark` | 幂等键，非幂等步骤「键不存在才写」 | C26-2 第 4 节 |
| `spend` | 累计成本 + 超限熔断，熔断抛异常停在终态 | C26-2 第 5 节 |
| `step_fetch` 判产物存在、`step_process` 用 `len(done)` 起点 | **每步自己判断「做没做过」**，这是进程无状态的关键 | C26-2 第 2 节 |
| `step_apply` 只做 `transition` | 敏感步骤不真写，先停 `awaiting_approval` | C26-2 第 3 节 |
| `resume(approved)` | 人 approve 才进 `applying` 真写；reject 直接 `rolled_back` | C26-2 第 3 节 |
| `main` 里每步后检查状态 | 一旦 `awaiting_approval` / 终态就 `return`，不继续往下跑 | C26-2 第 1 节 |

## 4. 三个必须知道的坑

1. **「进程无状态」是靠「每步幂等」换来的**。`main()` 每次重启都从头走 `PLAN`，之所以不重复干活，是因为每一步开头都问「这步做过了吗」。丢掉这个判断，续跑就变成重跑。

2. **状态落盘要用原子写**。`save_state` 里如果直接 `open(w)` 写，进程恰好在写一半时被杀，盘上就是半截 JSON，下次 `load_state` 直接解析失败。`tmp + os.replace` 一行之差，决定续跑是救星还是二次灾难。

3. **`transition` 里的 `assert` 是故意的**。它让「非法状态迁移」当场崩掉，而不是把脏状态存进盘里留给下一轮猜。生产里可以把 `assert` 换成「记错误日志 + 置 `failed`」，但**绝不允许静默迁移**。

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

## 下一篇

C26-4 讲评测与成本数据：怎么用 kill 进程和注入故障来测续跑、怎么验证熔断、三个失败案例，以及长任务的 token 分布和熔断省下的钱。
