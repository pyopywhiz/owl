import base64
import json
import logging
import os
import sqlite3
from typing import Any, Dict, Optional

import keyring
from Crypto.Protocol.KDF import PBKDF2

from models.firefox_decrypt import get_firefox_key


class Key:
    def __init__(self, platform_name: str, browser_name: str):
        self.platform_name = platform_name
        self.browser_name = browser_name

    def get_key(self, *_: Any, **__: Any) -> bytes:
        method_name = f"_get_key_{self.platform_name}_{self.browser_name}"
        method = getattr(self, method_name, self._unsupported_method)
        if method:
            try:
                return method(*_, **__)
            except (ValueError, IndexError, sqlite3.Error) as error:
                logging.error("An error occurred while getting the key: %s", error)
        else:
            logging.error(
                "Getting the key method not supported for %s and %s.",
                self.platform_name,
                self.browser_name,
            )
        return "".encode("utf-8")

    def save_key(self, key: Optional[bytes] = None, file_path: str = "key.bin") -> None:
        if key is None:
            key = self.get_key()

        with open(file_path, "wb") as file:
            file.write(key)

    def _unsupported_method(self) -> bytes:
        return (
            f"Decryption method not supported for "
            f"{self.platform_name} and {self.browser_name}."
        ).encode("utf8")

    def _get_key_ubuntu_google_chrome(self) -> bytes:
        settings: Dict[str, Any] = {
            "PASSWORD": "peanut",
            "SALT": "saltysalt",
            "NITERS": 1,
            "IV": "                ",
            "LENGTH": 16,
        }
        password = settings["PASSWORD"]
        for item in (
            keyring.get_keyring().get_preferred_collection().get_all_items()  # type: ignore
        ):
            label = item.get_label()
            if label == "Chrome Safe Storage":
                password = item.get_secret().decode("utf8")

        key: bytes = PBKDF2(
            password,
            settings["SALT"],
            settings["LENGTH"],
            settings["NITERS"],
        )
        return key

    def _get_key_ubuntu_firefox(self, *_: Any, **__: Any) -> bytes:
        return get_firefox_key(__["profile_path"])

    def _get_key_windows_google_chrome(self) -> Any:
        import win32crypt  # type: ignore

        local_state_path: str = os.path.join(
            os.environ["USERPROFILE"],
            "AppData",
            "Local",
            "Google",
            "Chrome",
            "User Data",
            "Local State",
        )
        with open(local_state_path, "r", encoding="utf-8") as file:
            state: str = file.read()
            local_state: Dict[str, Any] = json.loads(state)

        key: bytes = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        key = key[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

    def _get_key_windows_firefox(self, *_: Any, **__: Any) -> bytes:
        return get_firefox_key(__["profile_path"])
