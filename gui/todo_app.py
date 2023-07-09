from typing import Any, Optional, Tuple

from bson import ObjectId
from pymongo import MongoClient
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import (
    QApplication,
    QDesktopWidget,
    QDialog,
    QDialogButtonBox,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

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


class TodoForm(QDialog):
    def __init__(self, title: str = "", description: str = "") -> None:
        super().__init__()
        self.setWindowTitle("Add/Edit Todo")

        self.title_label = QLabel("Title:")
        self.title_input = QLineEdit()
        self.title_input.setText(title)

        self.description_label = QLabel("Description:")
        self.description_input = QLineEdit()
        self.description_input.setText(description)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout: Any = QVBoxLayout()
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.title_input)
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.description_input)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def get_inputs(self) -> Tuple[str, str]:
        return self.title_input.text(), self.description_input.text()


class TodoListModel(QStandardItemModel):
    def __init__(self) -> None:
        super().__init__()
        self.setHorizontalHeaderLabels(
            ["Object Id", "Title", "Description", "Completed"]
        )
        self.load_todos_from_database()

    def add_todo(self, todo: Todo) -> None:
        self.appendRow(
            [
                QStandardItem(str(todo.object_id)),
                QStandardItem(todo.title),
                QStandardItem(todo.description),
                QStandardItem("Yes" if todo.completed else "No"),
            ]
        )
        todos_collection.insert_one(
            {
                "_id": todo.object_id,
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
            }
        )

    def update_todo(self, index: int, todo: Todo) -> None:
        item = self.item(index, 1)
        item.setText(todo.title)
        item = self.item(index, 2)
        item.setText(todo.description)
        item = self.item(index, 3)
        item.setText("Yes" if todo.completed else "No")
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
        item = self.takeRow(index)
        todos_collection.delete_one({"_id": ObjectId(item[0].text())})

    def load_todos_from_database(self) -> None:
        for todo in todos_collection.find():
            self.appendRow(
                [
                    QStandardItem(str(todo["_id"])),
                    QStandardItem(todo["title"]),
                    QStandardItem(todo["description"]),
                    QStandardItem("Yes" if todo["completed"] else "No"),
                ]
            )


class TodoListView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.layout: Any = QVBoxLayout()
        self.todo_table = QTableView()

        self.layout.addWidget(self.todo_table)
        self.setLayout(self.layout)

    def set_model(self, model: TodoListModel) -> None:
        self.todo_table.setModel(model)


class TodoController:
    def __init__(
        self, todo_list_model: TodoListModel, todo_list_view: TodoListView
    ) -> None:
        self.todo_list_model = todo_list_model
        self.todo_list_view = todo_list_view

    def add_todo_button_clicked(self) -> None:
        self.show_todo_form()

    def update_todo_button_clicked(self) -> None:
        index = self.todo_list_view.todo_table.currentIndex().row()
        if index >= 0:
            todo = Todo(
                ObjectId(self.todo_list_model.item(index, 0).text()),
                self.todo_list_model.item(index, 1).text(),
                self.todo_list_model.item(index, 2).text(),
                self.todo_list_model.item(index, 3).text() == "Yes",
            )
            self.show_todo_form(todo)

    def delete_todo_button_clicked(self) -> None:
        index = self.todo_list_view.todo_table.currentIndex().row()
        if index >= 0:
            self.todo_list_model.delete_todo(index)

    def complete_todo_button_clicked(self) -> None:
        index = self.todo_list_view.todo_table.currentIndex().row()
        if index >= 0:
            todo = Todo(
                ObjectId(self.todo_list_model.item(index, 0).text()),
                self.todo_list_model.item(index, 1).text(),
                self.todo_list_model.item(index, 2).text(),
                True,
            )
            self.todo_list_model.update_todo(index, todo)

    def show_todo_form(self, todo: Optional[Todo] = None) -> None:
        if todo is None:
            todo_form = TodoForm()
        else:
            todo_form = TodoForm(todo.title, todo.description)

        result = todo_form.exec()

        if result == QDialog.Accepted:
            title, description = todo_form.get_inputs()
            if todo is None:
                self.todo_list_model.add_todo(
                    Todo(
                        ObjectId(),
                        title,
                        description,
                    )
                )
            else:
                updated_todo = Todo(
                    todo.object_id,
                    title,
                    description,
                    todo.completed,
                )
                index = self.todo_list_view.todo_table.currentIndex().row()
                self.todo_list_model.update_todo(index, updated_todo)

    def data_changed(self, index: Any) -> None:
        row = index.row()

        object_id = ObjectId(self.todo_list_model.item(row, 0).text())
        title = self.todo_list_model.item(row, 1).text()
        description = self.todo_list_model.item(row, 2).text()
        completed = self.todo_list_model.item(row, 3).text() == "Yes"

        updated_todo = Todo(
            object_id,
            title,
            description,
            completed,
        )
        self.todo_list_model.update_todo(row, updated_todo)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Todo List App")
        self.resize(600, 600)

        qr_value = self.frameGeometry()
        cp_value = QDesktopWidget().availableGeometry().center()
        qr_value.moveCenter(cp_value)
        self.move(qr_value.topLeft())

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout: Any = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.todo_list_view = TodoListView()

        self.add_button = QPushButton("Add todo")
        self.update_button = QPushButton("Update Todo")
        self.delete_button = QPushButton("Delete Todo")
        self.complete_button = QPushButton("Complete Todo")

        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.complete_button)
        self.layout.addWidget(self.todo_list_view)

        self.todo_list_model = TodoListModel()
        self.todo_list_view.set_model(self.todo_list_model)
        self.todo_list_view.todo_table.hideColumn(0)
        self.todo_list_view.todo_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.todo_controller = TodoController(self.todo_list_model, self.todo_list_view)

        self.todo_list_model.dataChanged.connect(self.todo_controller.data_changed)
        self.add_button.clicked.connect(self.todo_controller.add_todo_button_clicked)
        self.update_button.clicked.connect(
            self.todo_controller.update_todo_button_clicked
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
