from PyQt5.QtWidgets import (
    QApplication,
)
from mongoengine import connect

from gui.todo_app.config import MONGODB_CONNECTION_STRING
from gui.todo_app.controllers.main_controller import MainController

connect(host=MONGODB_CONNECTION_STRING)

if __name__ == "__main__":
    app = QApplication([])

    main_controller = MainController()
    main_controller.show()
    app.exec()
