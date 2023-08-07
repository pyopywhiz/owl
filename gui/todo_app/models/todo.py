from mongoengine import StringField, Document, ReferenceField, CASCADE, connect, BooleanField

from gui.bot_app.models.user import User


class Todo(Document):
    title = StringField()
    description = StringField()
    is_completed = BooleanField()
