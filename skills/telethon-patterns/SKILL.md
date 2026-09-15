---
name: telethon-patterns
description: >-
  Safe Telethon userbot patterns: sessions, flood wait, events, disconnect
  handling, and Bot API separation. Use when building MTProto clients or
  migrating from Pyrogram/Telethon legacy code.
---

# Telethon Patterns

Telethon uses **MTProto** (user/client API), not BotFather tokens.

## Client setup

```python
from telethon import TelegramClient
from telethon.sessions import StringSession
import os

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]

# Prefer StringSession in env for Docker; file session for local dev
session = os.getenv("SESSION_STRING")
if session:
    client = TelegramClient(StringSession(session), api_id, api_hash)
else:
    client = TelegramClient("bot_session", api_id, api_hash)
```

Never commit `bot_session.session` or export session strings to git.

## Main loop

```python
async def main():
    await client.start()
    me = await client.get_me()
    print(f"Logged in as {me.id}")
    await client.run_until_disconnected()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Event handlers

```python
from telethon import events

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def private_handler(event):
    await event.respond("Hello")
```

Use `incoming=True` explicitly. Filter early to reduce load.

## Flood wait (mandatory)

```python
from telethon.errors import FloodWaitError
import asyncio

try:
    await client.send_message(peer, text)
except FloodWaitError as e:
    await asyncio.sleep(e.seconds + 1)
    await client.send_message(peer, text)
```

Never spin-tight retry on flood errors.

## Join requests / channels

- Bot API handles `chat_join_request` — prefer Bot API for channel join flows when possible
- Userbots for actions bots cannot do — document ToS implications

## Disconnect & reconnect

```python
from telethon import connection

client = TelegramClient(
    session, api_id, api_hash,
    connection_retries=5,
    retry_delay=1,
)
```

Handle `KeyboardInterrupt` with `await client.disconnect()`.

## Bot vs userbot separation

| Task | Use |
|------|-----|
| Inline buttons in channels | Bot API |
| Read all group history as user | Telethon (careful) |
| Approve join requests | Bot API with admin rights |

Do not run Bot token client and userbot in one codebase without clear module boundaries.

## Anti-patterns

- Sharing one session file across multiple servers (session conflicts)
- `client.start(phone=...)` in production without interactive login solved first
- Ignoring `UserDeactivatedBanError` and retrying forever
- Scraping at high volume without delays

## Security

- Session string = full account — rotate if leaked
- Use dedicated account, not personal daily driver
- 2FA enabled on Telegram account
