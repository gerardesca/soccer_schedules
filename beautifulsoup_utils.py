from requests_utils import make_request
from logging_utils import log_message
from bs4 import BeautifulSoup
from datetime import datetime
import re

def get_current_date(format):
    # Get the current datetime object
    now = datetime.datetime.now()
    
    # Format the datetime object to a string with the given format
    date_str = now.strftime(format)
    
    # Return the formatted date string
    return date_str

def parse_html(html, parser='lxml'):
    # Create a BeautifulSoup object from the HTML string using the specified parser
    soup = BeautifulSoup(html, parser)
    
    # Return the BeautifulSoup object
    return soup

def get_matches_from_futbolenvivo(url, competition):
    content = make_request(url)
    soup = parse_html(content, parser='html.parser')
    log_message('app.log', 'INFO', "Start Scraping")

    table_matches = None
    current_date = datetime.now().date()
    #current_date = datetime(2023, 4, 8).date()
    matches = []

    # Regular expression to detect date in any format
    date_regex = re.compile(r"\d{1,2}[/\.-]\d{1,2}[/\.-]\d{4}")

    for table in soup.find_all('table', class_='tablaPrincipal detalleVacio'):
        # Search for date in any format within table text
        match = date_regex.search(table.text)
        if match:
            date_table = datetime.strptime(match.group(), '%d/%m/%Y').date()
            if current_date == date_table:
                table_matches = table
                break
    
    # If the table of the matches of the day was not found, return message
    if not table_matches:
        msg = f"No game today in the: {competition}"
        log_message('app.log', 'INFO', msg)
        return msg
    
    # Find all items that contain the match time
    match_schedules = table_matches.find_all('td', class_='hora')

    # Find the home teams, away teams and channels for each match
    for schedule in match_schedules:
        # Find the td element that contains the local machine
        local = schedule.find_next('td', class_='local')

        # Find the td element containing the away team
        visit = local.find_next('td', class_='visitante')

        # Find the ul element containing the channel list
        channels = schedule.find_next('ul', class_='listaCanales')
        if channels:
            list_channels = [canal.text.strip() for canal in channels.find_all('li')]

        # Store the data in a dictionary
        match = {
            'competition': competition,
            'time_utc-6':schedule.text.strip(),
            'local': local.text.strip(),
            'visita': visit.text.strip(),
            'chanels': list_channels if channels else None
        }

        matches.append(match)

    log_message('app.log', 'INFO', "Finish Scraping Successfully")
    return matches