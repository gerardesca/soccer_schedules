import logging

def configure_logging(log_file, log_level=logging.DEBUG):
    """Configures logging to write log messages to a file.

    Args:
        log_file (str): Path to the log file.
        log_level (int, optional): Level of log messages to write. Defaults to logging.DEBUG.
    """
    # Configure logging
    logging.basicConfig(filename=log_file, level=log_level)

    # Create a formatter for log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create a handler to send log messages to the file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logging.getLogger('').addHandler(file_handler)