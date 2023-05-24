from datetime import datetime, timedelta
from dateutil.parser import parse
from logging_utils import log_message
import os


def get_current_date_by_format(format='%Y-%m-%d', days=0):
    """ 
        Returns the date according to format.
        Default: 2023-05-03 (year, month, day)
    """
    
    # Get the current datetime object
    now = datetime.now() + timedelta(days)
    
    # Format the datetime object to a string with the given format
    date_str = now.strftime(format)
    
    # Return the formatted date string
    return date_str


def convert_time(time, hours, format='%I:%M%p'):
    """ 
        Returns the time according to the given difference hours and the format
    """
    hora_datetime = parse(time)
    dt_result = hora_datetime + timedelta(hours=hours)
    return dt_result.strftime(format)


def create_directory(directory_path):
    """
    If directory doesnt exist, create directory
    
    Args:
        directory (str): Directory path
    """
    
    # check if the directory exists, if not, create it
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        log_message('INFO', f"Directory {directory_path} created successfully.")