from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QListWidgetItem,
)
from pymongo import MongoClient

# Kết nối tới cơ sở dữ liệu MongoDB
client = MongoClient("localhost", 27017)
db = client["todo_app"]
todos_collection = db["todos"]


class Todo:
    def __init__(self, title, description):
        self.title = title
        self.description = description


class TodoListModel:
    def __init__(self):
        self.todos = []

    def add_todo(self, todo):
        self.todos.append(todo)

    def delete_todo(self, todo):
        self.todos.remove(todo)

    def get_all_todos(self):
        return self.todos

    def load_todos_from_db(self):
        self.todos = []
        for todo in todos_collection.find():
            self.todos.append(Todo(todo["title"], todo["description"]))


class TodoListView(QWidget):
    def __init__(self, todo_list_model):
        super().__init__()
        self.todo_list_model = todo_list_model

        self.layout = QVBoxLayout()
        self.todo_list = QListWidget()

        self.layout.addWidget(self.todo_list)
        self.setLayout(self.layout)

        self.refresh_list()

    def refresh_list(self):
        self.todo_list.clear()
        todos = self.todo_list_model.get_all_todos()
        for todo in todos:
            item = QListWidgetItem()
            item.setText(todo.title)
            self.todo_list.addItem(item)


class TodoController:
    def __init__(self, todo_list_model, todo_list_view):
        self.todo_list_model = todo_list_model
        self.todo_list_view = todo_list_view

    def add_todo_button_clicked(self):
        title = self.todo_list_view.title_input.text()
        description = self.todo_list_view.description_input.text()
        todo = Todo(title, description)
        self.todo_list_model.add_todo(todo)
        todos_collection.insert_one({"title": title, "description": description})
        self.todo_list_view.refresh_list()

    def delete_todo_button_clicked(self):
        selected_items = self.todo_list_view.todo_list.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            todo = self.todo_list_model.todos[selected_item.row()]
            self.todo_list_model.delete_todo(todo)
            todos_collection.delete_one(
                {"title": todo.title, "description": todo.description}
            )
            self.todo_list_view.refresh_list()


class MainWindow(QMainWindow):
    def __init__(self, todo_list_model, todo_list_view, todo_controller):
        super().__init__()
        self.setWindowTitle("Todo List App")
        self.resize(400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.title_label = QLabel("Title:")
        self.title_input = QLineEdit()
        self.description_label = QLabel("Description:")
        self.description_input = QLineEdit()

        self.add_button = QPushButton("Add Todo")
        self.delete_button = QPushButton("Delete Todo")

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.title_input)
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.description_input)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.delete_button)

        self.layout.addWidget(todo_list_view)

        self.add_button.clicked.connect(todo_controller.add_todo_button_clicked)
        self.delete_button.clicked.connect(todo_controller.delete_todo_button_clicked)


if __name__ == "__main__":
    app = QApplication([])

    todo_list_model = TodoListModel()
    todo_list_model.load_todos_from_db()

    todo_list_view = TodoListView(todo_list_model)
    todo_controller = TodoController(todo_list_model, todo_list_view)

    main_window = MainWindow(todo_list_model, todo_list_view, todo_controller)
    main_window.show()

    app.exec_()
