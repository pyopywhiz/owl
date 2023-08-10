from typing import Any, Tuple

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QDialogButtonBox, QVBoxLayout


class AddTodoView(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Add/Edit Todo")

        self.title_label = QLabel("Title:")
        self.title_input = QLineEdit()

        self.description_label = QLabel("Description:")
        self.description_input = QLineEdit()

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

    def register_controller(self, controller):
        self.controller = controller

    def get_inputs(self) -> Tuple[str, str]:
        return self.title_input.text(), self.description_input.text()
