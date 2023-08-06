from typing import Any

from PyQt5.QtWidgets import (
    QApplication,
    QDesktopWidget,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from gui.bot_app.controllers.bot_controller import BotController


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

        bot_controller = BotController()
        self.layout.addWidget(bot_controller.view)


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()
    app.exec()
