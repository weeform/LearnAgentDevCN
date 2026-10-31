#!/usr/bin/env python3
"""为正文篇目插入「篇末思考题」小节。

用法：
    python scripts/add-thinking-questions.py .tmp_probe/tq-stage0.json [--dry-run]

JSON 结构（路径相对于仓库根目录）：
    { "01-stage-.../01-xxx.md": {"q": ["问1","问2","问3"], "hint": ["思路1","思路2","思路3"]} }

规则：
- 插入点为最后一个「## ...下一篇」小节之前；没有则追加到文末。
- 已有「## 思考题」的篇目跳过（幂等）。
- 统一用不编号的二级标题，避免打乱既有「## N. xxx」序号。
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEADING = "## 思考题"
NEXT_RE = "下一篇"
INTRO = "> 先自己答，再展开参考思路。这三问不考记忆，考的是你能不能把它用在自己的项目上。"


def build_block(questions, hints):
    lines = [HEADING, "", INTRO, ""]
    for i, q in enumerate(questions, 1):
        lines.append(f"{i}. {q}")
    lines += ["", "<details>", "<summary>参考思路</summary>", ""]
    for i, h in enumerate(hints, 1):
        lines.append(f"{i}. {h}")
    lines += ["", "</details>", ""]
    return "\n".join(lines)


def insert(path: Path, block: str, dry_run: bool) -> str:
    text = path.read_text(encoding="utf-8")
    if HEADING in text:
        return "skip(已有思考题)"

    raw_lines = text.splitlines()
    idx = None
    for i, line in enumerate(raw_lines):
        if line.startswith("## ") and NEXT_RE in line:
            idx = i
    if idx is None:
        new_text = text.rstrip("\n") + "\n\n" + block
    else:
        head = "\n".join(raw_lines[:idx]).rstrip("\n")
        tail = "\n".join(raw_lines[idx:]).strip("\n")
        new_text = head + "\n\n" + block + "\n" + tail + "\n"

    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return "insert" + ("(dry)" if dry_run else "")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        raise SystemExit(1)
    dry_run = "--dry-run" in sys.argv
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))

    stats = {"insert": 0, "skip(已有思考题)": 0, "insert(dry)": 0, "missing": 0}
    for rel, item in data.items():
        path = ROOT / rel
        if not path.exists():
            print(f"[MISS] {rel}")
            stats["missing"] += 1
            continue
        qs, hs = item["q"], item["hint"]
        if len(qs) != 3 or len(hs) != 3:
            print(f"[WARN] {rel} 问/思路数量不是 3（{len(qs)}/{len(hs)}）")
        result = insert(path, build_block(qs, hs), dry_run)
        stats[result] = stats.get(result, 0) + 1
        print(f"[{result}] {rel}")
    print("----")
    for k, v in stats.items():
        if v:
            print(f"{k}: {v}")


if __name__ == "__main__":
    main()
