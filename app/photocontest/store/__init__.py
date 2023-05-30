import asyncio
import typing

from app.photocontest.store.database.database import Database

if typing.TYPE_CHECKING:
    from app.photocontest.web.app import Application


class Store:
    def __init__(
        self,
        app: "Application",
        queue_poll: asyncio.Queue,
        queue_send: asyncio.Queue,
    ) -> None:
        from app.photocontest.store.handler.accessor import HandlerAccessor
        from app.photocontest.store.vkapi.accessor import VkAccessor

        self.handler = HandlerAccessor(app)
        self.vkapi = VkAccessor(app)
        self.queue_poll = queue_poll
        self.queue_send = queue_send
        self.chats = {}


def setup_store(
    app: "Application", queue_poll: asyncio.Queue, queue_send: asyncio.Queue
) -> None:
    app.database = Database(app)
    app.store = Store(app, queue_poll, queue_send)
