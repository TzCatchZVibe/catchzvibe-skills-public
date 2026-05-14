#!/usr/bin/env bash
# install.sh · 把 hooks/ 里的脚本 symlink 到 .git/hooks/
# 用法: ./hooks/install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HOOKS_DIR="$REPO_ROOT/.git/hooks"

mkdir -p "$HOOKS_DIR"

echo "🪝 安装 git hooks"
echo "   源: $SCRIPT_DIR/"
echo "   目标: $HOOKS_DIR/"
echo ""

# commit-msg (brand-voice-lint) · 不是 pre-commit · 因为要读 message check skip-lint
# 清除遗留 pre-commit symlink (如果有)
[ -L "$HOOKS_DIR/pre-commit" ] && rm "$HOOKS_DIR/pre-commit"
ln -sfn "$SCRIPT_DIR/pre-commit-brand-voice-lint.py" "$HOOKS_DIR/commit-msg"
chmod +x "$SCRIPT_DIR/pre-commit-brand-voice-lint.py"
echo "  ✅ commit-msg → brand-voice-lint (含 [skip-lint] override + audit log)"

echo ""
echo "🎉 完成. 试 commit · 看是否拦截"
