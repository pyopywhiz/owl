import logging
import os
import zipfile
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from PIL import ImageGrab


def get_page_title(url: str) -> str:
    logging.info("Extracting page title for %s", url)
    page = requests.get(url=url, timeout=10)
    soup = BeautifulSoup(page.content, "html.parser")
    title_element = soup.find("title")
    if title_element is None:
        logging.info("No title found for %s", url)
        return ""
    title: str = title_element.get_text()
    logging.info("Found title for %s: %s", url, title)
    return title


def capture_screenshot() -> Optional[bytes]:
    logging.info("Capturing screenshot...")
    screenshot = ImageGrab.grab()

    screenshot_path = "screenshot.png"
    screenshot.save(screenshot_path)

    with open(screenshot_path, "rb") as file:
        screenshot_bytes = file.read()

    logging.info("Screenshot captured.")
    return screenshot_bytes


def compress_folders_and_files(directories: List[str], zip_file: str) -> None:
    logging.info("Compressing folders and files...")
    with zipfile.ZipFile(zip_file, "w") as zipf:
        for item in directories:
            if os.path.exists(item):
                if os.path.isfile(item):
                    zipf.write(item, os.path.basename(item))
                elif os.path.isdir(item):
                    for root, _, files in os.walk(item):
                        for file in files:
                            file_path = os.path.join(root, file)
                            zipf.write(file_path, os.path.relpath(file_path, item))
            else:
                logging.warning("File or folder does not exist: %s", item)
    logging.info("Compression completed.")
