from livesoccertv_utils import filtered_competitions
from images_utils import create_image_post
from logging_utils import log_message
from twitter_utils import create_tweet_with_media
from telegram_utils import send_image_with_msg
from utils import get_current_date_by_format


def post(text: list, title: str, image_name: str, filter: list, text_post: str) -> str:    
    
    # filtered competitions
    filtered = filtered_competitions(text, filter)
    # create image
    path_image = create_image_post(filtered, name=image_name, title_post=title, color_title_post=(18, 5, 5), color_match=(0, 76, 101), color_broadcast=(0, 120, 62), color_lines=(254,254,254))
    
    if path_image != None:
        log_message('INFO', f"Image created: {image_name} to post: {title}")
        # post tweet
        create_tweet_with_media(text_post, path_image)
        # send message to Telegram
        send_image_with_msg(text_post, path_image)
        # delete old image post
        #delete_image(PATH_SCHEDULES + f'{name_image+date_delete_image}.png')