from settings import MAIN_DIR
import logging

# Create a logger with the specified log file name
logger = logging.getLogger('app_logger')
logger.setLevel(logging.DEBUG)

# Create a file handler to write log messages to the specified log file
file_handler = logging.FileHandler(MAIN_DIR + '/app.log')
file_handler.setLevel(logging.DEBUG)

# Create a log message formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)


def log_message(log_level, log_message):

    # Log the specified message at the specified level
    if log_level == 'DEBUG':
        logger.debug(log_message)
    elif log_level == 'INFO':
        logger.info(log_message)
    elif log_level == 'WARNING':
        logger.warning(log_message)
    elif log_level == 'ERROR':
        logger.error(log_message)
    elif log_level == 'CRITICAL':
        logger.critical(log_message)
    
    print(log_message)