import logging

def log_message(log_file, log_level, log_message):
    # Create a logger with the specified log file name
    logger = logging.getLogger(log_file)
    logger.setLevel(log_level)

    # Create a file handler to write log messages to the specified log file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)

    # Create a log message formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

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