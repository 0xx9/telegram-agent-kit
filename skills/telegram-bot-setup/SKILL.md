---
name: telegram-bot-setup
description: >-
  Set up a new Telegram bot project with BotFather, env vars, folder layout,
  and safe defaults. Use when creating a bot, configuring BOT_TOKEN, or
  scaffolding a Telegram Bot API project.
---

# Telegram Bot Setup

Use this skill when starting or restructuring a Telegram bot project.

## Checklist

1. **Never** commit `BOT_TOKEN`, `API_ID`, `API_HASH`, or `.session` files
2. Create `.env.example` with placeholder values; load secrets via `os.getenv` or pydantic-settings
3. Add `.gitignore` entries: `.env`, `*.session`, `__pycache__/`, `.venv/`
4. Choose mode early:
   - **Bot API** (aiogram, python-telegram-bot) — official bots via @BotFather
   - **MTProto userbot** (Telethon, Pyrogram) — user account automation; higher ToS risk
5. Do not mix Bot API token auth and MTProto session auth in one process without clear separation

## BotFather setup

1. Message [@BotFather](https://t.me/BotFather)
2. `/newbot` → pick name and username (must end in `bot`)
3. Store token as `BOT_TOKEN` in `.env`
4. Optional: `/setprivacy`, `/setjoingroups`, `/setcommands` before coding

## Recommended project layout

```
my-bot/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── bot/
│   ├── __init__.py
│   ├── main.py          # entrypoint
│   ├── config.py        # settings from env
│   ├── handlers/        # command & message handlers
│   └── middlewares/     # logging, throttling
└── tests/
```

## Config pattern (Python)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    bot_token: str
    admin_ids: list[int] = []

    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
```

## Polling vs webhook

| Mode | When |
|------|------|
| Polling | Local dev, quick prototypes |
| Webhook | Production, serverless, scale |

Default to **polling for dev**, **webhook for prod**. See `telegram-webhook-deploy` skill for production.

## Admin commands

- Restrict destructive commands to `ADMIN_ID` or `ADMIN_IDS` from env
- Never trust `message.from_user.id` alone for payment or privilege escalation without checking admin list

## Deliverables

When setup is complete, provide:

1. `.env.example` with all required vars documented
2. Minimal runnable `main.py` that responds to `/start`
3. README setup section (install, env, run)
4. Confirmation that no secrets appear in tracked files
