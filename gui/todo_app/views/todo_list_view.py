from typing import Any

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QHeaderView


class TodoListView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.layout: Any = QVBoxLayout()
        self.todo_table = QTableView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(
            ["Object Id", "Title", "Description", "Completed"]
        )
        self.todo_table.setModel(self.model)
        self.todo_table.hideColumn(0)
        self.todo_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.layout.addWidget(self.todo_table)
        self.setLayout(self.layout)

    def register_controller(self, controller):
        self.controller = controller

        self.model.dataChanged.connect(self.controller.on_data_changed)

    def add_todo_to_view(self, todo):
        self.model.appendRow(
            [
                QStandardItem(str(todo.id)),
                QStandardItem(todo.title),
                QStandardItem(todo.description),
                QStandardItem("Yes" if todo.completed else "No"),
            ]
        )

    def remove_todo_from_view(self, index):
        self.model.removeRow(index)

    def update_todo_in_view(self, index, todo):
        self.model.item(index, 1).setText(todo.title)
        self.model.item(index, 2).setText(todo.description)
        self.model.item(index, 3).setText("Yes" if todo.completed else "No")

    def load_todos(self, todos) -> None:
        for todo in todos:
            self.model.appendRow(
                [
                    QStandardItem(str(todo.id)),
                    QStandardItem(todo.title),
                    QStandardItem(todo.description),
                    QStandardItem("Yes" if todo.completed else "No"),
                ]
            )
