import asyncio
import signal

from app.botpoll.main import run_app as run_botpoll
from app.botsend.main import run_app as run_botsend
from app.photocontest.main import run_app as run_handler


async def shutdown_app(signal: signal.Signals, loop: asyncio.AbstractEventLoop) -> None:
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    [task.cancel() for task in tasks]

    await asyncio.gather(*tasks, return_exceptions=True)

    loop.stop()


async def run_app() -> None:
    loop = asyncio.get_event_loop()

    for sig in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda sig=sig: asyncio.create_task(shutdown_app(sig, loop)))

    queue_poll = asyncio.Queue()
    queue_send = asyncio.Queue()

    botpoll_task = asyncio.create_task(run_botpoll(queue_poll=queue_poll), name="POLLER")
    handler_task = asyncio.create_task(run_handler(queue_poll=queue_poll, queue_send=queue_send), name="HANDLER")
    botsend_task = asyncio.create_task(run_botsend(queue_send=queue_send), name="SENDER")

    await asyncio.gather(botpoll_task, handler_task, botsend_task, return_exceptions=True)


if __name__ == "__main__":
    try:
        asyncio.run(run_app(), debug=True)
    except asyncio.CancelledError:
        pass
