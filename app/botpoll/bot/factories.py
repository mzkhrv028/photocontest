from app.botpoll.vkpoll.models import Event, Message, Update, UpdateObject


class UpdateFactory:
    def create(self, data: dict) -> Update:
        update = Update(type=data["type"], object=UpdateObject())

        match update.type:
            case "message_new":
                update.object.message = Message(**data["object"]["message"])
            case "message_event":
                update.object.event = Event(**data["object"])       

        return update