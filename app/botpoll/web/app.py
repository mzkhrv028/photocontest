import asyncio
from logging import Logger

from app.botpoll.web.config import Config, setup_config
from app.botpoll.web.logger import setup_logging
from app.botpoll.web.store import Store, setup_store


class Application:
    config: Config | None = None
    logger: Logger | None = None
    store: Store | None = None


app = Application()


def setup_app(queue_poll: asyncio.Queue) -> Application:
    setup_logging(app)
    setup_config(app)
    setup_store(app, queue_poll)
    return app
