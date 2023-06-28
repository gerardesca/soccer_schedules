from typing import Final
import os

# app
MAIN_FILE: Final = os.path.abspath(__file__)
MAIN_DIR: Final = os.path.dirname(MAIN_FILE)


# database
NAME_DB = 'soccer_schedules.db'


# images
IMG_MAIN_PATH: Final = os.path.join(MAIN_DIR, 'images/')
IMG_COMPETITIONS_PATH: Final = os.path.join(MAIN_DIR, 'images/competitions/')
IMG_SCHEDULES_PATH: Final = os.path.join(MAIN_DIR, 'images/schedules/')
IMG_FLAGS_PATH: Final = os.path.join(MAIN_DIR, 'images/flags/')
FONT: Final = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
MAX_HEIGHT_IMAGE = 2000