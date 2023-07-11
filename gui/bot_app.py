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

from gui.database import Database

bots_collection = Database("bot_app").get_collection("bots")
users_collection = Database("bot_app").get_collection("bots")
