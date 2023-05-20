from livesoccertv_utils import get_main_matches, filtered_competitions
from database_utils import countries_broadcast_en, main_leagues_en
from utils import get_current_date_by_format
from twitter_utils import create_tweet_with_media
from images_utils import create_image_post, delete_image

def run():
    today = get_current_date_by_format()
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
    image = create_image_post(filtered, name=date_post)
    # post tweet
    create_tweet_with_media(msg, image)
    # delete old image post
    delete_image(f'./images/{today}.png')
    
if __name__ == '__main__':
    run()