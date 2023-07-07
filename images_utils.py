from settings import IMG_MAIN_PATH, IMG_SCHEDULES_PATH, FONT_DEFAULT, MAX_HEIGHT_IMAGE, SIZE_LOGOS_TEAMS, TIMEZONES_FOR_IMAGE
from utils import create_directory, split_text, convert_time
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from requests_utils import make_request
from logging_utils import log_message
from io import BytesIO
import time


class ImageV1:
    
    def __init__(self,
                 database, 
                 margin: int = 20, 
                 x_start: int =0, 
                 y_start: int =0, 
                 indentation: int = 10,
                 space_between_elements: int = 10,
                 background: tuple = (255,255,255), 
                 color_title: tuple = (255, 255, 255),
                 color_box_title: tuple = (0, 0, 0),
                 color_competition: tuple = (0, 0, 0),
                 color_box_competition: tuple = (240, 240, 240),
                 color_match: tuple = (0, 0, 0),
                 color_schedules: tuple = (5, 69, 99),
                 color_broadcast: tuple = (0, 120, 62),
                 size_logos_teams: tuple = SIZE_LOGOS_TEAMS,
                 path_font_title: str = FONT_DEFAULT,
                 path_font_title_competition: str = FONT_DEFAULT,
                 path_font_title_match: str = FONT_DEFAULT,
                 path_font_title_schedules: str = FONT_DEFAULT,
                 path_font_title_broadcasts: str = FONT_DEFAULT) -> None:
        
        self.margin = margin
        self.x_start = x_start
        self.y_start = y_start
        self.indentation = indentation
        self.space_between_elements = space_between_elements
        self.background = background
        self.color_title = color_title
        self.color_box_title = color_box_title
        self.color_competition = color_competition
        self.color_box_competition = color_box_competition
        self.color_match = color_match
        self.color_schedules = color_schedules
        self.color_broadcast = color_broadcast
        self.size_logos_teams = size_logos_teams
        
        # fonts size and default Font by settings
        self.size_title_post = 28
        self.size_title_competition = 30
        self.size_title_match = 23
        self.size_title_schedules = 12
        self.size_title_broadcasts = 17
        self.font_title = ImageFont.truetype(path_font_title, self.size_title_post)
        self.font_title_competition = ImageFont.truetype(path_font_title_competition, self.size_title_competition)
        self.font_title_match = ImageFont.truetype(path_font_title_match, self.size_title_match)
        self.font_title_schedules = ImageFont.truetype(path_font_title_schedules, self.size_title_schedules)
        self.font_title_broadcasts = ImageFont.truetype(path_font_title_broadcasts, self.size_title_broadcasts)
        
        # connection to db
        self.database = database
        
        
    def _get_logos_from_url(self, url: str) -> Image:
        
        response = make_request(url, img_url=True)
        image = Image.open(BytesIO(response))
        image_resize = image.resize(self.size_logos_teams)
        time.sleep(1)
    
        return image_resize.convert('RGBA')
    
    
    def _get_size(self, content: list, title: str) -> int:
        
        # initial count variables
        width = 0
        height = 0
        
        
        """TITLE IMAGE"""
        # get title image and dimensions
        title_width, title_height = get_width_height_px_by_text(title, self.font_title)
        
        
        # get footer image
        self.footer_imagen = open_image(IMG_MAIN_PATH + 'footer.png')
        self.footer_imagen_width = 0 if self.footer_imagen is None else self.footer_imagen.width
        self.footer_imagen_height = 0 if self.footer_imagen is None else self.footer_imagen.height
        
        # sum margin plus footer height
        width = max([self.footer_imagen_width, title_width])
        height = self.footer_imagen_height + title_height + self.margin*2


        """COMPETITIONS"""
        for compe in content:
            
            # get title competition and dimensions
            competition_text = split_text(compe['competition'])
            competition_text_width, competition_text_height = get_width_height_px_by_text(competition_text, self.font_title_competition)

            # get image competition and dimensions
            competition_image = open_image(self.database.get_path_image_competition(compe['competition']))
            competition_image_width = 0 if competition_image is None else competition_image.width
            competition_image_height = 0 if competition_image is None else competition_image.height
            
            # get height competition
            if competition_text_height > competition_image_height:
                height += competition_text_height + self.space_between_elements
            else:
                height += competition_image_height + self.space_between_elements
            
            # get width competition
            width_comp = competition_text_width + competition_image_width + self.indentation
            if width_comp > width:
                width = width_comp
            
            
            """MATCHES"""
            for matche in compe['matches']:
                
                # get logos dimensions
                width_logos = self.size_logos_teams[0] if len(matche['logos']) == 2 else 0
                height_logos = self.size_logos_teams[1] if len(matche['logos']) == 2 else 0
                
                # get title match and dimensions
                match_text = matche['title']
                match_text_width, match_text_height = get_width_height_px_by_text(match_text, self.font_title_match)
                
                # box info match
                height_match_info = max([height_logos, match_text_height]) + self.space_between_elements
                width_match_info = width_logos*2 + self.indentation*2 + match_text_width
                
                # get schedules image
                schedules_image = open_image(IMG_MAIN_PATH + 'schedules.png')
                schedules_imagen_width = 0 if schedules_image is None else schedules_image.width
                schedules_imagen_height = 0 if schedules_image is None else schedules_image.height
                
                # get schedules and dimensions
                schedules = [convert_time(matche['time_server'], time_zone) + ' | ' if time_zone != TIMEZONES_FOR_IMAGE[-1] else convert_time(matche['time_server'], time_zone) for time_zone in TIMEZONES_FOR_IMAGE]
                text_schedules = f"  {''.join(sch for sch in schedules)}"
                width_text_schedules, height_text_schedules = get_width_height_px_by_text(text_schedules, self.font_title_schedules)
                
                # box schedules
                height_match_schedules = max([height_text_schedules, schedules_imagen_height])  + self.space_between_elements
                width_match_schedules = schedules_imagen_width + self.indentation*2 + width_text_schedules
                
                # get height for match
                height += height_match_info + height_match_schedules
                
                # get width for match
                width_match = max([width_match_info, width_match_schedules])
                if width_match > width:
                    width = width_match
                
                
                """BROADCASTS"""
                for broadcasts in matche['broadcasts']:
                    
                    # get image flag country and dimensions
                    flag_image = open_image(self.database.get_path_image_flag(broadcasts['country']))
                    flag_image_width = 0 if flag_image is None else flag_image.width
                    flag_image_height = 0 if flag_image is None else flag_image.height
                    
                    # get title broadcasts text
                    broadcasts_text = f"  {', '.join(str(channel) for channel in broadcasts['channels'])}"
                    broadcasts_text_width, broadcasts_text_height = get_width_height_px_by_text(broadcasts_text, self.font_title_broadcasts)

                    # get height for broadcast country
                    height += max([broadcasts_text_height, flag_image_height]) + self.space_between_elements
                    
                    # get width for broadcast country
                    width_broadcasts = flag_image_width + broadcasts_text_width + self.indentation*2
                    if width_broadcasts > width:
                        width = width_broadcasts
                        
            height += self.space_between_elements*4
            
        return width + self.margin*2, height + self.margin*2
    
    
    def create_image(self, content: list, name: str, title: str) -> str:
                
        if len(content) == 0:
            log_message('INFO', "There are no competitions to create the image post")
            return
        
        """TITLE IMAGE"""
        # get title image and dimensions
        title_width, title_height = get_width_height_px_by_text(title, self.font_title)
        
        """SIZE IMAGE"""
        # get total width and height
        width_image, height_image = self._get_size(content, title)
        log_message('INFO', f"Start to create image post. Width={width_image}px, Height={height_image}px")
        
        # create image
        image = Image.new('RGBA', (int(width_image), int(height_image)), color = self.background)
        draw = ImageDraw.Draw(image)
        
        
        # initial cordinates
        y = self.y_start + self.margin
        x = self.x_start + self.margin
        
        # draw box title
        draw.rectangle(((x, y), (image.width - self.margin, y + title_height+10)), fill=self.color_box_title, outline=None, width=0)
        
        # write title
        draw.text((int((image.width - title_width) / 2), y), title, fill=self.color_title, font=self.font_title)
        
        # coordinate y
        y += title_height + self.margin*2
        
        
        """COMPETITIONS"""
        for compe in content:
            
            # get title competition and dimensions
            competition_text = split_text(compe['competition'])
            competition_text_width, competition_text_height = get_width_height_px_by_text(competition_text, self.font_title_competition)
            
            # get image competition and dimensions
            competition_image = open_image(self.database.get_path_image_competition(compe['competition']))
            competition_image_width = 0 if competition_image is None else competition_image.width
            competition_image_height = 0 if competition_image is None else competition_image.height
            
            # create coordinates
            max_height_competition = competition_text_height if competition_text_height > competition_image_height else competition_image_height
            y_middle_point_competition = y + (max_height_competition/2)
            competition_width = competition_image_width + self.indentation + competition_text_width
            x_competition_image = int((image.width - competition_width) / 2)
            y_competition_image = int(y_middle_point_competition - competition_image_height/2)
            x_competition_text = int(x_competition_image + competition_image_width) + + self.indentation
            y_competition_text = int(y_middle_point_competition - competition_text_height/2)
            
            # draw box title competition
            draw.rectangle(((x, y-5),(image.width-self.margin, y+max_height_competition+7)), fill=self.color_box_competition, outline=None, width=0)
            
            if competition_image:
                # paste image competition
                image.paste(competition_image, (x_competition_image, y_competition_image), mask=competition_image)
                
            # write title competition
            draw.text((x_competition_text, y_competition_text), competition_text, fill=self.color_competition, font=self.font_title_competition)
            
            # coordinate y
            y += max_height_competition + self.space_between_elements


            """MATCHES"""
            for matche in compe['matches']:
                                
                # get logos dimensions
                width_logos = self.size_logos_teams[0] if len(matche['logos']) == 2 else 0
                height_logos = self.size_logos_teams[1] if len(matche['logos']) == 2 else 0
                
                # get title match and dimensions
                match_text = matche['title']
                match_text_width, match_text_height = get_width_height_px_by_text(match_text, self.font_title_match)
                
                # box info match
                height_match_info = max([height_logos, match_text_height])
                
                # get schedules image
                schedules_image = open_image(IMG_MAIN_PATH + 'schedules.png')
                schedules_imagen_width = 0 if schedules_image is None else schedules_image.width
                schedules_imagen_height = 0 if schedules_image is None else schedules_image.height
                
                # get schedules and dimensions
                schedules = [convert_time(matche['time_server'], time_zone) + ' | ' if time_zone != TIMEZONES_FOR_IMAGE[-1] else convert_time(matche['time_server'], time_zone) for time_zone in TIMEZONES_FOR_IMAGE]
                text_schedules = f"  {''.join(sch for sch in schedules)}"
                width_text_schedules, height_text_schedules = get_width_height_px_by_text(text_schedules, self.font_title_schedules)
                
                # box schedules
                height_match_schedules = max([height_text_schedules, schedules_imagen_height])
    
            
                # create coordinates
                y_middle_point_match_info = int(y + height_match_info/2)
                y_match_logos = int(y_middle_point_match_info - height_logos/2)
                y_match_title = int(y_middle_point_match_info - match_text_height/2)
                x_match_title = x + width_logos + self.indentation
                x_match_logo_away = x_match_title + match_text_width + self.indentation
                
                
                # write title and paste image logos
                draw.text((x_match_title, y_match_title), match_text, fill=self.color_match, font=self.font_title_match)
                
                if len(matche['logos']) == 2:
                    logo_home = self._get_logos_from_url(matche['logos'][0])
                    logo_away = self._get_logos_from_url(matche['logos'][1])
                    image.paste(logo_home, (x, y_match_logos), mask=logo_home)
                    image.paste(logo_away, (x_match_logo_away, y_match_logos), mask=logo_away)
                
                # coordinate y
                y += height_match_info + self.space_between_elements
                
                # create coordinates
                y_middle_point_match_schedules = int(y + height_match_schedules/2)
                y_match_schedules_image = int(y_middle_point_match_schedules - schedules_imagen_height/2)
                y_match_schedules_text = int(y_middle_point_match_schedules - height_text_schedules/2)
                x_match_schedules_image = int(x + self.indentation)
                x_match_schedules_text = int(x + schedules_imagen_width + self.indentation)
                
                
                # write shcedules and paste image
                draw.text((x_match_schedules_text, y_match_schedules_text), text_schedules, fill=self.color_schedules, font=self.font_title_schedules)
                
                if schedules_image:
                    image.paste(schedules_image, (x_match_schedules_image, y_match_schedules_image), mask=schedules_image)
                
                # coordinate y
                y += height_match_schedules + self.space_between_elements
                
                
                """BROADCASTS"""
                for broadcasts in matche['broadcasts']:
                    
                    # get image flag country and dimensions
                    flag_image = open_image(self.database.get_path_image_flag(broadcasts['country']))
                    text_image_width, text_image_height = get_width_height_px_by_text(f"{broadcasts['country']}: ", self.font_title_broadcasts)
                    flag_image_width = text_image_width if flag_image is None else flag_image.width
                    flag_image_height = text_image_height if flag_image is None else flag_image.height
                    
                    # get title broadcasts text and dimensions
                    broadcasts_text = f"  {', '.join(str(channel) for channel in broadcasts['channels'])}"
                    broadcasts_text_width, broadcasts_text_height = get_width_height_px_by_text(broadcasts_text, self.font_title_broadcasts)

                    
                    # create coordinates
                    height_max_broadcasts = max([flag_image_height, broadcasts_text_height])
                    y_middle_point_broadcasts = int(y + height_max_broadcasts/2)
                    y_broadcasts_flag = int(y_middle_point_broadcasts - flag_image_height/2)
                    y_broadcasts_text = int(y_middle_point_broadcasts - broadcasts_text_height/2)
                    x_broadcasts_flag = x + self.indentation
                    x_broadcasts_text = x_broadcasts_flag + flag_image_width + self.indentation
                    
                    # paste image flag country
                    if flag_image:
                        image.paste(flag_image, (x_broadcasts_flag, y_broadcasts_flag), mask=flag_image)
                    else:
                        draw.text((x_broadcasts_flag, y_broadcasts_flag), f"{broadcasts['country']}: ", fill=self.color_broadcast, font=self.font_title_broadcasts)
                        
                    # write broadcasts
                    draw.text((x_broadcasts_text, y_broadcasts_text), broadcasts_text, fill=self.color_broadcast, font=self.font_title_broadcasts)
                        
                    # coordinate y
                    y += height_max_broadcasts + self.space_between_elements
            
            
            y += self.space_between_elements*4
        
    
        # paste footer image
        if self.footer_imagen:
            image.paste(self.footer_imagen, (int((image.width - self.footer_imagen_width) / 2), int(y)))


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
        for item in content:
            current.append(item)
            width_content, height_content = self._get_size(current, title)
            current_height = height_content

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
        

def get_width_height_px_by_text(text: str, font) -> tuple:
    left, top, right, bottom = font.getbbox(text)
    return (right - left, bottom - top)


def open_image(path: str):
    try:
        image = Image.open(path)
        log_message('INFO', f"Image opened successfully: {path}")
        return image
    except FileNotFoundError:
        log_message('ERROR', f"Image doesnt exists: {path}")
        return