from typing import Any

from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QWidget, QVBoxLayout

from gui.todo_app.views.todo_view import TodoView


class MainView(QMainWindow):
    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller

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

        todo_view = TodoView()

        self.layout.addWidget(todo_view)
        self.setLayout(self.layout)

