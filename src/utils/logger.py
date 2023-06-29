import logging
import sys


def create_logger(name: str, log_level: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if logger.hasHandlers():
        logger.handlers.clear()

    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging\
        .Formatter('%(asctime)s — %(name)s — %(levelname)s — %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.propagate = False

    return logger
