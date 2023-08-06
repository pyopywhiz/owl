import logging
from typing import Any

from Crypto.Cipher import AES

from models.firefox_decrypt import decode_login_data


class Decrypt:
    def __init__(self, platform_name: str, browser_name: str):
        self.platform_name = platform_name
        self.browser_name = browser_name
        self.validate_inputs()

    def validate_inputs(self) -> bool:
        valid_platforms = ["ubuntu", "windows"]
        valid_browsers = ["google_chrome", "firefox"]
        platform_valid = self.platform_name in valid_platforms
        browser_valid = self.browser_name in valid_browsers

        if not platform_valid or not browser_valid:
            logging.error(
                "Invalid inputs. Platform should be one of %s, "
                "and browser should be one of %s.",
                valid_platforms,
                valid_browsers,
            )
            return False
        return True

    def decrypt_value(self, encrypted_value: bytes, key: bytes) -> Any:
        method_name = f"_decrypt_method_{self.platform_name}_{self.browser_name}"
        method = getattr(self, method_name, None)
        if method:
            try:
                return method(encrypted_value, key)
            except (ValueError, IndexError) as error:
                logging.error(
                    "An error occurred while decrypting: %s. Encrypted value: %s",
                    error,
                    encrypted_value,
                )
        else:
            logging.error(
                "Decryption method not supported for %s and %s.",
                self.platform_name,
                self.browser_name,
            )
        return ""

    def _decrypt_method_ubuntu_google_chrome(
            self, encrypted_value: bytes, key: bytes
    ) -> str:
        iv_value = b"                "
        cipher = AES.new(key, AES.MODE_CBC, IV=iv_value)
        value = cipher.decrypt(encrypted_value[3:])
        return value[: -value[-1]].decode("utf8")

    def _decrypt_method_ubuntu_firefox(self, encrypted_value: str, key: bytes) -> str:
        return decode_login_data(encrypted_value, key)

    def _decrypt_method_windows_google_chrome(
            self, encrypted_value: bytes, key: bytes
    ) -> str:
        iv_value = encrypted_value[3:15]
        encrypted_value = encrypted_value[15:]
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv_value)
        return cipher.decrypt(encrypted_value)[:-16].decode()

    def _decrypt_method_windows_firefox(self, encrypted_value: str, key: bytes) -> str:
        return decode_login_data(encrypted_value, key)
