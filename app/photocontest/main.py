import asyncio

from app.photocontest.web.app import setup_app
from app.photocontest.photocontest.manager import Handler


async def run_app(
    queue_poll: asyncio.Queue, queue_send: asyncio.Queue
) -> None:
    handler = Handler(
        setup_app(
            queue_poll=queue_poll,
            queue_send=queue_send,
        )
    )
    await handler.run()


if __name__ == "__main__":
    queue_poll = asyncio.Queue()
    queue_send = asyncio.Queue()
    asyncio.run(run_app(queue_poll, queue_send))
