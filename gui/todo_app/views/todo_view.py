from typing import Any

from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout

from gui.todo_app.views.todo_list_view import TodoListView


class TodoView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout: Any = QVBoxLayout()

        add_button = QPushButton("Add todo")
        update_button = QPushButton("Update Todo")
        delete_button = QPushButton("Delete Todo")
        todo_list_view = TodoListView()

        self.layout.addWidget(add_button)
        self.layout.addWidget(update_button)
        self.layout.addWidget(delete_button)
        self.layout.addWidget(todo_list_view)
        self.setLayout(self.layout)
