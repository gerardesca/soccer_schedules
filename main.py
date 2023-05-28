from livesoccertv_utils import get_main_matches
from database_utils import COUNTRIES_BROADCAST_EN, COMPETITIONS
from utils import dates_to_scraping
from posts_utils import create_images_to_post
import time


# get today and tomorrow dates
dates = dates_to_scraping(1)


def run():
    
    for date in dates:
        # scraping main page
        all = get_main_matches(COUNTRIES_BROADCAST_EN, date)
        
        # posts
        create_images_to_post(all, f"Cartelera Europea {date}", 'Europa_' + date, COMPETITIONS['Europe'])
        time.sleep(2)
        create_images_to_post(all, f"Cartelera Norteamericana {date}", 'North_America_' + date, COMPETITIONS['North_America'])
        time.sleep(2)
        create_images_to_post(all, f"Cartelera Sudamericana {date}", 'South_America_' + date, COMPETITIONS['South_America'])
        time.sleep(2)
        create_images_to_post(all, f"Cartelera Internacional {date}", 'International_' + date, COMPETITIONS['International'])
    

if __name__ == '__main__':
    run()