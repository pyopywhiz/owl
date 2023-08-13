from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QListWidget, \
    QListWidgetItem
from mongoengine import Document, StringField, connect

# Connect to a local MongoDB instance
connect('todo_app')


class ToDo(Document):
    title = StringField(required=True)
    description = StringField()


class Observer:
    def update(self, *args, **kwargs):
        pass


class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, *args, **kwargs):
        for observer in self._observers:
            observer.update(*args, **kwargs)


class ToDoModel(Observable):
    def __init__(self):
        super().__init__()

    def create(self, title, description):
        todo = ToDo(title=title, description=description)
        todo.save()
        self.notify_observers('create', todo)

    def update(self, todo, title=None, description=None):
        if title:
            todo.title = title
        if description:
            todo.description = description
        todo.save()
        self.notify_observers('update', todo)

    def delete(self, todo):
        todo.delete()
        self.notify_observers('delete', todo)


class ToDoListView(QWidget, Observer):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.model.add_observer(self)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.title_input = QLineEdit(self)
        self.description_input = QTextEdit(self)
        create_button = QPushButton('Create ToDo', self)
        delete_button = QPushButton('Delete ToDo', self)

        layout.addWidget(self.title_input)
        layout.addWidget(self.description_input)
        layout.addWidget(create_button)
        layout.addWidget(self.list_widget)
        layout.addWidget(delete_button)

        create_button.clicked.connect(self.on_create)
        delete_button.clicked.connect(self.on_delete)

        self.setLayout(layout)
        self.populate_todos()

    def on_create(self):
        title = self.title_input.text()
        description = self.description_input.toPlainText()
        self.model.create(title, description)

    def on_delete(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            todo = current_item.data(Qt.UserRole)
            self.model.delete(todo)

    def populate_todos(self):
        for todo in ToDo.objects:
            item = QListWidgetItem(todo.title)
            item.setData(Qt.UserRole, todo)
            self.list_widget.addItem(item)

    def update(self, action, todo):
        if action == 'create':
            item = QListWidgetItem(todo.title)
            item.setData(Qt.UserRole, todo)
            self.list_widget.addItem(item)
        elif action == 'delete':
            items = self.list_widget.findItems(todo.title, Qt.MatchExactly)
            for item in items:
                self.list_widget.takeItem(self.list_widget.row(item))


if __name__ == '__main__':
    app = QApplication([])
    model = ToDoModel()
    view = ToDoListView(model)
    view.show()
    app.exec_()
