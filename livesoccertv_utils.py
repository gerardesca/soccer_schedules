from requests_utils import make_request
from logging_utils import log_message
from utils import convert_time, get_current_date_by_format
from bs4 import BeautifulSoup
import time


class LiveSoccer:
    
    def __init__(self, countries_broadcast: list, language: str = 'en') -> None:
        self.BASE_URL = 'https://www.livesoccertv.com/'
        self.HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"}
        self.countries_broadcast = countries_broadcast
        self.language = '' if language == 'en' else language + '/'
    
    
    def get_all_main_matches(self, date: str = get_current_date_by_format()) -> list:
        """
        Return a list with all main matches from livesoccer on given date
        
        Args:
        date (str): Date of the games to scraping. 
                    Format: 2023-05-03 (year, month, day).
                    Deafult: Run script date
        """

        
        # main url
        url = self.BASE_URL + self.language + 'schedules/' + date + '/'
        
        # list will be return
        all_matches_by_competition = []
        
        # make request and get soup object
        content = make_request(url, headers=self.HEADER)
        soup = BeautifulSoup(content, 'html.parser')
        log_message('INFO', f"Start Scraping to: {url}")

        # find main table and all rows
        main_table = soup.find('table', class_='schedules')
        rows = main_table.find_all('tr')

        count_matches = 0
        # iterate each row
        for row in rows:
            # find row with competition name, create main dictionary and store in list 
            if row.has_attr('class') and 'sortable_comp' in row['class']:
                dict_competition = {'competition': row.get_text().strip(),
                                    'matches':[]}
                all_matches_by_competition.append(dict_competition)
            # The other rows are matches
            else:
                count_matches += 1
                # find its competition from each match (previus)
                competition = row.find_previous('tr', class_='sortable_comp').get_text().strip()
                
                # find elements by each match
                match_title = row.find('a').get_text()
                time_hour = row.find(lambda tag: tag.name == 'span' and tag.get('df') and 'ts' in tag.get('class', []))
                url = row.find('a')['href']
                url = self.BASE_URL + url[1:]
                
                # get logos links and broadcasts
                links_img, broadcasts = self._get_broadcasts_and_imgs_by_match(url)
                
                # create dictionary
                dict_matches_by_competition = {'title':match_title,
                                            'logos':links_img,
                                            'date':date,
                                            'time_utc': 'TBA' if time_hour is None else convert_time(time_hour.get_text().strip(), 4),
                                            'time_utc-4h': 'TBA' if time_hour is None else time_hour.get_text().strip(), #EDT New York
                                            'time_utc-5h': 'TBA' if time_hour is None else convert_time(time_hour.get_text().strip(), 4-6), #CDT Houston
                                            'time_utc-6h': 'TBA' if time_hour is None else convert_time(time_hour.get_text().strip(), 4-6), #CST CDMX
                                            'time_utc-7h': 'TBA' if time_hour is None else convert_time(time_hour.get_text().strip(), 4-7), #PDT Los angeles
                                            'url': url,
                                            'broadcasts': broadcasts}
                
                time.sleep(2)
                
                # find competition and store match in its competition
                for comp in all_matches_by_competition:
                    if comp['competition'] == competition:
                        comp['matches'].append(dict_matches_by_competition)
        
        log_message('INFO', f"Get {len(all_matches_by_competition)} main competitions and {count_matches} matches in total")
                        
        return all_matches_by_competition
    
    
    def _get_broadcasts_and_imgs_by_match(self, url: str) -> list:
        """
        Return a list with broadcasts filtered by list_countries_broadcasts and images' url from teams
        If match dont have any broadcast by list_countries_broadcasts, Return a empty list
        
        Args:
        url (str): URL of the game to scraping.
        """
        
        content = make_request(url, headers=self.HEADER)
        soup = BeautifulSoup(content, 'html.parser')
        log_message('INFO', f"Start Scraping to: {url}")
        
        # images links
        img_links = ['https:' + link.find_next('img')['src'] for link in soup.find_all('h1', {'id': 'team'})]
        
        # broadcasts
        main_table = soup.find('table', attrs={'id':'wc_channels'})
        
        try:
            broadcast_by_country = main_table.find_all('tr')
            
            broadcasts = []
            for broadcast in broadcast_by_country[:len(broadcast_by_country)-1]:
                country = broadcast.find_next('td').get_text()
                if country in self.countries_broadcast:
                    tvs = [tv.get_text() for tv in broadcast.find_all('a')]
                    dict = {'country':country,
                            'channels':tvs}
                    broadcasts.append(dict)
            
            return img_links, broadcasts

        except:
            log_message('WARNING', f"There arent broadcast")
            return [], []
        
        
def get_matches_by_competition(data: list, competitions: list) -> list:
    """
    Return a list filtered by competition, the list 'competitions' has the main competitions
    Return message to matches without broadcasts
    
    Args:
    data (list): All data
    competitions (list): Main competitions to filter by
    """
    if competitions:
        # filter by competition
        filtered_compe = [compe for compe in data if compe['competition'] in competitions]
        
        # filter by broadcasts empty
        filtered_broad = [{'competition': item['competition'], 'matches': [match for match in item['matches'] if match['broadcasts']]} for item in filtered_compe]
        
        # filter by matches empty
        filtered = [comp for comp in filtered_broad if comp['matches']]
        
        log_message('INFO', f"List original: {len(data)} competitions, List filtered: {len(filtered_compe)} competitions")
        
        return filtered
    else:
        return []