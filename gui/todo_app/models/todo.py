from mongoengine import StringField, Document, BooleanField


class Todo(Document):
    title = StringField()
    description = StringField()
    is_completed = BooleanField()
