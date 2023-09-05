from dataclasses import dataclass, field


@dataclass
class UserAccount:
    user_id: int
    first_name: str
    last_name: str
    can_access_closed: bool
    is_closed: bool
    has_photo: bool
    photo_id: str | None = None


@dataclass
class Button:
    type: str
    label: str
    payload: dict[str, str]

    @property
    def asdict(self):
        return {
            "action": {
                "type": self.type,
                "label": self.label,
                "payload": self.payload,
            }
        }


@dataclass
class Keyboard:
    one_time: bool = False
    inline: bool = False
    buttons: list[list[Button]] = field(default_factory=list[Button])
