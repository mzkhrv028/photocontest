import abc
import asyncio
import json
import typing as tp

from app.photocontest.photocontest.decorators import GameDecorator

if tp.TYPE_CHECKING:
    from app.botpoll.vkpoll.models import Event, Update
    from app.photocontest.web.app import Application
    from app.photocontest.web.context import AppContext
    from app.photocontest.store.vkapi.models import UserAccount


class BaseCommand(GameDecorator, abc.ABC):
    def __init__(self, app: "Application") -> None:
        self.app = app
        self.commands_tasks: list[asyncio.Task] = []

    async def __call__(self, update: "Update") -> None:
        await self.execute(update)

    @abc.abstractmethod
    async def execute(self, update: "Update") -> None:
        raise NotImplementedError


class MenuCommand(BaseCommand):
    @GameDecorator.check_progress
    async def execute(self, update: "Update") -> None:
        update.object.message.text = self.app.context.message.text.welcome()
        update.object.message.keyboard = self.app.context.director.keyboard.make_menu()
        self.app.store.queue_send.put_nowait(update)


class StartCommand(BaseCommand):
    @GameDecorator.check_progress
    async def execute(self, update: "Update") -> None:
        await self.app.store.handler.update_state_game(update.object.message.peer_id, "progress")
        update.object.message.text = self.app.context.message.text.before_confirme(
            self.app.config.game.timeout_confirme
        )
        update.object.message.keyboard = self.app.context.director.keyboard.make_confirme()
        self.commands_tasks.append(asyncio.create_task(self.progress_confirmed_users(update)))
        self.app.store.chats[update.object.message.peer_id] = {}
        self.app.store.queue_send.put_nowait(update)

    @GameDecorator.delay
    @GameDecorator.check_qty
    async def progress_confirmed_users(self, update: "Update") -> None:
        update.object.message.text = (
            self.app.context.message.text.after_confirme()
            + f"Кол-во участников {len(self.app.store.chats[update.object.message.peer_id])}."
        )
        update.object.message.keyboard = self.keyboard_director.make_empty()
        self.app.store.queue_send.put_nowait(update)
        self.app.logger.info(self.app.store.chats)
        users = await self.app.store.handler.register_users(
            accounts=self.app.store.chats[update.object.message.peer_id],
            chat_id=update.object.message.peer_id,
        )


class ConfirmeCommand(BaseCommand):
    async def execute(self, update: "Update") -> None:
        user_account = await self.app.store.vkapi.get_user_account(update.object.event.user_id)
        snackbar_text = self.get_snackbar_text(update.object.event, user_account)
        if (
            user_account.photo_id
            and update.object.event.user_id not in self.app.store.chats[update.object.event.peer_id]
        ):
            self.app.store.chats[update.object.event.peer_id][update.object.event.user_id] = user_account
        ## TODO: Переделать dumps
        update.object.event.event_data = json.dumps({"type": "show_snackbar", "text": snackbar_text})
        self.app.store.queue_send.put_nowait(update)

    def get_snackbar_text(self, event: "Event", user_account: "UserAccount") -> str:
        if event.user_id in self.app.store.chats[event.peer_id]:
            return self.app.context.message.snackbar.already_confirmed()
        if user_account.photo_id:
            return self.app.context.message.snackbar.confirmed()
        else:
            snackbar_text = self.app.context.message.snackbar.cancelled()
        if user_account.is_closed:
            snackbar_text += self.app.context.message.snackbar.error_profile()
        if not user_account.has_photo:
            snackbar_text += self.app.context.message.snackbar.error_photo()
        return snackbar_text


class CancelCommand(BaseCommand):
    async def execute(self, update: "Update") -> None:
        if update.object.event.user_id in self.app.store.chats[update.object.event.peer_id]:
            snackbar_text = self.app.context.message.snackbar.already_confirmed()
        else:
            snackbar_text = self.app.context.message.snackbar.cancelled()
        update.object.event.event_data = json.dumps({"type": "show_snackbar", "text": snackbar_text})
        self.app.store.queue_send.put_nowait(update)


def setup_commands(app: "Application", context: "AppContext"):
    commands = {}

    commands["/"] = MenuCommand(app)
    commands["start"] = StartCommand(app)
    commands["confirme"] = ConfirmeCommand(app)
    commands["cancel"] = CancelCommand(app)

    context.commands = commands
