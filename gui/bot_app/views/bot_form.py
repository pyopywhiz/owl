from typing import Any, Tuple

from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QVBoxLayout,
)
from gui.bot_app.models.bot_model import Bot
from typing import Optional


class BotForm(QDialog):
    def __init__(self, bot: Optional[Bot] = None) -> None:
        super().__init__()
        self.setWindowTitle("Edit Bot" if bot else "Add Bot")

        self.token_label = QLabel("Token:")
        self.token_input = QLineEdit()
        self.token_input.setText(bot.token if bot else "")

        self.chat_id_label = QLabel("Chat ID:")
        self.chat_id_input = QLineEdit()
        self.chat_id_input.setText(bot.chat_id if bot else "")

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout: Any = QVBoxLayout()
        self.layout.addWidget(self.token_label)
        self.layout.addWidget(self.token_input)
        self.layout.addWidget(self.chat_id_label)
        self.layout.addWidget(self.chat_id_input)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def get_inputs(self) -> Tuple[str, str]:
        return self.token_input.text(), self.chat_id_input.text()
