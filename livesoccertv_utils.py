from requests_utils import make_request
from logging_utils import log_message
from utils import convert_time, get_current_date_by_format
from bs4 import BeautifulSoup
import time

URL_BASE = 'https://www.livesoccertv.com/'
HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"}


def parse_html(html, parser='lxml'):
    # Create a BeautifulSoup object from the HTML string using the specified parser
    soup = BeautifulSoup(html, parser)
    
    # Return the BeautifulSoup object
    return soup


def get_broadcasts_by_match(url: str, list_countries_broadcast: list) -> list:
    """
    Return a list with broadcasts filtered by list_countries_broadcasts
    If match dont have any broadcast by list_countries_broadcasts, Return a empty list
    """
    
    content = make_request(url, headers=HEADER)
    soup = parse_html(content, parser='html.parser')
    log_message('INFO', f"Start Scraping to: {url}")
    
    main_table = soup.find('table', attrs={'id':'wc_channels'})
    
    try:
        broadcast_by_country = main_table.find_all('tr')
        
        broadcasts = []
        for broadcast in broadcast_by_country[:len(broadcast_by_country)-1]:
            country = broadcast.find_next('td').get_text()
            if country in list_countries_broadcast:
                tvs = [tv.get_text() for tv in broadcast.find_all('a')]
                dict = {'country':country,
                        'channels':tvs}
                broadcasts.append(dict)
        
        return broadcasts

    except:
        log_message('WARNING', f"There arent broadcast")
        return []


def get_main_matches(list_countries_broadcast: list, date: str = get_current_date_by_format(), language: str = '') -> list:
    """
    Return a list with all day main matches from livesoccer
    """
    
    # main url
    language = '' if language == '' else language + '/'
    url = URL_BASE + language + 'schedules/' + date + '/'
    
    # list will be return
    list_matches_by_competition = []
    
    # make request and get soup object
    content = make_request(url, headers=HEADER)
    soup = parse_html(content, parser='html.parser')
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
            list_matches_by_competition.append(dict_competition)
        # The other rows are matches
        else:
            count_matches += 1
            # find its competition from each match (previus)
            competition = row.find_previous('tr', class_='sortable_comp').get_text().strip()
            
            # find elements by each match
            match_title = row.find('a').get_text()
            time_hour = row.find(lambda tag: tag.name == 'span' and tag.get('df') and 'ts' in tag.get('class', []))
            url = row.find('a')['href']
            url = URL_BASE + url[1:]
            
            # create dictionary
            dict_matches_by_competition = {'title':match_title,
                                        'date':date,
                                        'time_utc': 'TBA' if time_hour is None else convert_time(time_hour.get_text().strip(), 4),
                                        'time_utc-4h': 'TBA' if time_hour is None else time_hour.get_text().strip(), #EDT New York
                                        'time_utc-5h': 'TBA' if time_hour is None else convert_time(time_hour.get_text().strip(), 4-6), #CDT Houston
                                        'time_utc-6h': 'TBA' if time_hour is None else convert_time(time_hour.get_text().strip(), 4-6), #CST CDMX
                                        'time_utc-7h': 'TBA' if time_hour is None else convert_time(time_hour.get_text().strip(), 4-7), #PDT Los angeles
                                        'url': url,
                                        'broadcasts': get_broadcasts_by_match(url, list_countries_broadcast)}
            
            time.sleep(2)
            
            # find competition and store match in its competition
            for comp in list_matches_by_competition:
                if comp['competition'] == competition:
                    comp['matches'].append(dict_matches_by_competition)
    
    log_message('INFO', f"Get {len(list_matches_by_competition)} main competitions and {count_matches} matches in total")
                    
    return list_matches_by_competition


def filtered_competitions(all_competitions: list, competitions: list) -> list:
    """
    Return a list filtered by competition, the list 'competitions' has the main competitions
    Return message to matches without broadcasts
    """
    filtered = [compe for compe in all_competitions if compe['competition'] in competitions]
    
    for compe in filtered:
        for macthes in compe['matches']:
            if macthes['broadcasts'] == []:
                macthes['broadcasts'] = ['Sin transmisión disponible']
    
    log_message('INFO', f"List original: {len(all_competitions)} competitions, List filtered: {len(filtered)} competitions")
    
    return filtered