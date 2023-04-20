import typing as tp

if tp.TYPE_CHECKING:
    from app.photocontest.web.context import AppContext


class BaseMessage:
    def __init__(self) -> None:
        self.text = TextMessage()
        self.label = ButtonLabel()
        self.payload = Payload()
        self.snackbar = Snackbar()


class TextMessage:
    def welcome(self) -> str:
        return "Игра фотоконкурс"

    def menu(self) -> str:
        return "Начать игру"

    def before_confirme(self, timeout: int) -> str:
        return f"Подтвердите участие в течение {timeout} секунд!"

    def after_confirme(self) -> str:
        return "Подтверждение окончено. "

    def already_started(self) -> str:
        return "Игра уже идёт. Подождите завершения."
    
    def error_notenough(self) -> str:
        return "Недостаточно участников."


class ButtonLabel:
    def menu(self) -> str:
        return "Начать игру"

    def confirme(self) -> str:
        return "Подтвердить"

    def cancel(self) -> str:
        return "Отменить"


class Payload:
    def start(self) -> str:
        return "start"

    def confirme(self) -> str:
        return "confirme"

    def cancel(self) -> str:
        return "cancel"


class Snackbar:
    def confirmed(self) -> str:
        return "Участие в игре принято."

    def cancelled(self) -> str:
        return "Участие в игре отменено. "

    def already_confirmed(self) -> str:
        return "Ваше участие уже принято."

    def error_profile(self) -> str:
        return "Профиль закрыт. "

    def error_photo(self) -> str:
        return "Отсутствует фото профиля. "


def setup_messages(context: "AppContext"):
    context.message = BaseMessage()
