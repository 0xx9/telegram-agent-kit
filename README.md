# Telegram Agent Kit

> **Production-ready [Cursor Agent Skills](https://cursor.com/docs/agent/skills) for Telegram bot developers.**

Stop letting AI generate broken webhooks, leaked tokens, and fragile Telethon sessions. This kit gives Cursor (and other AI coding agents) battle-tested patterns for Bot API and MTProto development.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Cursor Skills](https://img.shields.io/badge/Cursor-Agent%20Skills-000000?style=flat&logo=cursor&logoColor=white)](https://cursor.com)
[![Telegram](https://img.shields.io/badge/Telegram-Bot%20%26%20Userbot-26A5E4?style=flat&logo=telegram&logoColor=white)](https://core.telegram.org/bots)

---

## Why this exists

Telegram bots are easy to start and hard to ship. AI assistants often:

- Hardcode `BOT_TOKEN` in source files
- Use polling in production when webhooks are required
- Ignore flood limits and retry storms
- Mix userbot (MTProto) and bot (Bot API) patterns incorrectly
- Ship `.session` files or `.env` secrets to git

**Telegram Agent Kit** encodes real production rules so your agent ships safer code on the first try.

---

## Quick install (30 seconds)

```bash
git clone https://github.com/0xx9/telegram-agent-kit.git
cd telegram-agent-kit
./scripts/install.sh
```

This copies skills into `~/.cursor/skills/` so Cursor picks them up globally.

**Project-only install** (share with your team):

```bash
mkdir -p .cursor/skills
cp -r skills/* .cursor/skills/
cp rules/telegram-bot-security.mdc .cursor/rules/
```

Restart Cursor or open a new Agent chat. Skills activate when you ask about Telegram bots, webhooks, payments, Telethon, or aiogram.

---

## What's inside

### Agent Skills

| Skill | Use when |
|-------|----------|
| [`telegram-bot-setup`](skills/telegram-bot-setup/SKILL.md) | Starting a new bot, env config, BotFather, project layout |
| [`telegram-webhook-deploy`](skills/telegram-webhook-deploy/SKILL.md) | Production webhooks, HTTPS, nginx, Railway/Fly/VPS |
| [`telegram-payments`](skills/telegram-payments/SKILL.md) | Stars, invoices, pre-checkout, provider tokens |
| [`telegram-security`](skills/telegram-security/SKILL.md) | Secrets, sessions, rate limits, anti-leak checklist |
| [`aiogram-patterns`](skills/aiogram-patterns/SKILL.md) | aiogram 3.x routers, FSM, middleware, async best practices |
| [`telethon-patterns`](skills/telethon-patterns/SKILL.md) | Userbots, sessions, flood wait, event handlers |

### Cursor Rules

| Rule | Scope |
|------|-------|
| [`telegram-bot-security.mdc`](rules/telegram-bot-security.mdc) | Always-on security guardrails for any Telegram project |

### Starter templates

| Template | Stack |
|----------|-------|
| [`templates/aiogram-starter`](templates/aiogram-starter/) | Python + aiogram 3 + webhook-ready layout |
| [`templates/telethon-starter`](templates/telethon-starter/) | Python + Telethon + safe session handling |

---

## Example prompts (try these in Cursor)

```
Build a join-request verifier bot for my private channel using aiogram
```

```
Deploy my Telegram bot with webhooks on a VPS behind nginx + Let's Encrypt
```

```
Add Telegram Stars payments to my bot with proper pre_checkout_query handling
```

```
Review this Telethon userbot for session leaks and flood-wait handling
```

---

## Star history

If this saves you time, a star helps others find it.

[![Star History Chart](https://api.star-history.com/svg?repos=0xx9/telegram-agent-kit&type=Date)](https://star-history.com/#0xx9/telegram-agent-kit&Date)

---

## Contributing

We welcome skills, templates, and rule improvements. See [CONTRIBUTING.md](CONTRIBUTING.md).

**High-impact contributions:**

- New framework skills (python-telegram-bot, grammY, Telegraf)
- Deployment guides (Docker, Coolify, Render)
- Mini App / Web App patterns
- Channel growth & moderation workflows

---

## Related projects

- [aiogram](https://github.com/aiogram/aiogram) — modern async Bot API framework
- [Telethon](https://github.com/LonamiWebs/Telethon) — MTProto client library
- [PatrickJS/awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) — general Cursor rules collection
- [spencerpauly/awesome-cursor-skills](https://github.com/spencerpauly/awesome-cursor-skills) — curated Cursor skills

---

## License

MIT — use freely in personal and commercial bots.
