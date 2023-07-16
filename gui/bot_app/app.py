from typing import Any, Optional, Tuple

from bson import ObjectId
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
from gui.models.bot_model import Bot
from gui.models.user_model import User
from gui.controllers.bot_controller import BotController
from gui.views.bot_form import BotForm
from gui.common.database import Database

bots_collection = Database("bot_app").get_collection("bots")
users_collection = Database("bot_app").get_collection("users")


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Bot App")
        self.resize(600, 600)

        qr_value = self.frameGeometry()
        cp_value = QDesktopWidget().availableGeometry().center()
        qr_value.moveCenter(cp_value)
        self.move(qr_value.topLeft())

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout: Any = QVBoxLayout()
        self.central_widget.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()
    app.exec()
