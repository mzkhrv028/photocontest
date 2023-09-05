import json
from dataclasses import dataclass, field


@dataclass
class Snackbar:
    text: str
    type: str = field(init=False, default="show_snackbar")

    def dumps(self):
        return json.dumps({"type": self.type, "text": self.text})
