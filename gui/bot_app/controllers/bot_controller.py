from gui.bot_app.views.bot_view import BotView
from gui.bot_app.views.bot_form import BotForm
from gui.bot_app.entities.bot import Bot
from gui.bot_app.entities.user import User
from gui.bot_app.models.bot_model import BotModel
import platform
from PyQt5.QtWidgets import QDialog


class BotController:
    def __init__(self) -> None:
        self.view = BotView()
        self.model = BotModel()

        user_token = platform.version()

        self.view.add_edit_bot_button.clicked.connect(
            lambda: self.add_edit_bot(user_token)
        )
        self.view.build_button.clicked.connect(self.build_bot)

    def add_edit_bot(self, user_token: str) -> None:
        bot = self.model.get_bot_by_user_token(user_token=user_token)
        if bot is None:
            bot_form = BotForm()
        else:
            bot_form = BotForm(bot)

        result = bot_form.exec()

        if result == QDialog.Accepted:
            token, chat_id = bot_form.get_inputs()
            if bot is None:
                self.model.insert_bot({"token": token, "chat_id": chat_id})
            else:
                self.model.update_bot(
                    str(bot["_id"]), {"token": token, "chat_id": chat_id}
                )

    def build_bot(self) -> None:
        print("Build bot")

    def show(self) -> None:
        self.view.show()
