from logging_utils import configure_logging
from requests_utils import make_request

# Set up logging
configure_logging('app.log')

# Make a request
URL = 'https://www.livesoccertv.com/competitions/mexico/primera-division/'
content, status_code = make_request(URL)

if status_code == 200:
    print(content)