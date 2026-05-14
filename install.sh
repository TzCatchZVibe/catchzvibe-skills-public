#!/usr/bin/env bash
# install.sh · symlink catchzvibe-skills → ~/.claude/skills/
# 用法: ./install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$SCRIPT_DIR/skills"
COMMANDS_DIR="$SCRIPT_DIR/commands"
SKILLS_TARGET="$HOME/.claude/skills"
COMMANDS_TARGET="$HOME/.claude/commands"

mkdir -p "$SKILLS_TARGET" "$COMMANDS_TARGET"

echo "📦 catchzvibe-skills install"
echo ""

# ─── Skills (目录级 symlink) ───
echo "▸ Skills → $SKILLS_TARGET"
for skill_path in "$SKILLS_DIR"/*/; do
    skill_name="$(basename "$skill_path")"
    target="$SKILLS_TARGET/$skill_name"

    if [ -L "$target" ]; then
        rm "$target"
    elif [ -d "$target" ]; then
        backup="$target.backup-$(date +%s)"
        echo "  ⚠️  $skill_name 已存在为目录 · 备份到 $backup"
        mv "$target" "$backup"
    fi

    ln -s "$skill_path" "$target"
    echo "  ✅ $skill_name"
done

# ─── Commands (文件级 symlink) ───
echo ""
echo "▸ Commands → $COMMANDS_TARGET"
if [ -d "$COMMANDS_DIR" ]; then
    for cmd_file in "$COMMANDS_DIR"/*.md; do
        [ -f "$cmd_file" ] || continue
        cmd_name="$(basename "$cmd_file")"
        target="$COMMANDS_TARGET/$cmd_name"

        if [ -L "$target" ]; then
            rm "$target"
        elif [ -f "$target" ]; then
            backup="$target.backup-$(date +%s)"
            echo "  ⚠️  $cmd_name 已存在为文件 · 备份到 $backup"
            mv "$target" "$backup"
        fi

        ln -s "$cmd_file" "$target"
        echo "  ✅ /$(basename "$cmd_name" .md)"
    done
fi

echo ""
echo "🎉 完成. 跑 claude /skills 或敲 / 看命令列表."
