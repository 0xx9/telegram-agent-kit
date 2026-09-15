---
name: telegram-security
description: >-
  Security checklist for Telegram bots and userbots: secrets, sessions, rate
  limits, logging redaction, and git safety. Use when reviewing code, before
  deploy, or after a suspected token leak.
---

# Telegram Security

Apply on every Telegram project before merge or deploy.

## Secrets

| Secret | Storage | Never |
|--------|---------|-------|
| `BOT_TOKEN` | `.env` / secret manager | In source, logs, screenshots |
| `API_ID` / `API_HASH` | `.env` | Committed to git |
| `.session` files | Local disk, encrypted backup | Git, Docker image layers, public zip |

If `BOT_TOKEN` leaks:

1. Revoke via @BotFather `/revoke`
2. Issue new token
3. Rotate on all servers
4. Scan git history for old token

## .gitignore minimum

```
.env
.env.*
*.session
*.session-journal
```

## Logging

- Redact tokens: log `token[:8]...` at most
- Never log full update payloads in production if they contain payment data
- Structured logs: user id ok; phone numbers and emails — minimize

## Rate limits & abuse

- Handle `RetryAfter` / flood wait in Telethon (`FloodWaitError`)
- Throttle user commands (e.g. 1 req / 2 sec per user)
- Admin-only commands gated by env admin list, not hardcoded usernames
- Validate callback_data length (64 byte limit) and content

## Userbot (MTProto) extra rules

- Userbots violate Telegram ToS for some use cases — document risk
- Never run userbot on main personal account for experiments
- Session files = full account access — treat like passwords
- Enable 2FA on the Telegram account

## Input validation

- Sanitize user HTML if using `parse_mode=HTML`
- Escape or whitelist dynamic content in messages
- Reject unexpected callback_data patterns

## Deployment

- Run as non-root user
- Read-only filesystem where possible
- Webhook path non-guessable optional (`/webhook/<random>`) — security through obscurity is weak but reduces scanner noise

## Pre-ship audit checklist

- [ ] No secrets in repo (`git grep -i "bot_token\|api_hash"`)
- [ ] `.env.example` has placeholders only
- [ ] Session files excluded
- [ ] Admin commands restricted
- [ ] Payment grants idempotent
- [ ] Error messages don't leak stack traces to users
