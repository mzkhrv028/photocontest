import asyncio
import sys

from app.botpoll.main import run_app as run_botpoll
from app.photocontest.main import run_app as run_handler
from app.botsend.main import run_app as run_botsend


async def run_app() -> None:
    queue_poll = asyncio.Queue()
    queue_send = asyncio.Queue()

    botpoll_task = asyncio.create_task(run_botpoll(queue_poll=queue_poll), name="POLLER")
    handler_task = asyncio.create_task(
        run_handler(queue_poll=queue_poll, queue_send=queue_send),
        name="HANDLER",
    )
    botsend_task = asyncio.create_task(run_botsend(queue_send=queue_send), name="SENDER")

    await asyncio.gather(
        botpoll_task,
        handler_task,
        botsend_task,
    )


if __name__ == "__main__":
    asyncio.run(run_app(), debug=True)
