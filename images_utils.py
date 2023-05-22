from PIL import Image, ImageDraw, ImageFont, ImageFilter
from logging_utils import log_message
import os

PATH='./images/'
PATH_COMPETITIONS='./images/competitions/'

size_competition_title = 30
size_match_title = 20
size_broadcasts_title = 15
font_competition = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size_competition_title)
font_match = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size_match_title)
font_broadcasts_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size_broadcasts_title)


def get_width_px_by_text(text: str, font):
    left, top, right, bottom = font.getbbox(text)
    return right - left


def get_height_px_by_text(text: str, font):
    left, top, right, bottom = font.getbbox(text)
    return bottom - top


def get_max_text_width(content: list, margin: int = 0) -> int:
    msg_width=0
    for compe in content:
        competition = compe['competition'].split('-')[1].strip()
        
        # get width title competition in px
        width = get_width_px_by_text(competition, font_competition)
        if width > msg_width:
            msg_width = width
        
        for matche in compe['matches']:
            # get string title match
            title = f"{matche['date']} | {matche['title']} | {matche['time_utc-6h']} CST"
            
            # get width title match in px
            width = get_width_px_by_text(title, font_match)
            if width > msg_width:
                msg_width = width
            
            for broadcasts in matche['broadcasts']:
                
                if isinstance(broadcasts, str):
                    width = get_width_px_by_text(broadcasts, font_broadcasts_title)
                    if width > msg_width:
                        msg_width = width
                else:
                    # get string broadcasts match
                    tvs = f"{broadcasts['country']}: {', '.join(str(channel) for channel in broadcasts['channels'])}"
                
                    #get width broadcasts match in px
                    width = get_width_px_by_text(tvs, font_broadcasts_title)
                    if width > msg_width:
                        msg_width = width
                
    return msg_width + margin*2


def count_text_height(content: list, space_between_text: int = 0, margin: int = 0) -> int:
    
    # get footer image
    footer_imagen = Image.open(PATH + 'footer.png')
    
    # sum margin plus footer height
    msg_height = margin*2 + footer_imagen.height
    
    for compe in content:
        competition = compe['competition'].split('-')[1].strip()
        
        # get height title match in px
        msg_height += get_height_px_by_text(competition, font_competition) + space_between_text
        
        for matche in compe['matches']:
            # get string title match
            title = f"{matche['date']} | {matche['title']} | {matche['time_utc-6h']} CST"
            
            # get height title match in px
            msg_height += get_height_px_by_text(title, font_match) + space_between_text
            
            for broadcasts in matche['broadcasts']:
                
                if isinstance(broadcasts, str):
                    msg_height += get_height_px_by_text(broadcasts, font_broadcasts_title) + space_between_text
                else:
                    # get string broadcasts match
                    tvs = f"{broadcasts['country']}: {', '.join(str(channel) for channel in broadcasts['channels'])}"
                
                    # get height broadcasts match in px
                    msg_height += get_height_px_by_text(tvs, font_broadcasts_title) + space_between_text
                
        msg_height += space_between_text
                
    return msg_height


def create_image_post(content: list,
                      name: str = '',
                      margin = 20,
                      x_start=0,
                      y_start=0, 
                      space_between_text = 10, 
                      background = (255,255,255),
                      color_competition = (0, 0, 0),
                      color_match = (0, 0, 0),
                      color_broadcast = (0, 0, 0),
                      color_lines = (0,0,0),
                      width_line = 1):
    
    if len(content) == 0:
        log_message('INFO', "There are no competitions to create the image post")
        return
    
    # get footer image
    footer_imagen = Image.open(PATH + 'footer.png')
    
    # get size image
    image_width = get_max_text_width(content, margin=margin)
    image_height = count_text_height(content, space_between_text=space_between_text, margin=margin)
    
    log_message('INFO', f"Start to create image post. Width={image_width}px, Height={image_height}px")
    
    # create image
    image = Image.new('RGB', (image_width, image_height), color = background)
    draw = ImageDraw.Draw(image)
    
    # initial cordinates
    y = y_start + margin
    x = x_start + margin
    
    # draw margin lines
    draw.line([(margin/2, margin/2), (margin/2,  image_height-margin/2)], fill=color_lines, width=width_line)  # left line
    draw.line([(margin/2, margin/2), (image_width-margin/2, margin/2)], fill=color_lines, width=width_line)  # top line
    draw.line([(margin/2, image_height-margin/2), (image_width-margin/2, image_height-margin/2)], fill=color_lines, width=width_line)  # up line
    draw.line([(image_width-margin/2, margin/2), (image_width-margin/2, image_height-margin/2)], fill=color_lines, width=width_line)  # right line
    
    for compe in content:
        competition = compe['competition'].split('-')[1].strip()
        compe_image = Image.open(PATH_COMPETITIONS + compe['competition'] + '.png')
        
        # write title competition
        draw.text((x + compe_image.width + space_between_text, y), competition, fill=color_competition, font=font_competition)
        image.paste(compe_image,(x, y), compe_image.split()[3])
        # get height title competition in px
        y += get_height_px_by_text(competition, font_competition) + space_between_text

        for matche in compe['matches']:
            # get string title match
            title = f"{matche['date']} | {matche['title']} | {matche['time_utc-6h']} CST"
            
            # write matches
            draw.text((x, y), title, fill=color_match, font=font_match)
            # get height title match in px
            y += get_height_px_by_text(title, font_match) + space_between_text
            
            for broadcasts in matche['broadcasts']:
                
                if isinstance(broadcasts, str):
                    # write broadcasts
                    draw.text((x, y), broadcasts, fill=color_broadcast, font=font_broadcasts_title)
                    # get height broadcasts match in px
                    y += get_height_px_by_text(broadcasts, font_broadcasts_title) + space_between_text
                else:
                    # get string broadcasts match
                    tvs = f"{broadcasts['country']}: {', '.join(str(channel) for channel in broadcasts['channels'])}"
                
                    draw.text((x, y), tvs, fill=color_broadcast, font=font_broadcasts_title)
                    # get height broadcasts match in px
                    y += get_height_px_by_text(tvs, font_broadcasts_title) + space_between_text
        y += space_between_text
    
    # paste footer image
    image.paste(footer_imagen,(int((image.width - footer_imagen.width) / 2), y))
    image.filter(ImageFilter.SHARPEN)
    image_save_path = PATH + name + '.png'
    image.save(image_save_path)
    
    log_message('INFO', "Image created successfully")
    
    return image_save_path


def delete_image(file_path):
    """
    Deletes an image file given its file path.

    Args:
        file_path (str): The file path of the image to be deleted.
    """
    try:
        # Check if the file exists
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)
            log_message('INFO', f"Image at {file_path} deleted successfully.")
        else:
            log_message('INFO', f"Image at {file_path} does not exist.")
    except OSError as e:
        log_message('ERROR', f"Error occurred while deleting image at {file_path}: {e}")