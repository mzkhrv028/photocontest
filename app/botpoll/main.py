import asyncio
import sys

from app.botpoll.bot.manager import Bot
from app.botpoll.web.app import setup_app


async def run_app(queue_poll: asyncio.Queue) -> None:
    bot = Bot(setup_app(queue_poll=queue_poll))
    await bot.run()


if __name__ == "__main__":
    queue = asyncio.Queue()
    try:
        asyncio.run(run_app(queue))
    except KeyboardInterrupt:
        sys.exit(1)
