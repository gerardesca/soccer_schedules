from beautifulsoup_utils import get_matches_from_livesoccertv
from utils import COMPETITIONS_SOCCERLIVETV

liga_mx = get_matches_from_livesoccertv(COMPETITIONS_SOCCERLIVETV['Liga MX']['url'])
print(liga_mx)