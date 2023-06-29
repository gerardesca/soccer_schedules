from logging_utils import log_message
import requests


def make_request(url: str, headers: dict = {}):
    """Sends a HTTP GET request to the specified URL.

    Args:
        url (str): The URL to send the request to.

    Returns:
        str: The response text
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            log_message('INFO', f"Successful requests to: {url} Status code: {response.status_code}")
            return response.text
    except requests.exceptions.HTTPError as http_error:
        log_message('ERROR', f"HTTP error occurred: {http_error}")
    except requests.exceptions.RequestException as error:
        log_message('ERROR', f"An error occurred: {error}")
        
        
def send_post_request(url: str, data: dict) -> None:
    """Sends a HTTP POST request to the specified URL and data.

    Args:
        url (str): The URL to send the request to.
        data (dict): The dict with files to send
    """
    try:
        response = requests.post(url, files=data)
        response.raise_for_status()

        if response.status_code == 200:
            log_message('INFO', f"Successful POST requests. Status code: {response.status_code}")
        else:
            log_message('ERROR', f"POST requests failed with Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        log_message('ERROR', f"An error occurred while sending the POST request: {str(e)}")