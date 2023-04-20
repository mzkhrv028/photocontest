import typing
from dataclasses import dataclass

from app.utils import parse

if typing.TYPE_CHECKING:
    from app.photocontest.web.app import Application


@dataclass
class DatabaseConfig:
    user: str = "postgres"
    password: str = "postgres"
    host: str = "localhost"
    port: int = 5432
    database: str = "project"

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class GameConfig:
    timeout_confirme: int


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
