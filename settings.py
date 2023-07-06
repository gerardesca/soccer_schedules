from typing import Final
import os

"""app"""

MAIN_FILE: Final = os.path.abspath(__file__)
MAIN_DIR: Final = os.path.dirname(MAIN_FILE)


"""database"""

NAME_DB = 'soccer_schedules.db'
PATH_DB: Final = os.path.join(MAIN_DIR, NAME_DB)


"""images"""

IMG_MAIN_PATH: Final = os.path.join(MAIN_DIR, 'images/')
IMG_COMPETITIONS_PATH: Final = os.path.join(MAIN_DIR, 'images/competitions/')
IMG_SCHEDULES_PATH: Final = os.path.join(MAIN_DIR, 'images/schedules/')
IMG_FLAGS_PATH: Final = os.path.join(MAIN_DIR, 'images/flags/')
FONTS_PATH: Final = os.path.join(MAIN_DIR, 'fonts/')
FONT_DEFAULT: Final = os.path.join(FONTS_PATH, 'DejaVuSans-Bold.ttf')
MAX_HEIGHT_IMAGE = 1700

# (width, height)
SIZE_LOGOS_TEAMS = (60,60)

# you can add or remove timezones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
TIMEZONES_FOR_IMAGE = ['America/Mexico_City'
                       ,'America/Tijuana'
                       ,'America/Chicago'
                       #,'America/Los_Angeles' 
                       #,'America/New_York'
                       #,'America/Buenos_Aires'
                       ]


"""scraping"""

# you can change language for English: 'en' or Spanish: 'es'
LANGUAGE = 'es'

TIMEZONE_SERVER_LIVESOCCERTV = 'America/New_York'