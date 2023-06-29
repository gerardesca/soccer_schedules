from livesoccertv_utils import LiveSoccer, get_matches_by_competition
from db import ConnectionDB
from settings import MAX_HEIGHT_IMAGE
from images_utils import ImageV1
from utils import dates_to_scraping

"""VARIABLES"""

# get today and tomorrow dates
#dates = dates_to_scraping(1)
dates = ['2023-05-06']
# choose language Spanish
language = 'es'
# create db connection
database = ConnectionDB()
# query for countries broadcasts in Spanish
countries_broadcasts = database.get_countries_broadcast(language)
# init Scraper
scraper = LiveSoccer(countries_broadcasts, language)
# init Image
img = ImageV1(database)


def by_continent():
    
    # queries for competitions by each continent
    europe = database.get_competition_by_continent('Europe', language)
    north = database.get_competition_by_continent('North America', language)
    south = database.get_competition_by_continent('South America', language)
    inter = database.get_competition_by_continent('International', language)
    
    for date in dates:
        # extract data
        data = scraper.get_all_main_matches(date)
        # filter data by continent
        data_europe = get_matches_by_competition(data, europe)
        data_north = get_matches_by_competition(data, north)
        data_south = get_matches_by_competition(data, south)
        data_inter = get_matches_by_competition(data, inter)
        # create images by continent
        img.create_images_by_max_height(data_europe, f'Europe_{language}_{date}', f'CARTELERA EUROPEA {date}', MAX_HEIGHT_IMAGE)
        img.create_images_by_max_height(data_south, f'South_America_{language}_{date}', f'CARTELERA SUDAMERICANA {date}', MAX_HEIGHT_IMAGE)
        img.create_images_by_max_height(data_north, f'North_America_{language}_{date}', f'CARTELERA NORTEAMERICANA {date}', MAX_HEIGHT_IMAGE)
        img.create_images_by_max_height(data_inter, f'International_{language}_{date}', f'CARTELERA INTERNACIONAL {date}', MAX_HEIGHT_IMAGE)
    
    
def all_competitions():

    # query for all competitions
    competitions = database.get_competitions(language)
    
    for date in dates:
        # extract data
        data = scraper.get_all_main_matches(date)
        # filter data
        data_competitions = get_matches_by_competition(data, competitions)
        # create images
        img.create_images_by_max_height(data_competitions, f'All_{language}_{date}', f'CARTELERA FUTBOLERA {date}', MAX_HEIGHT_IMAGE)
    

if __name__ == '__main__':
    by_continent()
    #all_competitions()
    database.close()