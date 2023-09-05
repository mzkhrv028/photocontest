import asyncio

from app.botsend.bot.manager import Bot
from app.botsend.web.app import setup_app


async def run_app(queue_send: asyncio.Queue) -> None:
    bot = Bot(setup_app(queue_send=queue_send))
    await bot.run()


if __name__ == "__main__":
    queue = asyncio.Queue()
    asyncio.run(run_app(queue))
