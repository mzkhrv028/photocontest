import asyncio
import typing as tp

from app.photocontest.web.context import setup_context
from app.photocontest.web.logger import setup_logging
from app.photocontest.web.config import setup_config
from app.photocontest.store import setup_store


if tp.TYPE_CHECKING:
    from logging import Logger
    from app.photocontest.store.database.database import Database
    from app.photocontest.web.config import Config
    from app.photocontest.store import Store
    from app.photocontest.web.context import AppContext


class Application:
    config: tp.Optional["Config"] = None
    database: tp.Optional["Database"] = None
    store: tp.Optional["Store"] = None
    logger: tp.Optional["Logger"] = None
    context: tp.Optional["AppContext"] = None


app = Application()


def setup_app(queue_poll: asyncio.Queue, queue_send: asyncio.Queue):
    setup_logging(app)
    setup_config(app)
    setup_store(app, queue_poll, queue_send)
    setup_context(app)
    return app
