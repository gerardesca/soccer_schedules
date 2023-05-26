from typing import Final
import os

MAIN_FILE: Final = os.path.abspath(__file__)
MAIN_DIR: Final = os.path.dirname(MAIN_FILE)

PATH: Final = os.path.join(MAIN_DIR, 'images/')
PATH_COMPETITIONS: Final = os.path.join(MAIN_DIR, 'images/competitions/')
PATH_SCHEDULES: Final = os.path.join(MAIN_DIR, 'images/schedules/')
PATH_FLAGS: Final = os.path.join(MAIN_DIR, 'images/flags/')
FONT: Final = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

MAX_HEIGHT_IMAGE = 1500