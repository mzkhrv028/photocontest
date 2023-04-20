import typing

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.photocontest.store.database.sqlalchemy_base import Base

if typing.TYPE_CHECKING:
    from app.photocontest.web.app import Application


class Database:
    def __init__(self, app: "Application"):
        self.app = app
        self._engine: AsyncEngine | None = None
        self._db: DeclarativeBase | None = None
        self.sessionmaker: async_sessionmaker | None = None

    async def connect(self, *_: list, **__: dict) -> None:
        self._db = Base
        self._engine = create_async_engine(self.app.config.database.url, echo=True)
        self.sessionmaker = async_sessionmaker(self._engine, expire_on_commit=False)

    async def disconnect(self, *_: list, **__: dict) -> None:
        if self._engine:
            await self._engine.dispose()
