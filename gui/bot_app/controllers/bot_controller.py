import platform

from PyQt5.QtWidgets import QDialog

from gui.bot_app.models.bot import Bot
from gui.bot_app.models.user import User
from gui.bot_app.views.bot_form import BotForm
from gui.bot_app.views.bot_view import BotView


class BotController:
    def __init__(self) -> None:
        self.view = BotView()
        user_token = platform.version()
        self.create_user(user_token)
        self.view.add_edit_bot_button.clicked.connect(
            lambda: self.add_edit_bot(user_token)
        )
        self.view.build_button.clicked.connect(self.build_bot)

    def add_edit_bot(self, user_token: str) -> None:
        user = User.objects.get(user_token=user_token)
        bot = Bot.objects(user=user).first()
        if bot is None:
            bot_form = BotForm()
        else:
            bot_form = BotForm(bot)

        result = bot_form.exec()

        if result == QDialog.Accepted:
            token, chat_id = bot_form.get_inputs()
            if bot is None:
                Bot(token=token, chat_id=chat_id, user=user).save()
            else:
                bot.token = token
                bot.chat_id = chat_id
                bot.save()

    def build_bot(self) -> None:
        print("Build bot")

    def show(self) -> None:
        self.view.show()

    def create_user(self, user_token: str) -> None:
        user = User.objects(user_token=user_token).first()
        if not user:
            User(user_token=user_token).save()
