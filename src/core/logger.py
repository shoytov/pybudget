import sys
from logging import LoggerAdapter

from loguru import logger

from src.core.consts import LOGGING_LEVEL, LOGGING_SERIALIZE


class ApplicationLogger(LoggerAdapter):
    def __init__(self) -> None:  # noqa
        self.logger = logger

    def make_logger(self):
        self.logger.remove()
        self.logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=LOGGING_LEVEL,
            serialize=LOGGING_SERIALIZE,
        )
        return self.logger


app_logger = ApplicationLogger().make_logger()
