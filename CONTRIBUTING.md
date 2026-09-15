# Contributing to Telegram Agent Kit

Thanks for helping grow this project. High-quality contributions get merged fast.

## What we accept

- New **skills** under `skills/<name>/SKILL.md`
- **Cursor rules** under `rules/*.mdc`
- **Starter templates** under `templates/<name>/`
- README fixes, typos, broken links

## Skill guidelines

1. One skill = one focused workflow (setup, deploy, payments, etc.)
2. Include YAML frontmatter with `name` and `description`
3. Add a **When to use** section and **Checklist** the agent can follow
4. Never include real tokens, phone numbers, or session files
5. Prefer Python examples unless the skill is framework-specific

## Template guidelines

- Include `.env.example` (never `.env`)
- Include `requirements.txt` or `pyproject.toml`
- Minimal working code — no 500-line demos
- README with setup steps

## Pull request checklist

- [ ] No secrets or session files
- [ ] Skill/rule tested in Cursor Agent at least once
- [ ] Linked from main README if new skill or template

## Topics for first contributors

- grammY (TypeScript) skill
- node-telegram-bot-api skill
- Docker + webhook template
- Telegram Mini Apps skill
- Channel moderation patterns
