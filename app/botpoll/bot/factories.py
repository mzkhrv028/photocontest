from app.botpoll.vkpoll.models import UpdateObject, Message, Event


class UpdateFactory:
    def create(self, data: dict) -> UpdateObject | None:
        update_object = None

        match data["type"]:
            case "message_new":
                update_object = Message(**data["object"]["message"])
            case "message_event":
                update_object = Event(**data["object"])

        return update_object
