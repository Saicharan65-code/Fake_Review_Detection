import logging
import os
from logging.handlers import RotatingFileHandler
import config

def setup_logger(name):
    """Setup logger with file and console handlers"""
    logger = logging.getLogger(name)
    logger.setLevel(config.LOG_LEVEL)

    # Create logs directory if it doesn't exist
    os.makedirs(config.LOG_PATH, exist_ok=True)

    # Create file handler
    file_handler = RotatingFileHandler(
        os.path.join(config.LOG_PATH, f'{name}.log'),
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(config.LOG_FORMAT))
    logger.addHandler(file_handler)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(config.LOG_FORMAT))
    logger.addHandler(console_handler)

    return logger