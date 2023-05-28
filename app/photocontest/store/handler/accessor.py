import typing as tp

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.photocontest.photocontest.models import Game, User
from app.photocontest.store.vkapi.models import UserAccount


if tp.TYPE_CHECKING:
    from app.photocontest.web.app import Application


class HandlerAccessor:
    def __init__(self, app: "Application") -> None:
        self.app = app

    async def get_users_from_accounts(self, user_accounts: dict[int, UserAccount]) -> list[User] | None:
        async with self.app.database.sessionmaker() as session:
            stmt = select(User).where(User.user_id.in_(user_accounts)).options(selectinload(User.games))
            users = (await session.execute(stmt)).scalars().all()
        return users

    async def get_state_game(self, chat_id: int) -> str:
        async with self.app.database.sessionmaker() as session:
            stmt = select(Game).filter_by(chat_id=chat_id)
            game: Game = (await session.execute(stmt)).scalars().first()
        return game.state if game else None

    async def update_state_game(self, chat_id: int, state: str) -> Game | None:
        async with self.app.database.sessionmaker.begin() as session:
            stmt = select(Game).filter_by(chat_id=chat_id)
            game: Game = (await session.execute(stmt)).scalars().first()
            game.state = state
            
            session.add(game)
        return game

    async def get_or_register_game(self, chat_id: int) -> Game:
        async with self.app.database.sessionmaker() as session:
            stmt = select(Game).filter_by(chat_id=chat_id).options(selectinload(Game.users))
            game = (await session.execute(stmt)).scalars().first()

            if game is None:
                game = Game(chat_id=chat_id)

                session.add(game)
                await session.commit()

        return game
    
    async def cancel_all_game(self) -> None:
        async with self.app.database.sessionmaker.begin() as session:
            stmt = select(Game).filter_by(state="progress")
            games: list[Game] = (await session.execute(stmt)).scalars().unique().all()
            
            for game in games:
                game.state = None

            session.add_all(games)

    async def register_users(self, accounts: dict[int, UserAccount], chat_id: int) -> list[User]:
        async with self.app.database.sessionmaker.begin() as session:
            users = await self.get_users_from_accounts(accounts)
            game = await self.get_or_register_game(chat_id)

            self._update_users(game, users, accounts)
            self._create_users(game, users, accounts)

            session.add_all(users)

        return users

    def _update_users(self, game: Game, users: list[User], accounts: dict[int, UserAccount]) -> None:
        for user in users:
            account = accounts[user.user_id]

            user.first_name = account.first_name
            user.last_name = account.last_name
            user.photo_id = account.photo_id

            if not any(filter(lambda u: u.user_id == user.user_id, game.users)):
                user.games.append(game)

            del accounts[user.user_id]

    def _create_users(self, game: Game, users: list[User], accounts: dict[int, UserAccount]) -> None:
        for account in accounts.values():
            user = User(
                user_id=account.user_id,
                first_name=account.first_name,
                last_name=account.last_name,
                photo_id=account.photo_id,
            )

            user.games.append(game)
            users.append(user)
