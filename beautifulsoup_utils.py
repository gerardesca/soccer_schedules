from requests_utils import make_request
from logging_utils import log_message
from bs4 import BeautifulSoup
import datetime
import logging

def get_current_date(format):
    now = datetime.datetime.now()
    date_str = now.strftime(format)
    return date_str

def parse_html(html, parser='lxml'):
    soup = BeautifulSoup(html, parser)
    return soup