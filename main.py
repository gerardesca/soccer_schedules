from livesoccertv_utils import LiveSoccer, get_matches_by_competition
from db import ConnectionDB
from settings import MAX_HEIGHT_IMAGE
from images_utils import ImageV1
from utils import dates_to_scraping


def v1_by_continent():
    
    # get today and tomorrow dates
    dates = dates_to_scraping(1)
    language = 'en'

    database = ConnectionDB()
    countries_broadcasts = database.get_countries_broadcast(language)
    europe = database.get_competition_by_continent('Europe', language)
    north = database.get_competition_by_continent('North America', language)
    south = database.get_competition_by_continent('South America', language)
    inter = database.get_competition_by_continent('International', language)
    
    scraper = LiveSoccer(countries_broadcasts, language)
    img = ImageV1(database)
    
    for date in dates:
        data = scraper.get_all_main_matches(date)
        data_europe = get_matches_by_competition(data, europe)
        data_north = get_matches_by_competition(data, north)
        data_south = get_matches_by_competition(data, south)
        data_inter = get_matches_by_competition(data, inter)
        img.create_images_by_max_height(data_europe, f'Europa_{language}_{date}', f'CARTELERA EUROPEA {date}', MAX_HEIGHT_IMAGE)
        img.create_images_by_max_height(data_south, f'Sudamerica_{language}_{date}', f'CARTELERA NORTEAMERICANA {date}', MAX_HEIGHT_IMAGE)
        img.create_images_by_max_height(data_north, f'Norteamerica_{language}_{date}', f'CARTELERA NORTEAMERICANA {date}', MAX_HEIGHT_IMAGE)
        img.create_images_by_max_height(data_inter, f'Internacional_{language}_{date}', f'CARTELERA INTERNACIONAL {date}', MAX_HEIGHT_IMAGE)
    
    database.close()


if __name__ == '__main__':
    v1_by_continent()