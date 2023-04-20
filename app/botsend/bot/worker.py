import typing
import asyncio
from app.botpoll.vkpoll.models import Update

if typing.TYPE_CHECKING:
    from app.botsend.web.app import Application


class Worker:
    def __init__(self, app: "Application") -> None:
        self.app = app
        self.is_running = False

    async def start(self) -> None:
        self.is_running = True
        await asyncio.shield(self.progress_queue_send())

    async def stop(self) -> None:
        self.is_running = False
        await self.app.store.queue_send.join()

    async def progress_queue_send(self) -> None:
        while self.is_running:
            update = await self.app.store.queue_send.get()
            try:
                await self.send_update(update)
            finally:
                self.app.store.queue_send.task_done()

    async def send_update(self, update: Update) -> None:
        if update.object.message:
            await self.app.store.vksend.send_message(update.object.message)
        elif update.object.event:
            await self.app.store.vksend.send_event_answer(update.object.event)

    def _done_callback(self, future: asyncio.Future) -> None:
        if future.exception():
            self.app.logger.exception("SENDER FAILED", exc_info=future.exception)
