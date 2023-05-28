from utils import find_images_with_suffix, get_current_date_by_format
from twitter_utils import create_tweet_with_media
from telegram_utils import send_image_with_msg
from settings import PATH_SCHEDULES, text_post
import time

# get date today
today = get_current_date_by_format(days=2)
# find images with match date today
images = find_images_with_suffix(PATH_SCHEDULES, f'{today}.png')

def run():
    for path in images:
        if path != None:
            # post tweet
            #create_tweet_with_media(text_post(f'{today} | CARTELERA EUROPEA'), path)
            # send message to Telegram
            send_image_with_msg(text_post(f'{today} | CARTELERA EUROPEA'), path)
            time.sleep(1)
            

if __name__ == '__main__':
    run()