---
name: aiogram-patterns
description: >-
  Best practices for aiogram 3.x bots: routers, FSM, filters, middleware,
  dependency injection, and async handlers. Use when building or refactoring
  aiogram Telegram bots.
---

# aiogram 3 Patterns

## Project structure

```
bot/
├── main.py
├── config.py
├── handlers/
│   ├── start.py
│   ├── admin.py
│   └── payments.py
├── keyboards/
├── middlewares/
│   └── throttling.py
└── states/
    └── form.py
```

## Router registration

```python
from aiogram import Dispatcher
from handlers import start, admin

dp = Dispatcher()
dp.include_router(start.router)
dp.include_router(admin.router)
```

## Handler filters

Prefer explicit filters over parsing text manually:

```python
from aiogram import Router, F
from aiogram.filters import Command, CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    ...

@router.message(Command("help"))
async def cmd_help(message: Message):
    ...

@router.callback_query(F.data.startswith("plan:"))
async def on_plan(callback: CallbackQuery):
    ...
```

## FSM (multi-step flows)

```python
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class JoinFlow(StatesGroup):
    waiting_code = State()

@router.message(JoinFlow.waiting_code)
async def got_code(message: Message, state: FSMContext):
    ...
    await state.clear()
```

Always `await state.clear()` on completion or cancel.

## Middleware throttling

```python
from aiogram import BaseMiddleware

class ThrottleMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 1.0):
        self.rate_limit = rate_limit
        self.last_seen: dict[int, float] = {}

    async def __call__(self, handler, event, data):
        user = getattr(event, "from_user", None)
        if user:
            now = time.monotonic()
            prev = self.last_seen.get(user.id, 0)
            if now - prev < self.rate_limit:
                return
            self.last_seen[user.id] = now
        return await handler(event, data)
```

## Error handling

```python
@dp.errors()
async def errors_handler(event: ErrorEvent):
    logging.exception("Update %s caused error", event.update.update_id)
```

## Anti-patterns

- `asyncio.get_event_loop()` in handlers — use `asyncio.get_running_loop()` if needed
- Blocking calls (`requests.get`, heavy CPU) in handlers — use `asyncio.to_thread` or aiohttp
- Giant monolithic `bot.py` — split routers
- Global mutable state without locks for concurrent updates

## Testing

- Mock `Bot` for unit tests
- Use aiogram test utilities or feed `Update` objects directly to dispatcher
