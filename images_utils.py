from PIL import Image, ImageDraw, ImageFont

PATH='./images/'
PATH_COMPETITIONS='./images/competitions/'
size_font = 30
font = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf', size_font)


def get_width_px_by_text(text):
    left, top, right, bottom = font.getbbox(text)
    return right - left


def get_height_px_by_text(text):
    left, top, right, bottom = font.getbbox(text)
    return bottom - top


def count_text_height(content: list, space_between_text: int = 10):
    msg_height = 0
    
    for text in content:
        # get string title match
        title = f"{text['title']} | {text['date']} {text['time_utc-6h']} CST"
        
        # get height title match in px
        msg_height += get_height_px_by_text(title) + space_between_text
            
        for broadcasts in text['broadcasts']:
            # get string broadcasts match
            tvs = f"{broadcasts['country']}: {', '.join(str(channel) for channel in broadcasts['channels'])}"
            
            # get height broadcasts match in px
            msg_height += get_height_px_by_text(tvs) + space_between_text
                
        msg_height += space_between_text
                
    return msg_height

def get_max_text_width(content: list):
    msg_width= 0
    
    for text in content:
        # get string title match
        title = f"{text['title']} | {text['date']} {text['time_utc-6h']} CST"
        
        # get width title match in px
        width = get_width_px_by_text(title)
        if width > msg_width:
            msg_width = width
            
        for broadcasts in text['broadcasts']:
            # get string broadcasts match
            tvs = f"{broadcasts['country']}: {', '.join(str(channel) for channel in broadcasts['channels'])}"
            
            #get width broadcasts match in px
            width = get_width_px_by_text(tvs)
            if width > msg_width:
                msg_width = width
                
    return msg_width


def get_size_image(content: list, space_between_text: int = 10):
    
    # get footer image
    footer_imagen = Image.open(PATH + 'footer.png')
    # sum footer image height to total images_height
    images_height = footer_imagen.height
    
    text_height = 0
    max_text_width_list = []
    for competition in content:
        # get competition name
        list_competition = competition.get(''.join(competition.keys()))
        # sum each competition image height
        images_height += Image.open(PATH_COMPETITIONS + ''.join(competition.keys()).lower() + '.png').height + space_between_text
        # sum each text competition
        text_height += count_text_height(list_competition, space_between_text=space_between_text)
        # store each max text competition width
        max_text_width_list.append(get_max_text_width(list_competition))
        
    total_height = images_height + text_height
    total_width = max(max_text_width_list)
    
    return total_width, total_height


def create_image_post(post_title: str,
                      content: list, 
                      start_width = 1080, 
                      start_height = 200, 
                      margin = 20, 
                      x_start=0, 
                      y_start=0, 
                      space_between_text = 10, 
                      background = (255,255,255),
                      color_title = (0,0,0),
                      color_broadcast = (97,97,97)):
    
    if len(content) == 0:
        return
    
    # get footer image
    footer_imagen = Image.open(PATH + 'footer.png')
    
    # min space required
    min_width, min_height = get_size_image(content, space_between_text)
    min_width += margin*2
    min_height += margin*2
    
    # create main image
    if min_width > start_width and min_height > start_height:
        image = Image.new('RGB', (min_width, min_height), color = background)
    elif min_width > start_width and min_height < start_height:
        image = Image.new('RGB', (min_width, start_height), color = background)
    elif min_width < start_width and min_height > min_height:
        image = Image.new('RGB', (start_width, min_height), color = background)
    else:
        image = Image.new('RGB', (start_width, start_height), color = background)
    
    draw = ImageDraw.Draw(image)
    
    y = y_start + int(margin)
    x = x_start + int(margin)
    
    for competition in content:
        # get competition name
        league = ''.join(competition.keys())
        image_league = Image.open(PATH_COMPETITIONS + league.lower() + '.png')
        image.paste(image_league,(int((image.width - image_league.width) / 2), y))
        y += image_league.height + space_between_text
        
        for matches in competition[league]:
            date = matches['date'].replace(' ','')
            title = f"{matches['title']} | {matches['date']} {matches['time_utc-6h']} CST"
            # write text
            draw.text((x, y), title, fill=color_title, font=font)
            # get height title match in px
            y += get_height_px_by_text(title) + space_between_text
            
            for broadcasts in matches['broadcasts']:
                # get string broadcasts match
                tvs = f"{broadcasts['country']}: {', '.join(str(channel) for channel in broadcasts['channels'])}"
                draw.text((x, y), tvs, fill=color_broadcast, font=font)
                # get height broadcasts match in px
                y += get_height_px_by_text(tvs) + space_between_text
            y += space_between_text
            
    # paste footer image
    image.paste(footer_imagen,(int((image.width - footer_imagen.width) / 2), y))
    image_save_path = PATH + date + post_title + '.png'
    image.save(image_save_path)

    return image_save_path