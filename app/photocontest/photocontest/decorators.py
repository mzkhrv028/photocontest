import asyncio
import typing as tp


if tp.TYPE_CHECKING:
    from app.botpoll.vkpoll.models import Update



class GameDecorator:
    def check_progress(command: tp.Coroutine) -> tp.Coroutine:
        async def wrapper(self, update: "Update") -> tp.Coroutine:
            state_game = await self.app.store.handler.get_state_game(update.object.message.peer_id)
            if state_game == "progress":
                update.object.message.text = self.app.context.message.text.already_started()
                self.app.store.queue_send.put_nowait(update)
                return None
            return await command(self, update)

        return wrapper

    def delay(command: tp.Coroutine) -> tp.Coroutine:
        async def wrapper(self, update: "Update") -> tp.Coroutine:
            await asyncio.sleep(self.app.config.game.timeout_confirme)
            return await command(self, update)

        return wrapper

    def check_qty(command: tp.Coroutine) -> tp.Coroutine:
        async def wrapper(self, update: "Update") -> tp.Coroutine:
            if len(self.app.store.chats[update.object.message.peer_id]) < 2:
                update.object.message.text = self.app.context.message.text.error_notenough()
                update.object.message.keyboard = self.app.context.director.keyboard.make_menu()
                await self.app.store.handler.update_state_game(update.object.message.peer_id, None)
                self.app.store.queue_send.put_nowait(update)
                return None
            return await command(self, update)

        return wrapper
