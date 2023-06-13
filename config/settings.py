import json
import logging
from typing import Any, Dict

from config.logger_config import setup_logging


class Config:
    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path
        self.settings: Dict[str, Any] = {}

    def load_settings(self) -> None:
        logging.info("Loading settings from %s", self.file_path)
        with open(self.file_path, "r", encoding="utf-8") as file:
            self.settings = json.load(file)
        logging.info("Settings loaded successfully.")

    def get_setting(self, setting_key: str) -> Any:
        logging.info("Getting value for key %s", setting_key)
        return self.settings.get(setting_key)


setup_logging()
config = Config("config/config.json")
config.load_settings()

settings: Dict[str, Any] = config.settings
