from gui.common.database import Database
from typing import Dict, Any
from gui.bot_app.entities.user import User


class UserModel:
    def __init__(self) -> None:
        self.user_collection = Database("bot_app").get_collection("users")
        self.bot_collection = Database("bot_app").get_collection("bots")

    def get_user_by_user_token(self, user_token: str) -> User:
        pass

    def insert_user(self, item: Dict[str, Any]) -> User:
        pass

    def update_user(self, id: str, new_item: Dict[str, Any]) -> User:
        pass
