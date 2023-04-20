import json
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
        self.payload = json.loads(self.payload).get("cmd", "")
        self.text = self.text.lower()


@dataclass
class Event:
    user_id: int
    peer_id: int
    event_id: str
    payload: dict
    event_data: str = ""
    conversation_message_id: int | None = None

    def __post_init__(self):
        self.payload = self.payload.get("cmd", "")


@dataclass
class UpdateObject:
    message: Message | None = None
    event: Event | None = None


@dataclass
class Update:
    type: str
    object: UpdateObject