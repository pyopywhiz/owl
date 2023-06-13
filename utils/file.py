import logging
import os
import shutil
from typing import List


def remove_files_and_folders(paths: List[str]) -> None:
    for path in paths:
        if os.path.isfile(path):
            try:
                os.remove(path)
                logging.info("File removed: %s", path)
            except OSError:
                pass
        elif os.path.isdir(path):
            try:
                shutil.rmtree(path)
                logging.info("Directory removed: %s", path)
            except OSError:
                pass
        else:
            logging.info("Invalid path: %s", path)
