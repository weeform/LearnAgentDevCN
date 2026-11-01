# C25-3 · 实现
> 阅读约 15 分钟，建议在电脑前边读边做。目标：写出一套能跑通「问问题 → 沙箱算 → 校验 → 结论」的最小实现，先跑通再加固。

## 1. 先跑通再加固：两条腿走

实现顺序很关键，别一上来就想把沙箱做完美：

1. **先跑通**：用 SQLite + 一个「受限但没上 Docker」的执行器，把整条流水线串起来，确认能答对几道题。
2. **再加固**：把 Python 执行换成 Docker 沙箱，补上资源上限、越权拦截、逃逸记录。

> 为什么：沙箱是「安全层」，不影响「逻辑对不对」。先验证逻辑（schema 注入、校验、回传有没有用），再上安全层，调试成本低得多。两个维度分开验证，别搅在一起。

## 2. 数据准备：一张 SQLite 表

```python
import sqlite3, random
from datetime import date, timedelta

def build_db(path="orders.db", seed=42):
    random.seed(seed)
    regions = ["华东", "华北", "华南", "西南"]
    cats = {"电子": (199, 12999), "服饰": (99, 999),
            "食品": (9.9, 199), "家居": (49, 1999)}
    conn = sqlite3.connect(path)
    conn.execute("""CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        order_date TEXT, region TEXT, category TEXT,
        quantity INTEGER, unit_price REAL, revenue REAL, cost REAL)""")
    rows = []
    for i in range(1, 20001):
        d = date(2026, 1, 1) + timedelta(days=random.randint(0, 300))
        region = random.choice(regions)
        cat = random.choice(list(cats))
        qty = random.randint(1, 10)
        price = round(random.uniform(*cats[cat]), 2)
        rev = round(qty * price, 2)
        cost = round(rev * random.uniform(0.5, 0.85), 2)
        rows.append((i, str(d), region, cat, qty, price, rev, cost))
    conn.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?,?,?)", rows)
    conn.commit()
    return conn
```

约 2 万行；日期范围是 2026-01-01 往后 300 天（到 10 月底），跨 10 个自然月，够出「趋势」和「异常」题了。

## 3. 代码生成：schema 注入

把 C25-2 的 schema 塞进 system prompt，让模型输出「SQL 优先」的 JSON：

```python
SYSTEM_PROMPT = """你是数据分析助手。只做一件事：把用户的数据问题变成可执行查询并给出答案。

表 orders schema：
{SCHEMA}

规则：
1. 聚合/分组/过滤/趋势/异常类，优先写 SQL（只读 SELECT，禁止写操作）。
2. 只有 SQL 表达不了才写 Python。
3. 输出 JSON：{"sql": "...或空", "python": "...或空", "answer_value": 数字}

SQL 里的表和列必须严格按 schema，不要编造不存在的列。"""
```

注入 schema 时**千万不要用 `str.format()`**：这个 prompt 里本身就带着输出 JSON 的大括号（`{"sql": ...}`），`.format()` 会把它们当成格式占位符，直接抛 `KeyError: '"sql"'`。最省事的是：

```python
prompt = SYSTEM_PROMPT.replace("{SCHEMA}", schema_text)
```

或者把 JSON 那几对括号全转义成 `{{ }}`（难看但能用）。拼好 user 消息后，`temperature=0`，并要求纯 JSON 输出。

## 4. 执行层：SQL 直跑 + Python 沙箱

SQL 侧几乎零成本——只读连接 + 禁写：

```python
def run_sql(sql: str, db="orders.db"):
    conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)  # 只读
    try:
        cur = conn.execute(sql)
        return {"success": True, "rows": cur.fetchall()}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

Python 侧分两档。**第一档（跑通用）**：先上一个「够用」的执行器，明确标注这是临时版：

```python
def run_python_bare(code: str, timeout=5) -> dict:
    # ⚠ 临时版：无沙箱，仅用于本地逻辑调试，切勿喂不可信输入
    import io, sys
    buf = io.StringIO()
    env = {"__builtins__": __builtins__}
    old_out = sys.stdout
    sys.stdout = buf
    try:
        exec(code, env, env)          # globals 和 locals 必须传同一个 dict
        return {"success": True, "stdout": buf.getvalue()}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        sys.stdout = old_out
```

> `exec(code, env, env)` 里那个「传两次」不是啰嗦，是必须的。写成 `exec(code, env, {})`（globals 和 locals 分开）时，模块级语句把变量写进 locals，而**函数体、推导式、lambda 内部是按 globals 查名字的**——于是「先 `df = load()`、再 `def top(): return df.nlargest(...)`」这种最常见的两段式代码，一执行就 `NameError: name 'df' is not defined`，而代码本身完全正确。数据分析 Agent 生成的代码十有八九是这个形状，这个坑踩一次能耗掉半天。

**第二档（加固）**：换成 Docker 沙箱。四道闸一起上：

```python
import subprocess, tempfile, os

def run_python_sandbox(code: str, timeout=10) -> dict:
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code); path = f.name
    try:
        r = subprocess.run(
            ["docker", "run", "--rm",
             "--network", "none",                 # 闸1：断网
             "--memory", "256m", "--cpus", "1",   # 闸2：限资源
             "--user", "1000:1000",               # 闸3：非 root
             "-v", f"{os.path.abspath('orders.db')}:/data/orders.db:ro",  # 闸4：只读挂载
             "-v", f"{path}:/code/run.py",
             "python:3.11-slim", "python", "/code/run.py"],
            capture_output=True, text=True, timeout=timeout)
        return {"success": r.returncode == 0,
                "stdout": r.stdout[-2000:],
                "error": r.stderr[-1000:]}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "执行超时"}
    finally:
        os.unlink(path)
```

> 四道闸缺一不可：断网防数据外发、限资源防死循环吃满、非 root 防改宿主文件、只读挂载防篡改数据。C23-2 有完整论证，这里给的是本项目的最小落地。

C9-3 的 `ast` 白名单在这里是**第五道闸**（纵深防御）：进沙箱前先用 `ast.parse` 扫一遍，白名单外直接拒。它挡不住 `open()`，但能拦下 `__import__`、`eval`、`exec` 这类最直接的注入。

## 5. 错误回传循环

把执行结果结构化回传（C11-2），修正上限独立记账：

```python
MAX_CORRECTIONS = 2                        # 初次之外，最多再修 2 次

def solve(question):
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}]
    result = None
    for _ in range(MAX_CORRECTIONS + 1):   # 1 次初跑 + 2 次修正
        plan = generate_code(messages)     # 必须把 messages 传进去
        result = execute(plan)             # 跑 SQL 或沙箱 Python
        if result["success"]:
            break
        messages.append(feedback(result))  # 回传 {error, hint}
    if not result or not result["success"]:
        return {"success": False, "error": "多次修正仍失败"}
    return result
```

两个细节决定这段能不能真跑起来：

1. **`range(MAX_CORRECTIONS + 1)`，不是 `range(MAX_CORRECTIONS)`**。`MAX_CORRECTIONS` 的语义是「允许修几次」，初跑不算一次修正。写成 `range(MAX_CORRECTIONS)` 就变成「总共只跑 2 次 = 只修了 1 次」，与 C25-2 说的「修正上限设 2」差一次。这类差一错误不会报错，只会让你的评测表悄悄少一截修正成功率。
2. **`generate_code` 必须吃 `messages`**。原版是 `generate_code(question)`——那样 `messages.append(feedback(result))` 加进去的报错，模型**根本看不到**，回传机制形同虚设，每次都在重新生成同样的错代码。

## 6. 独立数值校验 + 结论

校验用「另一条路复算」，再把数字交给结论生成：

```python
def extract_scalar(r):
    return r["rows"][0][0] if r.get("rows") else None

def cross_check(plan, question, db="orders.db") -> dict:
    """两条彼此独立的路：A = 模型自己算的，B = 另起一条实现算的。"""
    if plan["sql"]:
        own   = extract_scalar(run_sql(plan["sql"], db))       # 模型自己写的那段 SQL
        other = recompute_independently(question, db)          # 独立重写一版 SQL（或 golden_sql）
    else:
        own   = plan["answer_value"]                           # 模型用 Python 算出来的数
        other = extract_scalar(run_sql(rewrite_as_sql(question), db))  # 换 SQL 复算

    if own is None or other is None:
        return {"pass": False, "reason": "某一侧没有产出数字"}

    ok = abs(own - other) < max(1e-6, abs(other) * 1e-4)       # 相对容差 0.01%
    return {"pass": ok, "own": own, "other": other}
```

> 校验的容差要写死：浮点用相对误差 0.01%，整数必须完全相等。别用 `==` 直接比 float，那会让 90% 的题死在浮点尾巴上。

**这段代码最容易被写错的地方，是把「重跑一遍」当成「校验」了**。它长这样：

```python
if plan["sql"]:
    r = run_sql(plan["sql"])          # 把模型自己写的 SQL 再跑一遍
    expected = extract_scalar(r)      # ← 这不是校验
```

然后拿 `expected` 跟 `answer_value` 比。看着很合理，其实**什么都没验**：SQL 是确定性的，同一段 SQL 跑两遍必然得到同一个数。它能抓到的只有一种错——「模型嘴上报的数字和它自己代码输出不一致」，也就是它心算错了。

而「算错还很有信心」恰恰不是这一种。C25-4 案例 A 里，模型把环比写成了同比：那段 SQL 跑得又顺又漂亮，重跑一百遍还是那个错数，你拿它自己跟自己比，永远 PASS。

所以要分清两级：

| 级别 | 拿谁跟谁比 | 能抓到 | 成本 |
|---|---|---|---|
| 一致性检查 | `answer_value` vs 模型自己代码的输出 | 嘴上说的 ≠ 代码算的（心算错、抄错） | 几乎为零 |
| **独立复算** | 模型的路 vs **另起一条路的**结果 | 代码逻辑本身就错（环比/同比、漏 where、排序取错） | 一次额外查询 |

一致性检查值得做（便宜，能拦一类低级错），但它**不能替代独立复算**。真正定义「数值正确」的是第二行——那才是 C25-1 说的「用另一条路复算」。独立那条路的来源可以是：评测集里的 `golden_sql`、按题目模板重写的 SQL、或者让另一个模型在**看不到第一版 SQL** 的前提下独立写一遍。

```python
def generate_conclusion(question, claimed_value):
    # 只让它写结论，不让它重算
    ...
```

## 7. 小结

- 实现顺序：先跑通（验证逻辑）再加固（上 Docker 沙箱），两维度分开调试。
- SQL 用只读连接，零沙箱成本；Python 沙箱四道闸：断网、限资源、非 root、只读挂载。
- 错误回传复用 C11-2，修正上限独立记账（设 2）。
- 数值校验用另一条路复算，容差写死（相对 0.01%），结论段只写话不算数。

## 思考题

> 先自己答，再展开参考思路。这三问不考记忆，考的是你能不能把它用在自己的项目上。

1. 为什么「先跑通再加固」要分成两个维度，而不是一次做完？
2. Python 沙箱的四道闸分别防什么？少一道会怎样？
3. 修正上限为什么要「独立记账」，和主循环的步数上限分开算？

<details>
<summary>参考思路</summary>

1. 因为逻辑问题和安全问题混在一起调试时，你分不清「跑不通」是代码生成错还是沙箱挡的。分开后每层都有明确的成功标准。
2. 断网防外泄、限资源防挖矿/OOM、非 root 防权限提升、只读挂载防篡改宿主。少断网，数据可能被直接发出去；少限资源，一个死循环能拖垮宿主。
3. 因为修正是个高频循环，很容易把总步数预算吃光，导致后面该做的校验和结论没机会跑。独立记账能保证「修不好就停」而不影响整体流程。

</details>

## 下一篇

C25-4 上评测：20 题评测集怎么自动判分、至少 3 个失败案例怎么拆、成本账怎么算、零逃逸怎么验证。
