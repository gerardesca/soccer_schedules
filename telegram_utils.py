from keys import CHAT_ID, TOKEN_TELEGRAM
from requests_utils import send_post_request
from logging_utils import log_message


def send_image_with_msg(msg: str = '', image_path: str = ''):
    
    try:
        with open(image_path, 'rb') as file:
            log_message('INFO', f"File {image_path} opened successfully.")
            
            image_to_send = {'photo':file}
            end_point = f'https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendPhoto?chat_id={CHAT_ID}&caption={msg}'
            send_post_request(end_point, image_to_send)
            log_message('INFO', f"Message sent successfully to Telegram.")
    
    except FileNotFoundError:
        log_message('ERROR', f"File {image_path} not found.")
        return None
    
    except IOError as e:
        log_message('ERROR', f"Failed to open the file {image_path}")
        log_message('ERROR', f"IOError: {e}")
        return None
    
def send_msg(msg: str):
    end_point = f'https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage?chat_id={CHAT_ID}&text={msg}'
    send_post_request(end_point, {})
    log_message('INFO', f"Message sent successfully to Telegram.")