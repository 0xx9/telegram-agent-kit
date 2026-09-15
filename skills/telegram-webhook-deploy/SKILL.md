---
name: telegram-webhook-deploy
description: >-
  Deploy Telegram bots with HTTPS webhooks on VPS, nginx, Docker, Railway, or
  Fly.io. Use when moving from polling to production, configuring SSL, or
  fixing webhook errors.
---

# Telegram Webhook Deploy

Production Telegram bots should use **webhooks**, not long polling.

## Requirements (Telegram enforces)

- HTTPS with valid certificate (Let's Encrypt OK)
- Port 443, 8443, 80, or 88
- Webhook URL must be publicly reachable
- Max webhook body ~1 MB; respond within timeout

## Pre-deploy checklist

- [ ] `BOT_TOKEN` only in environment, not code
- [ ] Health route (e.g. `GET /health`) for monitoring
- [ ] Graceful shutdown handler
- [ ] Set webhook **after** server is live and SSL works
- [ ] Log `getWebhookInfo` errors on startup

## aiogram 3 webhook (aiohttp)

```python
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://{DOMAIN}{WEBHOOK_PATH}"

async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()

def main():
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    app.on_startup.append(lambda _: on_startup(bot))
    app.on_shutdown.append(lambda _: on_shutdown(bot))
    web.run_app(app, host="0.0.0.0", port=8080)
```

## nginx reverse proxy (common VPS pattern)

```nginx
server {
    listen 443 ssl http2;
    server_name bot.example.com;

    ssl_certificate /etc/letsencrypt/live/bot.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/bot.example.com/privkey.pem;

    location /webhook {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /health {
        proxy_pass http://127.0.0.1:8080;
    }
}
```

Obtain cert: `certbot --nginx -d bot.example.com`

## Debug webhook issues

```bash
curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"
```

| Error symptom | Fix |
|---------------|-----|
| `SSL error` | Cert chain incomplete or wrong domain |
| `Connection refused` | App not listening / firewall |
| `Wrong response` | Return 200 quickly; defer heavy work |
| Pending updates pile up | `drop_pending_updates=True` once when switching modes |

## Platform notes

| Platform | Tip |
|----------|-----|
| Railway / Render | Use provided HTTPS URL + `/webhook` path |
| Fly.io | `fly certs add`; internal port 8080 |
| Docker | Expose 8080; terminate TLS at nginx or Traefik |

## Anti-patterns

- Running polling and webhook simultaneously
- Setting webhook to `http://` (rejected)
- Blocking the webhook handler with sync I/O or long LLM calls — queue background tasks instead
