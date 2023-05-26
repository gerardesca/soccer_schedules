from images_utils import split_list_by_height, create_image_post
from settings import MAX_HEIGHT_IMAGE
from livesoccertv_utils import filtered_competitions
from twitter_utils import create_tweet_with_media
from telegram_utils import send_image_with_msg
import time


def post(text: list, title: str, image_name: str, filter: list, text_post: str) -> str:
    path_images = [] 
    
    # filtered competitions
    filtered = filtered_competitions(text, filter)

    # split list
    number_images = split_list_by_height(filtered, MAX_HEIGHT_IMAGE, title)
    
    for i, image in enumerate(number_images, start=1):
        image_rename = f'{i}_{image_name}'
        # create images
        path_image = create_image_post(image, name=image_rename, title_post=title, color_title_post=(18, 5, 5), color_match=(0, 76, 101), color_broadcast=(0, 120, 62), color_lines=(254,254,254))
        path_images.append(path_image)
    
    for path in path_images:
        if path != None:
            # post tweet
            create_tweet_with_media(text_post, path)
            # send message to Telegram
            send_image_with_msg(text_post, path)
            time.sleep(1)