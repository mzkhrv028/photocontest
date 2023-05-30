import typing as tp
from dataclasses import asdict

from app.photocontest.store.vkapi.models import Button, Keyboard
from app.photocontest.photocontest.models import User
from app.photocontest.photocontest.messages import ButtonLabel, Payload


if tp.TYPE_CHECKING:
    from app.photocontest.web.context import AppContext


class BaseDirector:
    def __init__(self) -> None:
        self.keyboard = KeyboardDirector()


class KeyboardDirector:
    def __init__(self) -> None:
        self.__builder = KeyboardBuilder()
        self.__label = ButtonLabel()
        self.__payload = Payload()

    def make_empty(self) -> dict[str, tp.Any]:
        self.__builder.reset()

        return asdict(self.__builder.keyboard)

    def make_menu(self) -> dict[str, tp.Any]:
        self.__builder.reset()
        self.__builder.set_inline(False)
        self.__builder.set_onetime(False)

        buttons = [
            Button(
                type="text",
                label=self.__label.menu(),
                payload={"cmd": self.__payload.start()},
            ),
        ]

        self.__builder.add_buttons(buttons=buttons)

        return asdict(self.__builder.keyboard)

    def make_vote(self, users: list[User]) -> dict[str, tp.Any]:
        self.__builder.reset()
        self.__builder.set_inline(True)
        self.__builder.set_onetime(False)

        buttons = [
            Button(
                type="callback",
                label=user.first_name,
                payload={
                    "cmd": self.__payload.vote(),
                    "vote_id": user.user_id,
                },
            )
            for user in users
        ]

        self.__builder.add_buttons(buttons=buttons)

        return asdict(self.__builder.keyboard)

    def make_confirme(self) -> dict[str, tp.Any]:
        self.__builder.reset()
        self.__builder.set_inline(False)
        self.__builder.set_onetime(False)

        buttons = [
            Button(
                type="callback",
                label=self.__label.confirme(),
                payload={"cmd": self.__payload.confirme()},
            ),
            Button(
                type="callback",
                label=self.__label.cancel(),
                payload={"cmd": self.__payload.cancel()},
            ),
        ]

        self.__builder.add_buttons(buttons=buttons)

        return asdict(self.__builder.keyboard)


class KeyboardBuilder:
    def __init__(self) -> None:
        self.keyboard: tp.Optional[Keyboard] = None

    def reset(self) -> None:
        self.keyboard = Keyboard()

    def set_onetime(self, one_time: bool) -> None:
        self.keyboard.one_time = one_time

    def set_inline(self, inline: bool) -> None:
        self.keyboard.inline = inline

    def add_buttons(self, buttons: list[Button]) -> None:
        self.keyboard.buttons.append([btn.asdict for btn in buttons])


def setup_director(context: "AppContext"):
    context.director = BaseDirector()
