import logging
import requests

def make_request(url):
    """Sends a HTTP GET request to the specified URL.

    Args:
        url (str): The URL to send the request to.

    Returns:
        tuple: A tuple containing the response content and status code.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the status code indicates an error
        return response.content, response.status_code
    except requests.exceptions.RequestException as e:
        # Log the error and re-raise the exception
        logging.error(f'Error making request to {url}: {e}')
        raise