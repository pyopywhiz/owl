from typing import Any, Optional, Tuple
import platfrom
from bson import ObjectId
from pymongo import MongoClient
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

client: Any = MongoClient(
    "mongodb+srv://hungdhv97:hung23081997@cluster0.pxjti4x.mongodb.net/"
)
database: Any = client["bot_app"]
bots_collection: Any = database["bots"]
users_collection: Any = database["users"]
