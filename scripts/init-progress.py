#!/usr/bin/env python3
"""从 progress.template.md 生成属于你自己的本地进度文件 progress.md。

为什么需要这一步：
    仓库里的 `progress.md` 被 .gitignore 排除，每个人 clone 后该文件都不存在。
    本脚本把共享模板复制成本地副本，让每个人各记各的进度，互不覆盖。

用法：
    python scripts/init-progress.py            # 幂等：已存在则不覆盖
    python scripts/init-progress.py --force    # 强制覆盖（会丢弃已有进度！）
    python scripts/init-progress.py --check    # 只看是否存在，不创建
    python scripts/init-progress.py --print    # 打印 progress.md 的绝对路径

退出码：
    0 = 成功 / 已存在
    1 = 模板缺失
    2 = 强制覆盖时需要交互式确认但没有 TTY

零依赖，标准库即可运行（Windows / macOS / Linux 通用）。
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = REPO_ROOT / "progress.template.md"
TARGET = REPO_ROOT / "progress.md"

# 模板顶部那段「这是模板不要编辑」的说明，生成本地副本时需要剥掉，
# 否则 progress.md 里会残留一堆和自己无关的指引。
HEADER_MARKER = "> ## ⚠️ 这是模板文件，不要直接编辑"


def strip_template_header(text: str) -> str:
    """去掉模板专属的说明区块，保留 H1 标题与正文骨架。

    模板结构：
        # 学习进度看板          <- 保留
        （空行）
        > ## ⚠️ 这是模板...     <- HEADER_MARKER，从这里开始丢弃
        > ...
        ---                    <- 第一个顶层分隔线，到此为止
        > 状态图例：...         <- 从这行开始保留
    """
    if HEADER_MARKER not in text:
        return text

    lines = text.splitlines(keepends=True)
    keep: list[str] = []
    skipping = False
    for line in lines:
        if HEADER_MARKER in line:
            skipping = True
            continue
        if skipping:
            # 跳过余下的引用行与空行，直到顶层分隔线收尾
            if line.strip() == "---":
                skipping = False
            continue
        keep.append(line)

    result = "".join(keep)
    # 剥离 header 后可能留下连续空行，压缩成最多一个
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.lstrip("\n").rstrip("\n") + "\n"


def build_from_template() -> str:
    if not TEMPLATE.is_file():
        print(f"[error] 找不到模板文件：{TEMPLATE}", file=sys.stderr)
        sys.exit(1)
    return strip_template_header(TEMPLATE.read_text(encoding="utf-8"))


def confirm_overwrite() -> bool:
    if not sys.stdin.isatty():
        print(
            "[error] --force 会丢弃已有进度，且当前非交互终端。"
            "请手动删除 progress.md 后重试，或加 -y 明确确认。",
            file=sys.stderr,
        )
        sys.exit(2)
    ans = input("progress.md 已存在，覆盖会丢失当前进度。确认？[y/N] ").strip().lower()
    return ans in ("y", "yes")


def main() -> int:
    parser = argparse.ArgumentParser(description="初始化本地学习进度文件")
    parser.add_argument("--force", action="store_true", help="覆盖已存在的 progress.md")
    parser.add_argument("-y", "--yes", action="store_true", help="配合 --force 跳过确认")
    parser.add_argument("--check", action="store_true", help="仅检查是否存在")
    parser.add_argument("--print", dest="do_print", action="store_true", help="打印路径")
    args = parser.parse_args()

    if args.do_print:
        print(TARGET)
        return 0

    rel = os.path.relpath(TARGET, Path.cwd()) if TARGET.is_relative_to(Path.cwd()) else str(TARGET)

    if args.check:
        if TARGET.is_file():
            print(f"[ok] 进度文件已存在：{rel}")
            return 0
        print(f"[missing] 尚未初始化：{rel}")
        return 0

    if TARGET.is_file():
        if not args.force:
            print(f"[skip] 已存在，不覆盖：{rel}")
            print("       要看 / 改进度直接编辑这个文件；要重置请加 --force。")
            return 0
        if not args.yes and not confirm_overwrite():
            print("[cancel] 已取消，进度保持不变。")
            return 0

    content = build_from_template()
    # newline="\n" 统一按 LF 写出：Windows 默认会转成 CRLF，和仓库里其他 md 不一致
    TARGET.write_text(content, encoding="utf-8", newline="\n")
    verb = "已重置" if args.force else "已创建"
    print(f"[done] {verb}本地进度文件：{rel}")
    print("       文件已加入 .gitignore，不会被提交，别人看不到你的勾选状态。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
