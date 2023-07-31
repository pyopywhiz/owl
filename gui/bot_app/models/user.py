from mongoengine import (
    StringField,
    DateTimeField,
    Document,
)
from datetime import datetime
from mongoengine import connect

connect("test_bot")


class User(Document):
    user_token = StringField()
    telegram_id = StringField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    expired_at = DateTimeField(default=datetime.now)
    registed_at = DateTimeField(default=datetime.now)
