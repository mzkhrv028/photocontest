import typing as tp

from aiohttp import ClientSession, TCPConnector

from app.photocontest.store.vkapi.models import UserAccount

if tp.TYPE_CHECKING:
    from app.photocontest.web.app import Application


API_PATH = "https://api.vk.com/method/"


class VkAccessor:
    def __init__(self, app: "Application") -> None:
        self.app = app
        self.session: ClientSession | None = None

    async def connect(self) -> None:
        self.app.logger.info("CONNECT ACCESSOR")
        self.session = ClientSession(connector=TCPConnector(verify_ssl=False))

    async def disconnect(self) -> None:
        if not self.session.closed:
            await self.session.close()

    async def get_user_account(self, user_id: int) -> UserAccount:
        method = "users.get"
        fields = "has_photo,photo_id"
        params = {
            "v": "5.131",
            "access_token": self.app.config.bot.access_token,
            "user_ids": str(user_id),
            "fields": fields,
        }
        async with self.session.get(API_PATH + method, params=params) as resp:
            data = (await resp.json())["response"]
            self.app.logger.info(data)
            return UserAccount(
                user_id=data[0]["id"],
                first_name=data[0]["first_name"],
                last_name=data[0]["last_name"],
                can_access_closed=data[0]["can_access_closed"],
                is_closed=data[0]["is_closed"],
                has_photo=data[0]["has_photo"],
                photo_id=data[0].get("photo_id", None),
            )
