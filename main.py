from livesoccertv_utils import get_main_matches
from database_utils import countries_broadcast_en, main_leagues_en
from twitter_utils import create_tweet_with_media
from images_utils import create_image_post




#for post in posts:
#    test =  get_list_for_post(post, countries_broadcast_en)
#    create_image_post(post.capitalize(),test)
    
#print(test)
#create_tweet_with_media('La Liga 5 Mayo 2023', image_la_liga)

all_matches = get_main_matches(countries_broadcast_en, '2023-05-09')
print(len(all_matches))
print(all_matches)