from mongoengine import StringField, Document, ReferenceField, CASCADE, connect
from gui.bot_app.models.user import User

connect("test_bot")


class Bot(Document):
    token = StringField()
    chat_id = StringField()
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
