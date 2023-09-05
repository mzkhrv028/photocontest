import asyncio
from logging import Logger

from app.botsend.web.config import Config, setup_config
from app.botsend.web.logger import setup_logging
from app.botsend.web.store import Store, setup_store


class Application:
    config: Config | None = None
    logger: Logger | None = None
    store: Store | None = None


app = Application()


def setup_app(queue_send: asyncio.Queue) -> Application:
    setup_logging(app)
    setup_config(app)
    setup_store(app, queue_send)
    return app
