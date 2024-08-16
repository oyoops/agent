import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(config):
    logger = logging.getLogger('ai_web_app')
    logger.setLevel(config['logging']['level'])

    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Create file handler which logs even debug messages
    file_handler = RotatingFileHandler('logs/ai_web_app.log', maxBytes=10240000, backupCount=5)
    file_handler.setLevel(config['logging']['level'])

    # Create console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter(config['logging']['format'])
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# This will be imported in main.py
logger = None