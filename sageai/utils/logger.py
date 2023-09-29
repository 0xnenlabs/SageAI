import logging
from sageai.types.log_level import LogLevel


def get_logger(logger_name: str, log_level: LogLevel):
    logger = logging.getLogger(logger_name)

    log_level_value = log_level.value
    logger.setLevel(log_level_value)

    formatter = logging.Formatter("%(asctime)s | [%(levelname)s] %(message)s")

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level_value)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    else:
        logger.handlers[0].setLevel(log_level_value)  # assumes only one handler

    return logger
