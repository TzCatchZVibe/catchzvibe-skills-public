#!/usr/bin/env python3
"""
commit-msg hook · 跑 brand-voice-lint 拒绝失败 caption commit
(cvs-atlas-2026-05-14-022.1 · R9 落地 · 硬规则用 hook 不靠 prose)

⚠️ 这是 commit-msg hook (不是 pre-commit) · 因为需要读 commit message
   检查 [skip-lint] override。pre-commit 看不到 message。

机制：
1. 读 $1 (commit message file)
2. 扫 staged .md 文件
3. 找标记 `<!-- LINT:CAPTION -->` 后跟代码块的 caption
4. 跑 lint.py
5. 不过 + message 无 [skip-lint] → exit 1
6. Override: commit message 含 `[skip-lint: <reason>]` 跳过 + 落 audit

安装: hooks/install.sh (本目录) · 把这个脚本 symlink 到 .git/hooks/commit-msg
"""

import re
import subprocess
import sys
import os
from pathlib import Path

LINT_PATH = os.path.expanduser("~/.claude/skills/brand-voice-lint/scripts/lint.py")
MARKER = "<!-- LINT:CAPTION -->"
SKIP_AUDIT = Path.home() / ".claude-skills-repo/_agent_inbox/_skip_lint_audit.md"


def staged_md_files():
    r = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True, text=True, check=True
    )
    return [f for f in r.stdout.strip().split("\n") if f.endswith(".md") and f]


def extract_captions(file_path: str) -> list[tuple[int, str]]:
    """Find captions marked with <!-- LINT:CAPTION --> followed by ``` block."""
    captions = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return captions

    for i, line in enumerate(lines):
        if MARKER in line:
            # Find next ``` block
            for j in range(i + 1, min(i + 5, len(lines))):
                if lines[j].strip().startswith("```"):
                    body = []
                    for k in range(j + 1, len(lines)):
                        if lines[k].strip().startswith("```"):
                            captions.append((i + 1, "".join(body)))
                            break
                        body.append(lines[k])
                    break
    return captions


def check_skip_override(msg_file: str) -> tuple[bool, str]:
    """Check if commit message has [skip-lint: reason]. msg_file 是 commit-msg hook 的 $1。"""
    if not os.path.exists(msg_file):
        return False, ""
    with open(msg_file, "r", encoding="utf-8") as f:
        msg = f.read()
    m = re.search(r"\[skip-lint:\s*(.+?)\]", msg)
    if m:
        return True, m.group(1).strip()
    return False, ""


def log_skip(reason: str, files: list[str]):
    SKIP_AUDIT.parent.mkdir(parents=True, exist_ok=True)
    with open(SKIP_AUDIT, "a", encoding="utf-8") as f:
        from datetime import datetime
        ts = datetime.now().isoformat()
        f.write(f"\n## {ts} · pre-commit skip-lint\n")
        f.write(f"- reason: {reason}\n")
        f.write(f"- files: {', '.join(files)}\n")


def lint(caption: str) -> tuple[bool, str]:
    r = subprocess.run(
        ["python3", LINT_PATH],
        input=caption, capture_output=True, text=True
    )
    return r.returncode == 0, r.stdout


def main():
    if not os.path.exists(LINT_PATH):
        print(f"⚠️  brand-voice-lint not installed at {LINT_PATH} · skipping hook")
        return 0

    # commit-msg hook 接 $1 (commit message file path)
    msg_file = sys.argv[1] if len(sys.argv) > 1 else ".git/COMMIT_EDITMSG"

    files = staged_md_files()
    if not files:
        return 0

    failed: list[tuple[str, int, str]] = []
    for f in files:
        for line_no, body in extract_captions(f):
            passed, output = lint(body)
            if not passed:
                failed.append((f, line_no, output))

    if not failed:
        return 0

    # Check skip override
    skip, reason = check_skip_override(msg_file)
    if skip:
        log_skip(reason, [f for f, _, _ in failed])
        print(f"⚠️  [skip-lint: {reason}] · {len(failed)} caption(s) failed · audit logged")
        return 0

    # Reject
    print(f"\n❌ brand-voice-lint pre-commit · {len(failed)} caption failed:")
    print("─" * 60)
    for f, line_no, output in failed:
        print(f"\n📄 {f}:{line_no}")
        print(output.rstrip())
    print("─" * 60)
    print(f"\n💡 修复 caption 后重新 commit")
    print(f"💡 紧急 override: commit message 加 [skip-lint: <reason>] (落 audit log)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
