import asyncio
import typing as tp

from app.botsend.bot.worker import Worker

if tp.TYPE_CHECKING:
    from app.botsend.web.app import Application


class Bot:
    def __init__(self, app: "Application") -> None:
        self.app = app
        self.worker = Worker(app)

    async def run(self) -> None:
        try:
            await self.start()
        except asyncio.CancelledError:
            await self.stop()

    async def start(self) -> None:
        self.app.logger.info("START")
        await self.app.store.vksend.connect()
        await self.worker.start()

    async def stop(self) -> None:
        await self.worker.stop()
        await self.app.store.vksend.disconnect()
        self.app.logger.info("STOP")
