from images_utils import split_list_by_height, create_image_post
from settings import MAX_HEIGHT_IMAGE
from livesoccertv_utils import filtered_competitions


def create_images_to_post(text: list, title: str, image_name: str, filter: list) -> str:
    path_images = [] 
    
    # filtered competitions
    filtered = filtered_competitions(text, filter)

    # split list
    number_images = split_list_by_height(filtered, MAX_HEIGHT_IMAGE, title)
    
    for i, image in enumerate(number_images, start=1):
        image_rename = f'{i}_{image_name}'
        # create images
        path_image = create_image_post(image, name=image_rename, title_post=title, color_title_post=(18, 5, 5), color_match=(0, 76, 101), color_broadcast=(0, 120, 62), color_lines=(254,254,254))
        path_images.append(path_image)