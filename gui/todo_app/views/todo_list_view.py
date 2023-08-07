from typing import Any

from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QHeaderView


class TodoListView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.layout: Any = QVBoxLayout()
        self.todo_table = QTableView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(
            ["Object Id", "Title", "Description", "Completed"]
        )
        self.todo_table.setModel(self.model)
        self.todo_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.layout.addWidget(self.todo_table)
        self.setLayout(self.layout)
