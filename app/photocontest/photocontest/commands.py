import abc
import asyncio
import typing as tp
import collections

from app.botpoll.vkpoll.models import UpdateObject, Message, Event
from app.botsend.vksend.models import Snackbar
from app.photocontest.photocontest.decorators import GameDecorator


if tp.TYPE_CHECKING:
    from app.photocontest.web.app import Application
    from app.photocontest.web.context import AppContext
    from app.photocontest.store.vkapi.models import UserAccount
    from app.photocontest.photocontest.models import User


class BaseCommand(GameDecorator, abc.ABC):
    def __init__(self, app: "Application") -> None:
        self.app = app
        self.commands_tasks: list[asyncio.Task] = []

    async def __call__(self, update: "UpdateObject") -> None:
        await self.execute(update)

    @abc.abstractmethod
    async def execute(self, update: "UpdateObject") -> None:
        raise NotImplementedError


class MenuCommand(BaseCommand):
    @GameDecorator.check_progress
    async def execute(self, message: "Message") -> None:
        message.text = self.app.context.message.text.welcome()
        message.keyboard = self.app.context.director.keyboard.make_menu()
        
        self.app.store.queue_send.put_nowait(message)


class StartCommand(BaseCommand):
    @GameDecorator.check_progress
    async def execute(self, message: "Message") -> None:
        message.text = self.app.context.message.text.before_confirme(self.app.config.game.timeout)
        message.keyboard = self.app.context.director.keyboard.make_confirme()

        self.app.store.queue_send.put_nowait(message)

        game = await self.app.store.handler.get_or_register_game(message.peer_id)
        await self.app.store.handler.update_state_game(game.chat_id, "progress")

        self.app.store.games[game.chat_id] = {}

        self.commands_tasks.append(asyncio.create_task(self._progress_confirmed_users(message)))

    @GameDecorator.delay
    async def _progress_confirmed_users(self, message: "Message") -> None:
        message.text = self.app.context.message.text.after_confirme(
            len(self.app.store.games[message.peer_id])
        )
        message.keyboard = self.app.context.director.keyboard.make_empty()

        self.app.store.queue_send.put_nowait(message)

        users = await self.app.store.handler.register_users(
            accounts=self.app.store.games[message.peer_id],
            chat_id=message.peer_id,
        )

        await self._play_game(message=message, users=users)

    async def _play_game(self, message: "Message", users: list["User"]) -> None:
        users = collections.deque(users)

        while len(users) > 1:
            n = len(users)

            for _ in range(n // 2):
                self.app.store.games[message.peer_id]["voters"] = []

                first, second = users.popleft(), users.popleft()
                winner = await self._play_round(message, first, second)
                users.append(winner)

    async def _play_round(self, message: "Message", first: "User", second: "User") -> None:
        message.attachments = [f"photo{user.photo_id}" for user in (first, second)]
        message.keyboard = self.app.context.director.keyboard.make_vote(first, second)
        message.text = "Выберите фотографию."

        self.app.store.queue_send.put_nowait(message)


class ConfirmeCommand(BaseCommand):
    async def execute(self, event: "Event") -> None:
        user_account = await self.app.store.vkapi.get_user_account(event.user_id)
        
        if user_account.photo_id:
            snackbar_text = self._success_snackbar(event, user_account)
        else:
            snackbar_text = self._failed_snackbar(user_account)

        event.event_data = Snackbar(text=snackbar_text).dumps()
        self.app.store.queue_send.put_nowait(event)
    
    def _success_snackbar(self, event: "Event", user_account: "UserAccount") -> str:
        if event.user_id in self.app.store.games[event.peer_id]:
            return self.app.context.message.snackbar.already_confirmed()
        
        self.app.store.games[event.peer_id][event.user_id] = user_account
        return self.app.context.message.snackbar.confirmed()
        
    def _failed_snackbar(self, user_account: "UserAccount") -> str:
        snackbar_text = self.app.context.message.snackbar.cancelled()

        if user_account.is_closed:
            snackbar_text += self.app.context.message.snackbar.closed_profile()

        if not user_account.has_photo:
            snackbar_text += self.app.context.message.snackbar.no_photo()

        return snackbar_text


class CancelCommand(BaseCommand):
    async def execute(self, event: "Event") -> None:
        snackbar_text = self.app.context.message.snackbar.cancelled()

        if event.user_id in self.app.store.games[event.peer_id]:
            del self.app.store.games[event.peer_id][event.user_id]

        event.event_data = Snackbar(text=snackbar_text).dumps()
        self.app.store.queue_send.put_nowait(event)


class VoteCommand(BaseCommand):
    async def execute(self, event: "Event") -> None:
        chat = self.app.store.games[event.peer_id]

        if not event.user_id in chat:
            return None
        
        if event.user_id in chat["voters"]:
            pass




def setup_commands(app: "Application", context: "AppContext"):
    commands = {}

    commands["/"] = MenuCommand(app)
    commands["start"] = StartCommand(app)
    commands["confirme"] = ConfirmeCommand(app)
    commands["cancel"] = CancelCommand(app)
    commands["vote"] = VoteCommand(app)

    context.commands = commands
