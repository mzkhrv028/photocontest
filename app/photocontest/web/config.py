import typing
from dataclasses import dataclass

from app.utils import parse

if typing.TYPE_CHECKING:
    from app.photocontest.web.app import Application


@dataclass
class DatabaseConfig:
    user: str
    password: str
    host: str
    port: str
    database: str

    @property
    def url(self) -> str:
        print(self.port, self.host)
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class GameConfig:
    timeout: int


@dataclass
class BotConfig:
    group_id: str
    access_token: str


@dataclass
class Config:
    database: DatabaseConfig = None
    bot: BotConfig = None
    game: GameConfig = None


def setup_config(app: "Application"):
    raw_config = parse.parse_config()

    app.config = Config(
        database=DatabaseConfig(**raw_config["database"]),
        bot=BotConfig(**raw_config["bot"]),
        game=GameConfig(**raw_config["game"]),
    )
