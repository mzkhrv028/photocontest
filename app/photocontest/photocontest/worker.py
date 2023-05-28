import typing as tp
import asyncio

from app.botpoll.vkpoll.models import UpdateObject, Message, Event


if tp.TYPE_CHECKING:
    from app.photocontest.web.app import Application


class Worker:
    def __init__(self, app: "Application") -> None:
        self.app = app
        self.is_running = False
        self.progress_task: asyncio.Task | None = None

    async def start(self) -> None:
        self.is_running = True
        self.progress_task = asyncio.create_task(self.progress_queue_poll())
        self.progress_task.add_done_callback(self._done_callback)
        await asyncio.shield(self.progress_task)

    async def stop(self) -> None:
        self.is_running = False
        await self.app.store.handler.cancel_all_game() #TODO: Убрать?

    async def progress_queue_poll(self) -> None:
        try:
            while self.is_running:
                update_object = await self.app.store.queue_poll.get()

                try:
                    await self.progress_update(update_object)
                finally:
                    self.app.store.queue_poll.task_done()
                    
        except asyncio.CancelledError:
            pass

    async def progress_update(self, update_object: "UpdateObject") -> None:
        command = None

        if isinstance(message := update_object, Message):
            if message.payload:
                command = message.payload
            elif message.text:
                command = message.text
        elif isinstance(event := update_object, Event):
            command = event.payload

        if command in self.app.context.commands:
            await self.app.context.commands[command](update_object)

    def _done_callback(self, future: asyncio.Future) -> None:
        if future.exception():
            self.app.logger.exception("HANDLER FAILED", exc_info=future.exception)
