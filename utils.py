from settings import TIMEZONE_SERVER_LIVESOCCERTV, LANGUAGE
from babel.dates import get_timezone_location
from datetime import datetime, timedelta
from logging_utils import log_message
from dateutil.parser import parse
import pytz
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


def convert_time(time: str, time_zone: str, format: str = '%I:%M%p', language: str = LANGUAGE):
    """ 
        Returns the time according to the given timezone and format
    """
    
    lang = 'en' if language == '' else language
    
    if time is None:
        return 'TBA'
    
    # parse time
    hora_datetime = parse(time)
    
    # timezone New York from server
    ny_tz = pytz.timezone(TIMEZONE_SERVER_LIVESOCCERTV)

    # desired timezone
    desired_tz = pytz.timezone(time_zone)

    # convert time to New York timezone
    ny_time = ny_tz.localize(hora_datetime)

    # convert time to desired timezone
    desired_time = ny_time.astimezone(desired_tz)
    
    # get timezone name
    time_zone_name = desired_time.strftime('%Z')
    
    # get city name
    city_name = get_timezone_location(time_zone, locale=lang, return_city=True)

    # format time
    formatted_time = desired_time.strftime(format)

    return f"{formatted_time} {time_zone_name} {city_name}"


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