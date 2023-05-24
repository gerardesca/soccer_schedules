from livesoccertv_utils import get_main_matches, filtered_competitions
from database_utils import countries_broadcast_en, main_leagues_en
from utils import get_current_date_by_format
from twitter_utils import create_tweet_with_media
from telegram_utils import send_image_with_msg
from images_utils import create_image_post, delete_image
from settings import PATH_SCHEDULES

def run():
    date_delete_image = get_current_date_by_format(days=-7)
    date_post = get_current_date_by_format(days=1)

    msg = f"""
    {date_post} | JORNADA FUTBOLERA
Transmisiones disponibles para México y USA
Horarios en CST (Hora Estándar Central)

#futbol #transmisiones #jornadafutbolera
"""

    # scraping main page
    all = get_main_matches(countries_broadcast_en, date_post)
    # filtered competitions
    filtered = filtered_competitions(all, main_leagues_en)
    # create image
    image = create_image_post(filtered, name=date_post, color_match=(20,78,147), color_broadcast=(0,91,66), color_lines=(229,54,88))
    # post tweet
    create_tweet_with_media(msg, image)
    # send message to Telegram
    send_image_with_msg(msg, image)
    # delete old image post
    delete_image(PATH_SCHEDULES + f'{date_delete_image}.png')
    
    
if __name__ == '__main__':
    run()