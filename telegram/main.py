from telegram_utils import send_image_with_msg, send_msg
import time
import os, sys

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from utils import find_images_with_suffix, get_current_date_by_format
from settings import IMG_SCHEDULES_PATH


# get date today
today = get_current_date_by_format(days=1)
# find images with match date
images = find_images_with_suffix(IMG_SCHEDULES_PATH, f'{today}.png')

# text for posts
text_post_by_competition = {'europa':'CARTELERA EUROPEA',
                            'north_america': 'CARTELERA NORTEAMERICANA',
                            'south_america': 'CARTELERA SUDAMERICANA',
                            'international': 'CARTELERA INTERNACIONAL'}

def text_post(post: str):
    return f"""
{post} | Hora CDMX
"""

def send_images():
    if len(images) == 0:
        send_msg('Mañana no hay partidos para mostrar :(')
    else:
        for path in images:
            for key, value in text_post_by_competition.items():
                if key in path.lower():
                    # send message to Telegram
                    send_image_with_msg(text_post(f'{today} | {value}'), path)
                    time.sleep(1)
                    break


if __name__ == '__main__':
    send_images()