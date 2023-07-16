from gui.bot_app.entities.bot import Bot
from gui.common.database import Database
from typing import Dict, List, Any


class BotModel:
    def __init__(self) -> None:
        self.collection = Database("bot_app").get_collection("bots")

    def get_bots(self) -> List[Dict[str, Any]]:
        return self.collection.get_all_items()

    def get_bot_by_user_token(self, user_token: str) -> Dict[str, Any] | None:
        return self.collection.get_item({"user_token": user_token})

    def insert_bot(self, bot: Bot) -> Any:
        return self.collection.insert_one(bot.dict())

    def update_bot(self, id: str, new_item: Dict[str, Any]) -> Any:
        return self.collection.update_one(id, new_item)
