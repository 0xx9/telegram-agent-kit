#!/usr/bin/env bash
# Install Telegram Agent Kit skills into Cursor user directory
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DEST="${CURSOR_SKILLS_DIR:-$HOME/.cursor/skills}"
RULES_DEST="${CURSOR_RULES_DIR:-$HOME/.cursor/rules}"

echo "Telegram Agent Kit installer"
echo "  Skills -> $SKILLS_DEST"
echo "  Rules  -> $RULES_DEST"
echo

mkdir -p "$SKILLS_DEST" "$RULES_DEST"

for skill in "$ROOT"/skills/*/; do
  name="$(basename "$skill")"
  rm -rf "$SKILLS_DEST/$name"
  cp -R "$skill" "$SKILLS_DEST/$name"
  echo "  + skill: $name"
done

cp "$ROOT/rules/telegram-bot-security.mdc" "$RULES_DEST/telegram-bot-security.mdc"
echo "  + rule: telegram-bot-security.mdc"

echo
echo "Done. Restart Cursor or open a new Agent chat."
echo "Try: 'Build a join-request verifier bot with aiogram'"
