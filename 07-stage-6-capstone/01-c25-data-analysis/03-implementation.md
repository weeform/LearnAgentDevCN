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

约 2 万行、跨 11 个月，够出「趋势」和「异常」题了。

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

调用时把 `schema` 文本格式化进去，再把问题拼进 user 消息。为了让结果可解析，`temperature=0`，并要求纯 JSON 输出。

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
    old_out = sys.stdout
    sys.stdout = io.StringIO()
    try:
        exec(code, {"__builtins__": __builtins__}, {})
        return {"success": True, "stdout": sys.stdout.getvalue()}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        sys.stdout = old_out
```

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
MAX_CORRECTIONS = 2
corrections = 0
while corrections < MAX_CORRECTIONS:
    plan = generate_code(question)          # 生成 {"sql","python","answer_value"}
    result = execute(plan)                  # 跑 SQL 或沙箱 Python
    if result["success"]:
        break
    messages.append(feedback(result))       # 回传 {error, hint}
    corrections += 1
if not result["success"]:
    return {"success": False, "error": "多次修正仍失败"}
```

## 6. 独立数值校验 + 结论

校验用「另一条路复算」，再把数字交给结论生成：

```python
def cross_check(plan, db="orders.db") -> bool:
    # 若模型用 SQL 算，就用 golden SQL / 改写 SQL 复算；反之用 SQL 复算 Python
    if plan["sql"]:
        r = run_sql(plan["sql"])
        expected = extract_scalar(r)          # 取第一行第一列
    else:
        expected = recompute_via_sql(plan)    # 按问题模板重写 SQL
    claimed = plan["answer_value"]
    return expected is not None and abs(claimed - expected) < max(1e-6, abs(expected) * 1e-4)

def generate_conclusion(question, claimed_value):
    # 只让它写结论，不让它重算
    ...
```

> 校验的容差要写死：浮点用相对误差 0.01%，整数必须完全相等。别用 `==` 直接比 float，那会让 90% 的题死在浮点尾巴上。

## 7. 小结

- 实现顺序：先跑通（验证逻辑）再加固（上 Docker 沙箱），两维度分开调试。
- SQL 用只读连接，零沙箱成本；Python 沙箱四道闸：断网、限资源、非 root、只读挂载。
- 错误回传复用 C11-2，修正上限独立记账（设 2）。
- 数值校验用另一条路复算，容差写死（相对 0.01%），结论段只写话不算数。

## 下一篇

C25-4 上评测：20 题评测集怎么自动判分、至少 3 个失败案例怎么拆、成本账怎么算、零逃逸怎么验证。
