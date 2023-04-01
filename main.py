from logging_utils import configure_logging
from requests_utils import make_request
import beautifulsoup_utils

# Set up logging
configure_logging('app.log')

# Make a request
URL = 'https://www.livesoccertv.com/competitions/mexico/primera-division/'
content, status_code = make_request(URL)

if status_code == 200:
    links_matches = [URL[:28]+match for match in beautifulsoup_utils.get_links_matches(content)]
    print(links_matches)