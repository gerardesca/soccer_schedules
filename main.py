from beautifulsoup_utils import get_matches_from_futbolenvivo

url = 'https://www.futbolenvivomexico.com/competicion/liga-mexico'
print(get_matches_from_futbolenvivo(url, 'Liga MX'))