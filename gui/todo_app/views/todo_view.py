from typing import Any

from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout


class TodoView(QWidget):
    def __init__(self):
        super().__init__()
        self.add_button = QPushButton("Add todo")
        self.update_button = QPushButton("Update Todo")
        self.delete_button = QPushButton("Delete Todo")
        self.complete_button = QPushButton("Complete Todo")

        self.layout: Any = QVBoxLayout()

        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.complete_button)

        self.setLayout(self.layout)

    def register_todo_controller(self, todo_controller):
        self.todo_controller = todo_controller

        self.add_button.clicked.connect(self.todo_controller.on_add_todo)
        self.update_button.clicked.connect(self.todo_controller.on_update_todo)
        self.delete_button.clicked.connect(self.todo_controller.on_delete_todo)
        self.complete_button.clicked.connect(self.todo_controller.on_complete_todo)
