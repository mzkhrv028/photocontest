import asyncio
import typing as tp

if tp.TYPE_CHECKING:
    from app.botpoll.vkpoll.models import Message


class GameDecorator:
    def check_progress(command: tp.Coroutine) -> tp.Coroutine:
        async def wrapper(self, message: "Message") -> tp.Coroutine:
            state_game = await self.app.store.handler.get_state_game(message.peer_id)

            if state_game == "progress":
                message.text = self.app.context.message.text.already_started()
                self.app.store.queue_send.put_nowait(message)
                return None

            return await command(self, message)

        return wrapper

    def delay(command: tp.Coroutine) -> tp.Coroutine:
        async def wrapper(self) -> tp.Coroutine:
            await asyncio.sleep(self.app.config.game.timeout)
            return await command(self)

        return wrapper

    def check_quantity(command: tp.Coroutine) -> tp.Coroutine:
        async def wrapper(self, message: "Message") -> tp.Coroutine:
            if len(self.app.store.chats[message.peer_id]) < 2:
                message.text = self.app.context.message.text.error_notenough()
                message.keyboard = self.app.context.director.keyboard.make_menu()

                await self.app.store.handler.update_state_game(message.peer_id, None)

                self.app.store.queue_send.put_nowait(message)
                return None

            return await command(self, message)

        return wrapper
