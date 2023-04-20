import typing
from dataclasses import dataclass

from app.utils import parse

if typing.TYPE_CHECKING:
    from app.botsend.web.app import Application


@dataclass
class BotConfig:
    group_id: str
    access_token: str


@dataclass
class Config:
    bot: BotConfig = None


def setup_config(app: "Application") -> None:
    raw_config = parse.parse_config()

    app.config = Config(
        bot=BotConfig(**raw_config["bot"]),
    )
