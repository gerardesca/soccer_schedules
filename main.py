from livesoccertv_utils import get_main_matches
from database_utils import countries_broadcast_en, COMPETITIONS
from utils import get_current_date_by_format
from posts_utils import post
import time

date_delete_image = get_current_date_by_format(days=-7)
date_post = get_current_date_by_format(days=3)


def text_post(post: str):
    return f"""
    {date_post} | {post}
Transmisiones disponibles para México y USA
Horarios en CST (Hora CDMX)

#futbol #transmisiones #jornadafutbolera
"""


def run():
    # scraping main page
    all = get_main_matches(countries_broadcast_en, date_post)
    
    # posts
    post(all, f"Cartelera Europea {date_post}", 'Europa_' + date_post, COMPETITIONS['Europe'], text_post('CARTELERA EUROPEA'))
    time.sleep(2)
    post(all, f"Cartelera Norteamericana {date_post}", 'North_America_' + date_post, COMPETITIONS['North_America'], text_post('CARTELERA NORTEAMERICANA'))
    time.sleep(2)
    post(all, f"Cartelera Sudamericana {date_post}", 'South_America_' + date_post, COMPETITIONS['South_America'], text_post('CARTELERA SUDAMERICANA'))
    time.sleep(2)
    post(all, f"Cartelera Internacional {date_post}", 'International_' + date_post, COMPETITIONS['International'], text_post('CARTELERA INTERNACIONAL'))
    

if __name__ == '__main__':
    run()