import asyncio
import typing as tp

from app.botpoll.vkpoll.models import Event, Message, UpdateObject

if tp.TYPE_CHECKING:
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
            update_object: "UpdateObject" = await self.app.store.queue_send.get()
            try:
                await self.send_update(update_object)
            finally:
                self.app.store.queue_send.task_done()

    async def send_update(self, update_object: "UpdateObject") -> None:
        if isinstance(message := update_object, Message):
            await self.app.store.vksend.send_message(message)
        elif isinstance(event := update_object, Event):
            await self.app.store.vksend.send_event_answer(event)

    def _done_callback(self, future: asyncio.Future) -> None:
        if future.exception():
            self.app.logger.exception("SENDER FAILED", exc_info=future.exception)
