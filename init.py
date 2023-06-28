from utils import create_directory
from settings import IMG_MAIN_PATH, IMG_COMPETITIONS_PATH, IMG_FLAGS_PATH, IMG_SCHEDULES_PATH
from db import db_init


# directories
create_directory(IMG_MAIN_PATH)
create_directory(IMG_COMPETITIONS_PATH)
create_directory(IMG_FLAGS_PATH)
create_directory(IMG_SCHEDULES_PATH)


# SQLite
db_init()