import asyncio
import logging
from functools import wraps
from typing import Any, Callable, Optional, TypeVar

T = TypeVar("T", bound=Callable[..., Any])


def retry_async(max_retries: int = 5, delay: int = 5) -> Callable[[T], T]:
    def decorator(func: T) -> T:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Optional[Any]:
            for attempt in range(1, max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as error:  # pylint: disable=W0718
                    logging.warning(
                        "Function %s had an unexpected error: %s. Attempting retry %d/%d",
                        func.__name__,
                        str(error),
                        attempt,
                        max_retries,
                    )
                    await asyncio.sleep(delay)
            logging.error(
                "Function %s failed after %d retries", func.__name__, max_retries
            )
            return None

        return wrapper  # type: ignore

    return decorator
