import asyncio
import logging
from typing import Any, List, Optional

from telegram import Bot

from utils.decorator import retry_async


class BotTool:
    def __init__(self, token: str, chat_id: str):
        self.token: str = token
        self.chat_id: str = chat_id

    @retry_async()
    async def send_text(self, bot: Bot, text: str) -> None:
        logging.info("Sending text message to %s", self.chat_id)
        await bot.send_message(chat_id=self.chat_id, text=text)  # type: ignore

    @retry_async()
    async def send_photo(self, bot: Bot, photo: Any) -> None:
        logging.info("Sending photo to %s", self.chat_id)
        await bot.send_photo(chat_id=self.chat_id, photo=photo)  # type: ignore

    @retry_async()
    async def send_document(self, bot: Bot, document: str) -> None:
        logging.info("Sending document to %s", self.chat_id)
        with open(document, "rb") as doc_file:
            await bot.send_document(chat_id=self.chat_id, document=doc_file)  # type: ignore

    async def send_information(
            self,
            texts: Optional[List[str]] = None,
            photos: Optional[List[Any]] = None,
            documents: Optional[List[str]] = None,
    ) -> None:
        if texts is None:
            texts = []
        if photos is None:
            photos = []
        if documents is None:
            documents = []
        async with Bot(token=self.token) as bot:
            for text in texts:
                await self.send_text(bot, text)

            for photo in photos:
                await self.send_photo(bot, photo)

            for document in documents:
                await self.send_document(bot, document)


class ListBot:
    def __init__(self) -> None:
        self.bots: List[BotTool] = []
        logging.info("ListBot initialized")

    async def send_information(
            self,
            texts: Optional[List[str]] = None,
            photos: Optional[List[Any]] = None,
            documents: Optional[List[str]] = None,
    ) -> None:
        if texts is None:
            texts = []
        if photos is None:
            photos = []
        if documents is None:
            documents = []

        logging.info("Sending information...")
        tasks = [
            bot_tool.send_information(texts, photos, documents)
            for bot_tool in self.bots
        ]
        await asyncio.gather(*tasks)
        logging.info("Information sent successfully")

    def create_bot(self, bot_token: str, chat_id: str) -> None:
        logging.info("Creating new bot for chat_id %s", chat_id)
        new_bot = BotTool(bot_token, chat_id)
        self.bots.append(new_bot)

    def read_bot(self, bot_token: str) -> Optional[BotTool]:
        for bot in self.bots:
            if bot.token == bot_token:
                return bot
        logging.info("Bot not found.")
        return None

    def update_bot(
            self,
            bot_token: str,
            new_bot_token: Optional[str] = None,
            chat_id: Optional[str] = None,
    ) -> None:
        for bot in self.bots:
            if bot.token == bot_token:
                if new_bot_token:
                    bot.token = new_bot_token
                if chat_id:
                    bot.chat_id = chat_id
                logging.info("Bot updated.")
                return
        logging.info("Bot not found.")

    def delete_bot(self, bot_token: str) -> None:
        for bot in self.bots:
            if bot.token == bot_token:
                self.bots.remove(bot)
                logging.info("Bot deleted.")
                return
        logging.info("Bot not found.")
