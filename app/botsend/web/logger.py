import logging
import typing

if typing.TYPE_CHECKING:
    from app.botsend.web.app import Application


def setup_logging(app: "Application") -> None:
    logging.basicConfig(level=logging.INFO)
    app.logger = logging.getLogger("BOTSEND")
