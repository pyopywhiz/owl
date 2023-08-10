from mongoengine import StringField, Document, BooleanField


class Todo(Document):
    title = StringField()
    description = StringField()
    completed = BooleanField(default=False)
