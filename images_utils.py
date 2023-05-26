from settings import PATH, PATH_COMPETITIONS, PATH_SCHEDULES, PATH_FLAGS, FONT
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from utils import create_directory, split_text, remove_text_special
from logging_utils import log_message
import os

size_title_post = 28
size_competition_title = 30
size_match_title = 23
size_broadcasts_title = 17
font_title_post = ImageFont.truetype(FONT, size_title_post)
font_competition = ImageFont.truetype(FONT, size_competition_title)
font_match = ImageFont.truetype(FONT, size_match_title)
font_broadcasts_title = ImageFont.truetype(FONT, size_broadcasts_title)


def get_width_px_by_text(text: str, font):
    left, top, right, bottom = font.getbbox(text)
    return right - left


def get_height_px_by_text(text: str, font):
    left, top, right, bottom = font.getbbox(text)
    return bottom - top


def get_max_text_width(content: list, margin: int = 0, indentation=0) -> int:
    msg_width=0
    for compe in content:
        competition = split_text(compe['competition'])
        
        # get width title competition in px
        width = get_width_px_by_text(competition, font_competition)
        if width > msg_width:
            msg_width = width
        
        for matche in compe['matches']:
            # get string title match
            title = f"{matche['title']} | {matche['time_utc-6h']} CST"
            
            # get width title match in px
            width = get_width_px_by_text(title, font_match)
            if width > msg_width:
                msg_width = width
            
            for broadcasts in matche['broadcasts']:
                
                if isinstance(broadcasts, str):
                    width = get_width_px_by_text(broadcasts, font_broadcasts_title) + indentation
                    if width > msg_width:
                        msg_width = width
                else:
                    # get flag country
                    flag_country = Image.open(PATH_FLAGS + broadcasts['country'] + '.png')
                    
                    # get string broadcasts match
                    tvs = f"  {', '.join(str(channel) for channel in broadcasts['channels'])}"
                
                    #get width broadcasts match in px
                    width = get_width_px_by_text(tvs, font_broadcasts_title) + flag_country.width + indentation
                    if width > msg_width:
                        msg_width = width
                
    return msg_width + margin*2


def count_text_height(content: list, space_between_text: int = 0, margin: int = 0) -> int:
    
    # get footer image
    footer_imagen = Image.open(PATH + 'footer.png')
    
    # sum margin plus footer height
    msg_height = margin*2 + footer_imagen.height
    
    for compe in content:
        competition = split_text(compe['competition'])
        
        # get height title match in px
        msg_height += get_height_px_by_text(competition, font_competition) + space_between_text
        
        for matche in compe['matches']:
            # get string title match
            title = f"{matche['title']} | {matche['time_utc-6h']} CST"
            
            # get height title match in px
            msg_height += get_height_px_by_text(title, font_match) + space_between_text
            
            for broadcasts in matche['broadcasts']:
                
                if isinstance(broadcasts, str):
                    msg_height += get_height_px_by_text(broadcasts, font_broadcasts_title) + space_between_text
                else:
                    # get flag country
                    flag_country = Image.open(PATH_FLAGS + broadcasts['country'] + '.png')
                    
                    # get string broadcasts match
                    tvs = f"  {', '.join(str(channel) for channel in broadcasts['channels'])}"
                    # get height broadcasts match in px
                    tvs_height = get_height_px_by_text(tvs, font_broadcasts_title)
                    
                    if flag_country.height > tvs_height:
                        msg_height += flag_country.height + space_between_text
                    else:
                        msg_height += tvs_height + space_between_text
                
        msg_height += space_between_text*2
                
    return msg_height


def create_image_post(content: list,
                      name: str = '',
                      title_post: str = '',
                      margin = 20,
                      x_start=0,
                      y_start=0,
                      indentation = 10, 
                      space_between_text = 10, 
                      background = (255,255,255),
                      color_title_post = (0, 0, 0),
                      color_competition = (0, 0, 0),
                      color_match = (0, 0, 0),
                      color_broadcast = (0, 0, 0),
                      color_lines = (0,0,0),
                      width_line = 1):
    
    if len(content) == 0:
        log_message('INFO', "There are no competitions to create the image post")
        return
    
    # title
    title_height = get_height_px_by_text(title_post, font_title_post)
    title_width = get_width_px_by_text(title_post, font_title_post)
    
    # get footer image
    footer_imagen = Image.open(PATH + 'footer.png')
    
    # get size image
    text_width = get_max_text_width(content, margin=margin, indentation=indentation)
    if text_width > title_width:
        image_width = text_width
    else:
        image_width = title_width + margin*2
        
    image_height = count_text_height(content, space_between_text=space_between_text, margin=margin) + title_height  + space_between_text*2
    
    log_message('INFO', f"Start to create image post. Width={image_width}px, Height={image_height}px")
    
    # create image
    image = Image.new('RGB', (image_width, image_height), color = background)
    draw = ImageDraw.Draw(image)
    
    # initial cordinates
    y = y_start + margin
    x = x_start + margin
    
    # write title
    draw.text((int((image.width - title_width) / 2), y), title_post, fill=color_title_post, font=font_title_post)
    y += title_height + space_between_text*2
    
    # draw margin lines
    draw.line([(margin/2, margin/2), (margin/2,  image_height-margin/2)], fill=color_lines, width=width_line)  # left line
    draw.line([(margin/2, margin/2), (image_width-margin/2, margin/2)], fill=color_lines, width=width_line)  # top line
    draw.line([(margin/2, image_height-margin/2), (image_width-margin/2, image_height-margin/2)], fill=color_lines, width=width_line)  # up line
    draw.line([(image_width-margin/2, margin/2), (image_width-margin/2, image_height-margin/2)], fill=color_lines, width=width_line)  # right line
    
    for compe in content:
        competition = split_text(compe['competition'])
        compe_image = Image.open(PATH_COMPETITIONS + remove_text_special(compe['competition']) + '.png')
        
        # write title competition
        draw.text((x + compe_image.width + space_between_text, y), competition, fill=color_competition, font=font_competition)
        image.paste(compe_image,(x, y), compe_image.split()[3])
        # get height title competition in px
        y += get_height_px_by_text(competition, font_competition) + space_between_text

        for matche in compe['matches']:
            # get string title match
            title = f"{matche['title']} | {matche['time_utc-6h']} CST"
            
            # write matches
            draw.text((x, y), title, fill=color_match, font=font_match)
            # get height title match in px
            y += get_height_px_by_text(title, font_match) + space_between_text
            
            for broadcasts in matche['broadcasts']:
                
                if isinstance(broadcasts, str):
                    # write broadcasts
                    draw.text((x+indentation, y), broadcasts, fill=color_broadcast, font=font_broadcasts_title)
                    # get height broadcasts match in px
                    y += get_height_px_by_text(broadcasts, font_broadcasts_title) + space_between_text
                else:
                    # get flag country
                    flag_country = Image.open(PATH_FLAGS + broadcasts['country'] + '.png')
                    image.paste(flag_country,(x+indentation, y), flag_country.split()[3])
                    
                    # get string broadcasts match
                    tvs = f"  {', '.join(str(channel) for channel in broadcasts['channels'])}"
                    # get height broadcasts match in px
                    tvs_height = get_height_px_by_text(tvs, font_broadcasts_title)
                    
                    draw.text((x+indentation+flag_country.width, y), tvs, fill=color_broadcast, font=font_broadcasts_title)
                    
                    if flag_country.height > tvs_height:
                        y += flag_country.height + space_between_text
                    else:
                        y += tvs_height + space_between_text
                    
        y += space_between_text*2
    
    # paste footer image
    image.paste(footer_imagen,(int((image.width - footer_imagen.width) / 2), y))
    image.filter(ImageFilter.SHARPEN)
    create_directory(PATH_SCHEDULES)
    image_save_path = PATH_SCHEDULES + name + '.png'
    image.save(image_save_path)
    
    log_message('INFO', "Image created successfully")
    
    return image_save_path


def delete_image(file_path: str):
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