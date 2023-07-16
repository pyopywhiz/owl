from gui.common.database import Database
from typing import Dict, Any


class BotModel:
    def __init__(self) -> None:
        self.user_collection = Database("bot_app").get_collection("users")
        self.bot_collection = Database("bot_app").get_collection("bots")

    def get_bots_by_user_token(self, user_token: str) -> Any:
        user = self.user_collection.get_item({"user_token": user_token})
        return user["bots"] if user else None

    def get_bot_by_user_token(self, user_token: str) -> Any:
        user = self.user_collection.get_item({"user_token": user_token})
        return user["bots"][0] if user else None

    def insert_bot(self, item: Dict[str, Any]) -> Any:
        return self.bot_collection.insert_one(item)

    def update_bot(self, id: str, new_item: Dict[str, Any]) -> Any:
        return self.bot_collection.update_one(id, new_item)
