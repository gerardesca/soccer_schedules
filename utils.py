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


def dates_to_scraping(number_days: int = 1) -> list:
    """
    Returns a dates list given a number of days.
    Example, if given zero, return today date. If given 1, return today and tomorrow.
    Then, the given number is the number of dates from today
    
    Args:
        number_days (int): number of dates from today
    """
    list_dates = [get_current_date_by_format(days=day) for day in range(0, number_days+1)]
    return list_dates  


def convert_time(time, hours, format='%I:%M%p'):
    """ 
        Returns the time according to the given difference hours and the format
    """
    hora_datetime = parse(time)
    dt_result = hora_datetime + timedelta(hours=hours)
    return dt_result.strftime(format)


def create_directory(directory_path) -> None:
    """
    If directory doesnt exist, create directory
    
    Args:
        directory (str): Directory path
    """
    
    # check if the directory exists, if not, create it
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        log_message('INFO', f"Directory {directory_path} created successfully.")
        

def split_text(text: str, symbol: str = '-') -> str:
    parts = text.split(symbol)
    if len(parts) > 1:
        return parts[1].strip()
    else:
        return text

    
def remove_text_special(text: str, text_remove: str = '/') -> str:
    return text.replace(text_remove, '')


def find_images_with_suffix(folder_path, suffix) -> list:
    """
    Find file with suffix given
    """
    
    image_paths = []

    # Traverse all files and subdirectories in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if the file ends with the specified suffix
            if file.endswith(suffix):
                # Get the full path of the file and add it to the list
                image_path = os.path.join(root, file)
                image_paths.append(image_path)

    return image_paths


def delete_file(file_path: str):
    """
    Delete an file given its file path.

    Args:
        file_path (str): The file path to be deleted.
    """

    try:
        # Check if the file exists
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)
            log_message('INFO', f"File at {file_path} deleted successfully.")
        else:
            log_message('INFO', f"File at {file_path} does not exist.")
    except OSError as e:
        log_message('WARNING', f"Error occurred while deleting File at {file_path}: {e}")