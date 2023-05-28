import asyncio
import typing as tp


if tp.TYPE_CHECKING:
    from app.botpoll.web.app import Application


class Store:
    def __init__(self, app: "Application", queue_poll: asyncio.Queue) -> None:
        from app.botpoll.vkpoll.accessor import VkLongPollAccessor
        from app.botpoll.bot.factories import UpdateFactory

        self.factory = UpdateFactory()
        self.vkpoll = VkLongPollAccessor(app)
        self.queue_poll = queue_poll


def setup_store(app: "Application", queue_poll: asyncio.Queue) -> None:
    app.store = Store(app, queue_poll)
