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
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises an HTTPError if the status code indicates an error
        return response.content, response.status_code
    except requests.exceptions.HTTPError as http_error:
        # Log the error and re-raise the exception
        logging.error(f"HTTP error occurred: {http_error}")
    except requests.exceptions.RequestException as error:
        logging.exception(f"An error occurred: {error}")