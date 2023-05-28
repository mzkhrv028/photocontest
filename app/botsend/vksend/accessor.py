import json
import random
import typing as tp

from aiohttp import TCPConnector
from aiohttp.client import ClientSession

from app.botpoll.vkpoll.models import Event, Message


if tp.TYPE_CHECKING:
    from app.botsend.web.app import Application


API_PATH = "https://api.vk.com/method/"


class VkSendAccessor:
    def __init__(self, app: "Application") -> None:
        self.app = app
        self.session: ClientSession | None = None

    async def connect(self) -> None:
        self.app.logger.info("CONNECT ACCESSOR")
        self.session = ClientSession(connector=TCPConnector(verify_ssl=False))

    async def disconnect(self) -> None:
        if self.session:
            await self.session.close()

    async def send_message(self, message: Message) -> None:
        method = "messages.send"
        params = {
            "v": "5.131",
            "access_token": self.app.config.bot.access_token,
            "group_id": self.app.config.bot.group_id,
            "message": message.text,
            "attachment": ",".join(message.attachments),
            "random_id": random.randint(1, 2**32),
            "peer_id": message.peer_id,
            "keyboard": json.dumps(message.keyboard),
        }
        async with self.session.get(API_PATH + method, params=params) as resp:
            data = await resp.json()
            self.app.logger.info(data)

    async def send_event_answer(self, event: Event) -> None:
        method = "messages.sendMessageEventAnswer"
        params = {
            "v": "5.131",
            "access_token": self.app.config.bot.access_token,
            "event_id": event.event_id,
            "user_id": event.user_id,
            "peer_id": event.peer_id,
            "event_data": event.event_data,
        }
        async with self.session.get(API_PATH + method, params=params) as resp:
            data = await resp.json()
            self.app.logger.info(data)
