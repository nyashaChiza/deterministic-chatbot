import sys

from decouple import config
from loguru import logger


def configure_logging() -> None:
    """
    Structured JSON logs when DEBUG=False (production), so a log
    aggregator can parse them; the default colorized console format stays
    for local dev/tests, where a person is reading stdout directly.
    """
    debug = config("DEBUG", default=True, cast=bool)
    if not debug:
        logger.remove()
        logger.add(sys.stdout, serialize=True)


configure_logging()
