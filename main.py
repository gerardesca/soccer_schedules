from logging_utils import configure_logging
import beautifulsoup_utils

# Set up logging
configure_logging('app.log')

URL = 'https://www.livesoccertv.com/competitions/mexico/primera-division/'

links_matches = beautifulsoup_utils.get_links_matches(URL)