import sys
from typing import Dict

from pymongo import MongoClient
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
)


class BotInformationDialog(QDialog):
    def __init__(self, bot_info: Dict[str, str] = None) -> None:
        super().__init__()

        self.setWindowTitle("Bot Information")
        self.setFixedSize(300, 200)

        self.bot_info = bot_info

        # Bot Information
        self.id_line_edit: QLineEdit = QLineEdit()
        self.bot_token_line_edit: QLineEdit = QLineEdit()
        self.chat_id_line_edit: QLineEdit = QLineEdit()

        # If bot_info is provided, populate the fields with its values
        if bot_info:
            self.id_line_edit.setText(bot_info["id"])
            self.bot_token_line_edit.setText(bot_info["bot_token"])
            self.chat_id_line_edit.setText(bot_info["chat_id"])

        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("ID:"))
        layout.addWidget(self.id_line_edit)
        layout.addWidget(QLabel("Bot Token:"))
        layout.addWidget(self.bot_token_line_edit)
        layout.addWidget(QLabel("Chat ID:"))
        layout.addWidget(self.chat_id_line_edit)

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def accept(self) -> None:
        bot_info: Dict[str, str] = {
            "id": self.id_line_edit.text(),
            "bot_token": self.bot_token_line_edit.text(),
            "chat_id": self.chat_id_line_edit.text(),
        }
        self.bot_info = bot_info
        super().accept()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("MongoDB GUI")
        self.setFixedSize(400, 300)

        # MongoDB connection
        self.client: MongoClient[Dict[str, str]] = MongoClient(
            "mongodb://localhost:27017/"
        )
        self.database = self.client["bot_db"]
        self.collection = self.database["bot_collection"]

        # Main widget
        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        # Layout
        main_layout = QVBoxLayout()
        self.widget.setLayout(main_layout)

        # Buttons
        self.load_button = QPushButton("Load Bot")
        self.load_button.clicked.connect(self.open_bot_information_dialog)
        main_layout.addWidget(self.load_button)

        # Console
        self.console = QLabel()
        main_layout.addWidget(QLabel("Console"))
        main_layout.addWidget(self.console)

    def log_message(self, message: str) -> None:
        self.console.setText(message)

    def open_bot_information_dialog(self) -> None:
        existing_bot = self.collection.find_one()

        dialog = BotInformationDialog(existing_bot)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            bot_info = dialog.bot_info

            if bot_info["id"]:
                if existing_bot:
                    self.log_message("Bot information already exists. Updating...")
                    self.collection.update_one(
                        {"id": bot_info["id"]}, {"$set": bot_info}
                    )
                    self.log_message("Bot information updated.")
                else:
                    self.log_message("Creating new bot information...")
                    self.collection.insert_one(bot_info)
                    self.log_message("Bot information created.")
            else:
                self.log_message("Bot ID cannot be empty.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
