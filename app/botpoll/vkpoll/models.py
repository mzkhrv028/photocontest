import json
import typing as tp
from dataclasses import dataclass, field


@dataclass
class Message:
    date: int
    from_id: int
    id: int
    out: int
    attachments: list
    conversation_message_id: int
    fwd_messages: list
    important: bool
    is_hidden: bool
    peer_id: int
    random_id: int
    text: str
    keyboard: str = ""
    payload: str = "{}"

    def __post_init__(self):
        payload = json.loads(self.payload)
        self.payload = payload.get("cmd", "")
        self.text = self.text.lower()


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