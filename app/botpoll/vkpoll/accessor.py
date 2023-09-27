import typing as tp

from aiohttp import TCPConnector
from aiohttp.client import ClientSession

if tp.TYPE_CHECKING:
    from app.botpoll.vkpoll.models import UpdateObject
    from app.botpoll.web.app import Application


API_PATH = "https://api.vk.com/method/"


class VkLongPollAccessor:
    def __init__(self, app: "Application") -> None:
        self.app = app
        self.session: ClientSession | None = None
        self.key: str | None = None
        self.server: str | None = None
        self.ts: int | None = None

    async def connect(self) -> None:
        self.session = ClientSession(connector=TCPConnector(verify_ssl=False))
        try:
            await self._get_long_poll_server()
        except Exception as e:
            self.app.logger.error("Exception", exc_info=e)
        self.app.logger.info("VK POLLING")

    async def disconnect(self) -> None:
        if self.session:
            await self.session.close()

    async def _get_long_poll_server(self) -> None:
        method = "groups.getLongPollServer"
        params = {
            "v": "5.131",
            "group_id": self.app.config.bot.group_id,
            "access_token": self.app.config.bot.access_token,
        }
        async with self.session.get(API_PATH + method, params=params) as resp:
            data = (await resp.json())["response"]
            self.app.logger.info(data)
            self.key, self.server, self.ts = (
                data["key"],
                data["server"],
                data["ts"],
            )

    async def poll(self) -> list["UpdateObject"]:
        params = {
            "act": "a_check",
            "key": self.key,
            "ts": self.ts,
            "wait": 25,
        }
        async with self.session.get(self.server, params=params) as resp:
            data = await resp.json()
            self.app.logger.info(data)
            self.ts = data["ts"]

            return self.progress_updates(updates=data["updates"])

    def progress_updates(self, updates: dict) -> list["UpdateObject"]:
        return [self.app.store.factory.create(u) for u in updates]
