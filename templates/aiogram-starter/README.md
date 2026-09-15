# aiogram starter

Minimal aiogram 3 bot with env-based config. Dev: polling. Prod: see telegram-webhook-deploy skill.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env — add BOT_TOKEN from @BotFather
python -m bot.main
```

## Env

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | yes | From @BotFather |
| `ADMIN_IDS` | no | Comma-separated Telegram user IDs |
