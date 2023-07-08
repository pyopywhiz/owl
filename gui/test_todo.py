from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QListWidgetItem,
)
from typing import Any, List
from bson import ObjectId
from pymongo import MongoClient


client: Any = MongoClient(
    "mongodb+srv://hungdhv97:hung23081997@cluster0.pxjti4x.mongodb.net/"
)
database: Any = client["todo_app"]
todos_collection: Any = database["todos"]


class Todo:
    def __init__(
        self,
        object_id: ObjectId,
        title: str,
        description: str,
        completed: bool = False,
    ) -> None:
        self.object_id = object_id
        self.title = title
        self.description = description
        self.completed = completed


class TodoListModel:
    def __init__(self) -> None:
        self.todos: List[Todo] = []

    def create_todo(self, todo: Todo) -> None:
        self.todos.append(todo)
        todos_collection.insert_one(
            {
                "_id": todo.object_id,
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
            }
        )

    def get_todo(self, index: int) -> Todo:
        return self.todos[index]

    def get_todos(self) -> List[Todo]:
        return self.todos

    def update_todo(self, index: int, todo: Todo) -> None:
        self.todos[index] = todo
        todos_collection.update_one(
            {"_id": todo.object_id},
            {
                "$set": {
                    "title": todo.title,
                    "description": todo.description,
                    "completed": todo.completed,
                }
            },
        )

    def delete_todo(self, index: int) -> None:
        todo = self.todos[index]
        del self.todos[index]
        todos_collection.delete_one({"_id": todo.object_id})

    def load_todos_from_database(self) -> None:
        self.todos = []
        for todo in todos_collection.find():
            self.todos.append(
                Todo(todo["_id"], todo["title"], todo["description"], todo["completed"])
            )


class TodoListView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.layout: Any = QVBoxLayout()
        self.todo_list = QListWidget()

        self.layout.addWidget(self.todo_list)
        self.setLayout(self.layout)

    def refresh_list(self, todos: List[Todo]) -> None:
        self.todo_list.clear()
        for todo in todos:
            item = QListWidgetItem()
            item.setText(todo.title)
            self.todo_list.addItem(item)


class TodoController:
    def __init__(
        self, todo_list_model: TodoListModel, todo_list_view: TodoListView
    ) -> None:
        self.todo_list_model = todo_list_model
        self.todo_list_view = todo_list_view

    def add_todo_button_clicked(self, todo: Todo) -> None:
        self.todo_list_model.create_todo(todo)
        self.todo_list_view.refresh_list(self.todo_list_model.get_todos())

    def delete_todo_button_clicked(self) -> None:
        indexes = self.todo_list_view.todo_list.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            self.todo_list_model.delete_todo(row)
            self.todo_list_view.refresh_list(self.todo_list_model.get_todos())

    def complete_todo_button_clicked(self) -> None:
        indexes = self.todo_list_view.todo_list.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            todo = self.todo_list_model.get_todo(row)
            todo.completed = True
            self.todo_list_model.update_todo(row, todo)
            self.todo_list_view.refresh_list(self.todo_list_model.get_todos())


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Todo List App")
        self.resize(400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout: Any = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.title_label = QLabel("Title:")
        self.title_input = QLineEdit()
        self.description_label = QLabel("Description:")
        self.description_input = QLineEdit()
        self.todo_list_view = TodoListView()

        self.add_button = QPushButton("Add todo")
        self.delete_button = QPushButton("Delete Todo")
        self.complete_button = QPushButton("Complete Todo")

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.title_input)
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.description_input)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.complete_button)
        self.layout.addWidget(self.todo_list_view)

        self.todo_list_model = TodoListModel()
        self.todo_list_model.load_todos_from_database()
        self.todo_list_view.refresh_list(self.todo_list_model.get_todos())
        self.todo_controller = TodoController(self.todo_list_model, self.todo_list_view)

        self.add_button.clicked.connect(
            lambda: self.todo_controller.add_todo_button_clicked(
                Todo(
                    ObjectId(),
                    self.title_input.text(),
                    self.description_input.text(),
                )
            )
        )
        self.delete_button.clicked.connect(
            self.todo_controller.delete_todo_button_clicked
        )
        self.complete_button.clicked.connect(
            self.todo_controller.complete_todo_button_clicked
        )


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()
    app.exec()
