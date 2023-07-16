from typing import Any

from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
)


class BotView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.layout: Any = QVBoxLayout()

        self.add_edit_bot_button = QPushButton("Add/Edit bot")
        self.build_button = QPushButton("Build Bot")

        self.layout.addWidget(self.add_edit_bot_button)
        self.layout.addWidget(self.build_button)

        self.setLayout(self.layout)
