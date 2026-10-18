# C5-2 · 重试策略：退避、jitter 与幂等
> 阅读约 11 分钟。目标：写出一套"既有效又不添乱"的重试。

## 1. 为什么不能立刻重试

假设服务端因为过载开始返回 429，而 1000 个客户端都"立刻重试"——它们会在同一瞬间再次打过去，把刚缓过来的服务**再次打垮**。这叫**惊群（thundering herd）**。

所以重试的第一原则是：**退避（backoff）**——等一会儿，而且等待时间随失败次数增长。

## 2. 指数退避

```
delay = min(cap, base × 2^attempt)
```

常用参数：

| 参数 | 建议值 | 说明 |
|---|---|---|
| `base` | 0.5～1 秒 | 第一次等待 |
| `cap` | 8～30 秒 | 上限，避免无限增长 |
| `max_attempts` | 3～5 次 | 总次数（含首次） |

序列示例（base=1, cap=30）：1s → 2s → 4s → 8s → 16s。

## 3. jitter：为什么必须加

如果所有客户端同步失败、同步退避，它们仍会**同步重试**——惊群只是被推迟，没被消除。解决办法是加**随机抖动**：

| 类型 | 公式 | 特点 |
|---|---|---|
| 无 jitter | `d` | 会同步 |
| full jitter | `random(0, d)` | 最平缓，推荐 |
| equal jitter | `d/2 + random(0, d/2)` | 折中 |
| decorrelated | `random(base, prev×3)` | 更平滑，实现略复杂 |

**推荐 full jitter**：一句话能实现，效果最好。

```python
delay = random.uniform(0, min(cap, base * 2 ** attempt))
```

## 4. 尊重服务端给的信号

如果响应头里有：

- `Retry-After: 20`（秒）或 HTTP 日期 ——**优先用它**，别自己算；
- `x-ratelimit-reset-tokens` / `x-ratelimit-reset-requests` 一类头 —— 用它估算恢复时间。

服务端比你知道得多。有 `Retry-After` 就听它的，没有再退回到指数退避。

## 5. 重试预算：两个上限

只限制"次数"是不够的，还要限制"总时间"：

- **次数上限**：3～5 次；
- **总时长上限**（更重要）：比如"整个任务的重试总耗时不超过 30 秒"。

原因：一个 30 步的 Agent，如果每步都可能重试 5 次，最坏情况会退化成"卡住几分钟然后失败"。设总预算能让它**快速失败并降级**，而不是无限挣扎。

## 6. 只对"该重试的"重试

对照 C5-1 的类别：

```python
RETRYABLE = {429, 500, 502, 503, 504}          # 瞬时
RETRYABLE_CODES = {"rate_limit_exceeded", "internal_server_error", ...}

if status in RETRYABLE or err_code in RETRYABLE_CODES:
    retry()
else:
    raise                                        # B 类：不要白试
```

补充两条：

- **429 里要区分"限流"和"配额耗尽"**：限流等一会儿就好，配额耗尽（月度额度用光）重试也没用，应告警。
- **不要对 `context_length_exceeded` 直接重试**：必须先压缩（C5-1 第 5 节），否则必然再失败。

## 7. 幂等：重试安全的真正难点

"重试是否安全"取决于**这个请求有没有副作用**：

- 纯生成（问答、摘要）：重试安全，只是多花一次钱；
- 有副作用（下单、发邮件、写数据库）：**重试可能造成重复动作**。

处理方式：

1. **自己生成业务幂等键**（如 `task_id + step_index + tool_name + 参数哈希`），执行前查重；
2. **工具层做幂等**：写操作支持"同一 key 只执行一次"；
3. **流式已输出内容**不要盲目重试（C4-1）：要么接受部分结果，要么明确告知用户重新生成。

> 没有幂等保证时，宁可**失败并提示人工**，也不要自动重试副作用操作。

## 8. 代码骨架

```python
import random, time

def call_with_retry(fn, *, base=1.0, cap=30.0, max_attempts=4, deadline=30.0):
    started = time.time()
    last_exc = None
    for attempt in range(max_attempts):
        try:
            return fn()
        except RetryableError as e:
            last_exc = e
            if attempt == max_attempts - 1:
                break
            delay = random.uniform(0, min(cap, base * 2 ** attempt))   # full jitter
            if retry_after := getattr(e, "retry_after", None):
                delay = float(retry_after)
            if time.time() + delay - started > deadline:
                break                                                  # 超预算，交给降级
            time.sleep(delay)
    raise last_exc
```

四个要点都在里面：**指数退避 + full jitter + 尊重 Retry-After + 总时长预算**。

## 9. 重试时记录什么

```
attempt, delay, error_code, request_id, elapsed_ms, final_status
```

没有这些，你无法回答"我们的失败率到底是多少""重试是不是在掩盖某个真实问题"。

## 10. 小结

- 立刻重试会造成惊群，必须**指数退避 + jitter**（推荐 full jitter）。
- 有 `Retry-After` 就听服务端的。
- 限制**次数 + 总时长**两个预算。
- 只对瞬时错误重试；配额耗尽、参数错误不重试。
- **有副作用的操作必须有幂等保证**，否则宁可失败。

## 下一篇

重试解决单点失败，但如果整个服务被限流、或模型整体不可用，就需要更上层的手段——C5-3 讲限流、并发与降级。
