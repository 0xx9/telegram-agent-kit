import asyncio
import logging
import os

from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError

load_dotenv()

logging.basicConfig(level=logging.INFO)

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_NAME = os.getenv("SESSION_NAME", "user")

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


@client.on(events.NewMessage(incoming=True, pattern="/ping"))
async def ping_handler(event: events.NewMessage.Event) -> None:
    try:
        await event.respond("pong")
    except FloodWaitError as e:
        await asyncio.sleep(e.seconds + 1)
        await event.respond("pong")


async def main() -> None:
    await client.start()
    me = await client.get_me()
    logging.info("Logged in as %s (%s)", me.username, me.id)
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
