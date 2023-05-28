import typing as tp

from app.photocontest.photocontest.commands import setup_commands
from app.photocontest.photocontest.keyboards import setup_director
from app.photocontest.photocontest.messages import setup_messages


if tp.TYPE_CHECKING:
    from app.photocontest.web.app import Application
    from app.photocontest.photocontest.keyboards import BaseDirector
    from app.photocontest.photocontest.commands import BaseCommand
    from app.photocontest.photocontest.messages import BaseMessage


class AppContext:
    commands: tp.Optional[dict[str, "BaseCommand"]] = None
    message: tp.Optional["BaseMessage"] = None
    director: tp.Optional["BaseDirector"] = None


ctx = AppContext()


def setup_context(app: "Application"):
    setup_commands(app, ctx)
    setup_director(ctx)
    setup_messages(ctx)

    app.context = ctx
