import logging


def setup_logging() -> None:
    """Setup logging configuration"""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
