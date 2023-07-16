from gui.bot_app.views.bot_view import BotView
from gui.bot_app.views.bot_form import BotForm
from gui.bot_app.entities.bot import Bot
from gui.bot_app.entities.user import User
from gui.bot_app.models.bot_model import BotModel


class BotController:
    def __init__(self) -> None:
        self.view = BotView()
        self.model = BotModel()
