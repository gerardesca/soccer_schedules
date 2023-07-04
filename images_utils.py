from settings import IMG_MAIN_PATH, IMG_SCHEDULES_PATH, FONT, MAX_HEIGHT_IMAGE
from utils import create_directory, split_text, remove_text_special, convert_time
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from logging_utils import log_message


class ImageV1:
    
    def __init__(self,
                 database, 
                 margin: int = 20, 
                 x_start: int =0, 
                 y_start: int =0, 
                 indentation: int = 10, 
                 space_between_text: int = 10, 
                 background = (255,255,255), 
                 color_title = (18, 5, 5), 
                 color_competition = (0, 0, 0),
                 color_match = (0, 76, 101),
                 color_broadcast = (0, 120, 62)) -> None:
        
        self.margin = margin
        self.x_start = x_start
        self.y_start = y_start
        self.indentation = indentation
        self.space_between_text = space_between_text
        self.background = background
        self.color_title = color_title
        self.color_competition = color_competition
        self.color_match = color_match
        self.color_broadcast = color_broadcast
        
        # fonts size and default Font by settings
        self.size_title_post = 28
        self.size_title_competition = 30
        self.size_title_match = 23
        self.size_title_broadcasts = 17
        self.font_title = ImageFont.truetype(FONT, self.size_title_post)
        self.font_title_competition = ImageFont.truetype(FONT, self.size_title_competition)
        self.font_title_match = ImageFont.truetype(FONT, self.size_title_match)
        self.font_title_broadcasts = ImageFont.truetype(FONT, self.size_title_broadcasts)
        
        # connection to db
        self.database = database
    
    
    def _get_max_text_width(self, content: list) -> int:
                
        # get footer image
        footer_imagen = open_image(IMG_MAIN_PATH + 'footer.png')
        footer_imagen_width = 0 if footer_imagen is None else footer_imagen.width
        
        msg_width = footer_imagen_width
        
        for compe in content:
            
            # title competition
            compe_image = open_image(self.database.get_path_image_competition(compe['competition']))
            compe_image_width = 0 if compe_image is None else compe_image.width
            competition = split_text(compe['competition'])
            
            # get width title competition in px
            width = compe_image_width + get_width_px_by_text(competition, self.font_title_competition) + self.space_between_text
            if width > msg_width:
                msg_width = width
            
            # title matches
            for matche in compe['matches']:
                # get string title match
                title = f"{matche['title']} | {convert_time(matche['time_server'], 'America/Mexico_City')}"
                
                # get width title match in px
                width = get_width_px_by_text(title, self.font_title_match)
                if width > msg_width:
                    msg_width = width
                
                # title broadcasts
                for broadcasts in matche['broadcasts']:
                    
                    if isinstance(broadcasts, str):
                        width = get_width_px_by_text(broadcasts, self.font_title_broadcasts) + self.indentation
                        if width > msg_width:
                            msg_width = width
                    else:
                        # get flag country
                        flag_country = open_image(self.database.get_path_image_flag(broadcasts['country']))
                        flag_country_width = 0 if flag_country is None else flag_country.width
                        
                        # get string broadcasts match
                        tvs = f"  {', '.join(str(channel) for channel in broadcasts['channels'])}"
                    
                        #get width broadcasts match in px
                        if flag_country:
                            width = get_width_px_by_text(tvs, self.font_title_broadcasts) + flag_country_width + self.indentation
                        else:
                            width = get_width_px_by_text(tvs, self.font_title_broadcasts) + get_width_px_by_text(broadcasts['country']+': ', self.font_title_broadcasts) + self.indentation
                            
                        if width > msg_width:
                            msg_width = width
                    
        return msg_width + self.margin*2
    
    
    def _count_text_height(self, content: list) -> int:
    
        # get footer image
        footer_imagen = open_image(IMG_MAIN_PATH + 'footer.png')
        footer_imagen_height = 0 if footer_imagen is None else footer_imagen.height
        
        # sum margin plus footer height
        msg_height = self.margin*2 + footer_imagen_height
        
        for compe in content:
            competition = split_text(compe['competition'])
            
            # get height title match in px
            msg_height += get_height_px_by_text(competition, self.font_title_competition) + self.space_between_text
            
            for matche in compe['matches']:
                # get string title match
                title = f"{matche['title']} | {convert_time(matche['time_server'], 'America/Mexico_City')}"
                
                # get height title match in px
                msg_height += get_height_px_by_text(title, self.font_title_match) + self.space_between_text
                
                for broadcasts in matche['broadcasts']:
                    
                    if isinstance(broadcasts, str):
                        msg_height += get_height_px_by_text(broadcasts, self.font_title_broadcasts) + self.space_between_text
                    else:
                        # get flag country
                        flag_country = open_image(self.database.get_path_image_flag(broadcasts['country']))
                        flag_country_height = 0 if flag_country is None else flag_country.height
                        
                        # get string broadcasts match
                        tvs = f"  {', '.join(str(channel) for channel in broadcasts['channels'])}"
                        
                        # get height broadcasts match in px
                        tvs_height = get_height_px_by_text(tvs, self.font_title_broadcasts)
                        
                        if flag_country_height > tvs_height:
                            msg_height += flag_country_height + self.space_between_text
                        else:
                            msg_height += tvs_height + self.space_between_text
                    
            msg_height += self.space_between_text*2
                    
        return msg_height
        
        
    def create_image(self, content: list, name: str, title: str) -> str:
                
        if len(content) == 0:
            log_message('INFO', "There are no competitions to create the image post")
            return
        
        # title
        title_height = get_height_px_by_text(title, self.font_title)
        title_width = get_width_px_by_text(title, self.font_title)
        
        # get footer image
        footer_imagen = open_image(IMG_MAIN_PATH + 'footer.png')
        
        # get size image
        content_width = self._get_max_text_width(content)
        image_width = content_width if content_width > title_width else title_width + self.margin*2
        image_height = self._count_text_height(content) + title_height + self.space_between_text*2
        log_message('INFO', f"Start to create image post. Width={image_width}px, Height={image_height}px")
        
        # create image
        image = Image.new('RGB', (image_width, image_height), color = self.background)
        draw = ImageDraw.Draw(image)
        
        # initial cordinates
        y = self.y_start + self.margin
        x = self.x_start + self.margin
        
        # write title
        draw.text((int((image.width - title_width) / 2), y), title, fill=self.color_title, font=self.font_title)
        y += title_height + self.space_between_text*2
        
        for compe in content:
            competition = split_text(compe['competition'])
            compe_image = open_image(self.database.get_path_image_competition(compe['competition']))
            compe_image_width = 0 if compe_image is None else compe_image.width
            
            # write title competition
            draw.text((x + compe_image_width + self.space_between_text, y), competition, fill=self.color_competition, font=self.font_title_competition)
            if compe_image:
                image.paste(compe_image,(x, y), compe_image.split()[3])
            # get height title competition in px
            y += get_height_px_by_text(competition, self.font_title_competition) + self.space_between_text

            for matche in compe['matches']:
                # get string title match
                title_match = f"{matche['title']} | {convert_time(matche['time_server'], 'America/Mexico_City')}"
                
                # write matches
                draw.text((x, y), title_match, fill=self.color_match, font=self.font_title_match)
                # get height title match in px
                y += get_height_px_by_text(title_match, self.font_title_match) + self.space_between_text
                
                for broadcasts in matche['broadcasts']:
                    
                    if isinstance(broadcasts, str):
                        # write broadcasts
                        draw.text((x+self.indentation, y), broadcasts, fill=self.color_broadcast, font=self.font_title_broadcasts)
                        # get height broadcasts match in px
                        y += get_height_px_by_text(broadcasts, self.font_title_broadcasts) + self.space_between_text
                    else:
                        # get flag country
                        flag_country = open_image(self.database.get_path_image_flag(broadcasts['country']))
                        flag_country_width = 0 if flag_country is None else flag_country.width
                        flag_country_height = 0 if flag_country is None else flag_country.height
                        text_country_width = 0 if flag_country else get_width_px_by_text(broadcasts['country']+': ', self.font_title_broadcasts)

                        if flag_country:
                            image.paste(flag_country,(x+self.indentation, y), flag_country.split()[3])
                        else:
                            draw.text((x+self.indentation, y), broadcasts['country']+': ', fill=self.color_broadcast, font=self.font_title_broadcasts)
                        
                        # get string broadcasts match
                        tvs = f"  {', '.join(str(channel) for channel in broadcasts['channels'])}"
                        # get height broadcasts match in px
                        tvs_height = get_height_px_by_text(tvs, self.font_title_broadcasts)
                        
                        draw.text((x+self.indentation+flag_country_width+text_country_width, y), tvs, fill=self.color_broadcast, font=self.font_title_broadcasts)
                        
                        if flag_country_height > tvs_height:
                            y += flag_country_height + self.space_between_text
                        else:
                            y += tvs_height + self.space_between_text
                        
            y += self.space_between_text*2
        
        # paste footer image
        if footer_imagen:
            image.paste(footer_imagen,(int((image.width - footer_imagen.width) / 2), y))
            
        image.filter(ImageFilter.SHARPEN)
        create_directory(IMG_SCHEDULES_PATH)
        image_save_path = IMG_SCHEDULES_PATH + name + '.png'
        image.save(image_save_path)
        
        log_message('INFO', f"Image created successfully {name} to post: {title}")
        
        return image_save_path
    
    
    def create_images_by_max_height(self, content: list, name: str, title: str, height_limit: int = MAX_HEIGHT_IMAGE) -> list:
        
        if len(content) == 0:
            log_message('INFO', "There are no competitions to create the image post")
            return
        
        result = []
        current = []
        
        # title
        title_height = get_height_px_by_text(title, self.font_title)
        
        for item in content:
            current.append(item)
            current_height = self._count_text_height(current) + title_height + self.margin*2

            if current_height > height_limit:
                current.pop()  # Remove the last added item
                result.append(current)
                current = [item]

        result.append(current)  # Add the remaining current list
        log_message('INFO', f"Split list to {len(result)} list(s)")
        
        # create images
        path_images = []
        for i, image in enumerate(result, start=1):
            image_rename = f'{i}_{name}'
            # create images
            path_image = self.create_image(image, image_rename, title)
            path_images.append(path_image)
        
        return path_images
        
        
def get_width_px_by_text(text: str, font) -> int:
    left, top, right, bottom = font.getbbox(text)
    return right - left


def get_height_px_by_text(text: str, font) -> int:
    left, top, right, bottom = font.getbbox(text)
    return bottom - top


def open_image(path: str):
    try:
        image = Image.open(path)
        log_message('INFO', f"Image opened successfully: {path}")
        return image
    except FileNotFoundError:
        log_message('ERROR', f"Image doesnt exists: {path}")
        return