from requests_utils import make_request
from bs4 import BeautifulSoup
import datetime
import re

def get_current_date(format):
    now = datetime.datetime.now()
    date_str = now.strftime(format)
    return date_str

def parse_html(html, parser='html.parser'):
    soup = BeautifulSoup(html, parser)
    return soup

def get_links_matches(url):
    # Make a request
    content, status_code = make_request(url)

    if status_code == 200:
        # Parse the HTML
        soup = parse_html(content)
        match_links = []

        # Find all 'tr' elements with class 'livecomp'
        date = get_current_date('%A, %d %B %Y')
        livecomp = soup.find_all('tr', {'class': 'livecomp'})

        # Loop through each 'tr' element with class 'livecomp'
        for lc in livecomp:
            # Check if the date matches the current date
            if re.search(date, str(lc)):
                # Loop through the siblings of the livecomp row
                for sibling in lc.find_next_siblings():
                    # Check if the sibling is another livecomp row
                    if sibling.has_attr('class') and 'livecomp' in sibling['class']:
                        # If it is, break out of the loop and move to the next livecomp row
                        break
                    # If the sibling is a matchrow, append it to the list of match rows
                    elif sibling.has_attr('class') and 'matchrow' in sibling['class']:
                        td = sibling.find_all('td')[2]  # Get the third td element
                        link = td.find('a')  # Find the first a element
                        href = link.get('href')  # Get the href attribute
                        match_links.append(url[:28]+href)
        return match_links