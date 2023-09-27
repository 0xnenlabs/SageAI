import logging

from sageai.types.log_level import LogLevel


def get_logger(log_level: LogLevel):
    logger = logging.getLogger(__name__)
    log_level = log_level.value

    logger.setLevel(log_level)

    formatter = logging.Formatter("%(asctime)s | [%(levelname)s] %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
