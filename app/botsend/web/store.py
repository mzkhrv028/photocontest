import asyncio
import typing as tp


if tp.TYPE_CHECKING:
    from app.botsend.web.app import Application


class Store:
    def __init__(self, app: "Application", queue_send: asyncio.Queue) -> None:
        from app.botsend.vksend.accessor import VkSendAccessor

        self.vksend = VkSendAccessor(app)
        self.queue_send = queue_send


def setup_store(app: "Application", queue_send: asyncio.Queue) -> None:
    app.store = Store(app, queue_send)
