from utils import COMPETITIONS_SOCCERLIVETV
from requests_utils import make_request
from logging_utils import log_message
from utils import get_current_date
from bs4 import BeautifulSoup

URL_BASE = 'https://www.livesoccertv.com/'


def parse_html(html, parser='lxml'):
    # Create a BeautifulSoup object from the HTML string using the specified parser
    soup = BeautifulSoup(html, parser)
    
    # Return the BeautifulSoup object
    return soup


def get_matches_from_livesoccertv(url_competition, language=''):
    
    url = URL_BASE + language + url_competition
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"}
    
    # Find date according to language
    if language != '':
        schedule = get_current_date(language)
        if schedule is None:
            log_message('app.log', 'ERROR', f"Language: {language} isn't available")
            return []
    else:
        schedule = get_current_date()

    # Start scraping
    content = make_request(url, headers=header)
    soup = parse_html(content, parser='html.parser')
    log_message('app.log', 'INFO', "Start Scraping")

    # Find main table
    main_table = soup.find('div', class_='tab_container')
    schedules_table = main_table.find('table', class_='schedules')

    # Find matches by today date
    list_matches = []
    for matches_and_schedules in schedules_table:
        if schedule in matches_and_schedules.get_text():
            next_livecomp = matches_and_schedules.find_next('tr', class_='livecomp')
            next_element = matches_and_schedules.find_next('tr', class_='matchrow')
            while next_element and next_element != next_livecomp:
                if next_element.has_attr('id') and next_element.find('a'):
                    dict_match =  {
                        'id': next_element['id'],
                        'date': schedule,
                        'title': next_element.find('a')['title'],
                        'url': URL_BASE[:28] + next_element.find('a')['href']
                    }
                    list_matches.append(dict_match)
                next_element = next_element.find_next('tr')
    
    log_message('app.log', 'INFO', "Finish Scraping Successfully")
                
    if len(list_matches) > 0:
        msg = f"Games today: {str(len(list_matches))}"
        print(msg)
        log_message('app.log', 'INFO', msg)
        return list_matches
    else:
        msg = f"No games today in the: {url_competition}"
        print(msg)
        log_message('app.log', 'INFO', msg)
        return []


def get_broadcast_by_match(match_dict):
    
    url = match_dict['url']

    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"}

    # Start scraping
    content = make_request(url, headers=header)
    soup = parse_html(content, parser='html.parser')

    main_table = soup.find('div', class_='tab_content')
    broadcast_by_country = main_table.find_all('tr')

    broadcasts = []
    for broadcast in broadcast_by_country[:len(broadcast_by_country)-1]:
        country = broadcast.find_next('td').get_text()
        tvs = [tv.get_text() for tv in broadcast.find_all('a')]
        dict = {'country':country,
                'channels':tvs}
        broadcasts.append(dict)
    
    match_dict['broadcasts'] = broadcasts
    
    return match_dict

def get_list_matches_by_league(league, language=''):
    
    macthes = []
    for match in get_matches_from_livesoccertv(COMPETITIONS_SOCCERLIVETV[league]['url'], language):
        macthes.append(get_broadcast_by_match(match))
        
    return macthes