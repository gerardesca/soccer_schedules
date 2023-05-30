from utils import find_images_with_suffix, get_current_date_by_format
from twitter_utils import create_tweet_with_media
from telegram_utils import send_image_with_msg, send_msg
from settings import PATH_SCHEDULES, text_post
import time

# get date today
today = get_current_date_by_format(days=1)
# find images with match date today
images = find_images_with_suffix(PATH_SCHEDULES, f'{today}.png')

# text for posts
text_post_by_competition = {'europa':'CARTELERA EUROPEA',
                            'north_america': 'CARTELERA NORTEAMERICANA',
                            'south_america': 'CARTELERA SUDAMERICANA',
                            'international': 'CARTELERA INTERNACIONAL'}


def run():
    if len(images) == 0:
        send_msg('Mañana no hay partidos para mostrar :(')
    else:
        for path in images:
            for key, value in text_post_by_competition.items():
                if key in path.lower():
                    # post tweet
                    #create_tweet_with_media(text_post(f'{today} | {value}'), path)
                    # send message to Telegram
                    send_image_with_msg(text_post(f'{today} | {value}'), path)
                    time.sleep(1)
                    break
            

if __name__ == '__main__':
    run()