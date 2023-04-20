import typing
import asyncio


if typing.TYPE_CHECKING:
    from app.botpoll.web.app import Application


class Poller:
    def __init__(self, app: "Application") -> None:
        self.app = app
        self.is_running = False

    async def start(self) -> None:
        self.is_running = True
        await asyncio.shield(self.poll())

    async def stop(self) -> None:
        self.is_running = False
        await self.app.store.queue_poll.join()

    async def poll(self) -> None:
        while self.is_running:
            updates = await self.app.store.vkpoll.poll()
            for update in updates:
                self.app.store.queue_poll.put_nowait(update)

    def _done_callback(self, future: asyncio.Future) -> None:
        if future.exception():
            self.app.logger.exception("POLLING FAILED", exc_info=future.exception)
