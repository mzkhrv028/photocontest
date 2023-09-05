from sqlalchemy import BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.photocontest.store.database.sqlalchemy_base import Base


class GameSession(Base):
    __tablename__ = "sessions"
    __table_args__ = (UniqueConstraint("user_id", "chat_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger(), ForeignKey("users.user_id")
    )
    chat_id: Mapped[int] = mapped_column(
        BigInteger(), ForeignKey("games.chat_id")
    )
    round: Mapped[int] = mapped_column(default=0)
    score: Mapped[int] = mapped_column(default=0)

    def __init__(self, round_: int, score: int):
        self.round = round_
        self.score = score


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger(), unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    photo_id: Mapped[str]
    wins: Mapped[int] = mapped_column(default=0)
    games: Mapped[list["Game"]] = relationship(
        init=False, secondary="sessions", back_populates="users", lazy="joined"
    )


class Game(Base):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger(), unique=True)
    users: Mapped[list["User"]] = relationship(
        init=False, secondary="sessions", back_populates="games", lazy="joined"
    )
    state: Mapped[str | None] = mapped_column(default=None)
