import logging
from datetime import datetime, timedelta
from typing import Any, Union


def json_serializer(obj: Any) -> Union[str, Any]:
    if isinstance(obj, bytes):
        return obj.decode("utf-8")

    return obj


def get_chrome_datetime(chromedate: int) -> Union[int, datetime]:
    if chromedate != 86400000000 and chromedate:
        try:
            return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
        except ValueError as error:
            logging.error("Error occurred in get_chrome_datetime: %s", error)
            return chromedate
    else:
        return chromedate
