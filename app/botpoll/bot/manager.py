import asyncio
import typing as tp

from app.botpoll.bot.poller import Poller


if tp.TYPE_CHECKING:
    from app.botpoll.web.app import Application


class Bot:
    def __init__(self, app: "Application") -> None:
        self.app = app
        self.poller = Poller(app)

    async def run(self) -> None:
        try:
            await self.start()
        except asyncio.CancelledError:
            await self.stop()

    async def start(self) -> None:
        self.app.logger.info("START")
        await self.app.store.vkpoll.connect()
        await self.poller.start()

    async def stop(self) -> None:
        await self.poller.stop()
        await self.app.store.vkpoll.disconnect()
        self.app.logger.info("STOP")
