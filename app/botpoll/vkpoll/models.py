import json
import typing as tp
from dataclasses import dataclass, field


@dataclass
class Message:
    peer_id: int
    text: str
    keyboard: str = ""
    payload: str = "{}"
    attachments: list = field(default_factory=list)
    date: int | None = None
    from_id: int | None = None
    id: int | None = None
    out: int | None = None
    conversation_message_id: int | None = None
    fwd_messages: list | None = None
    important: bool | None = None
    is_hidden: bool | None = None
    random_id: int | None = None

    def __post_init__(self):
        payload = json.loads(self.payload)
        self.payload = payload.get("cmd", "")


@dataclass
class Event:
    user_id: int
    peer_id: int
    event_id: str
    payload: dict
    event_data: str = ""
    conversation_message_id: int | None = None
    vote_id: int | None = field(init=False, default=None)

    def __post_init__(self):
        payload = self.payload
        self.vote_id = payload.get("vote_id", None)
        self.payload = payload.get("cmd", "")


UpdateObject = tp.TypeVar("UpdateObject", Message, Event)
