from typing import Any

from PyQt5.QtWidgets import QDesktopWidget, QWidget, QMainWindow, QVBoxLayout


class MainView(QMainWindow):
    def __init__(self, controller):
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

        self.layout.addWidget(self.controller.todo_controller.todo_view)
        self.layout.addWidget(self.controller.todo_list_controller.todo_list_view)
