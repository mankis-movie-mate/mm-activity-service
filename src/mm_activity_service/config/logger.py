import logging
import sys


def setup_logger(log_level: str = "INFO"):
    LOG_FORMAT = "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"

    logger = logging.getLogger()
    if logger.hasHandlers():
        return

    logger.setLevel(log_level)
    log_formatter = logging.Formatter(LOG_FORMAT)

    # Logs to stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)