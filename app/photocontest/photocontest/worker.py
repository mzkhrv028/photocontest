import typing
import asyncio

if typing.TYPE_CHECKING:
    from app.botpoll.vkpoll.models import Update
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
        for chat_id in self.app.store.chats:
            await self.app.store.handler.update_state_game(chat_id, None)

    async def progress_queue_poll(self) -> None:
        while self.is_running:
            update = await self.app.store.queue_poll.get()
            try:
                await self.progress_update(update)
            finally:
                self.app.store.queue_poll.task_done()

    async def progress_update(self, update: "Update") -> None:
        cmd = None

        if update.object.message:
            if update.object.message.payload:
                cmd = update.object.message.payload
            elif update.object.message.text:
                cmd = update.object.message.text
        elif update.object.event:
            cmd = update.object.event.payload

        if cmd in self.app.context.commands:
            await self.app.context.commands[cmd](update)

    def _done_callback(self, future: asyncio.Future) -> None:
        if future.exception():
            self.app.logger.exception("HANDLER FAILED", exc_info=future.exception)
