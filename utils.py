from datetime import datetime

COMPETITIONS_SOCCERLIVETV = {
    'Liga MX':{
        'country':'Mexico',
        'url':'competitions/mexico/primera-division/'
    },
    'La Liga':{
        'country':'Spain',
        'url':'competitions/spain/primera-division/'
    },
    'Premier League':{
        'country':'England',
        'url':'competitions/england/premier-league/'
    }
}

MONTHS_BY_LANGUAGE = [
                        {'es':'Enero'},
                        {'es':'Febrero'},
                        {'es':'Marzo'},
                        {'es':'Abril'},
                        {'es':'Mayo'},
                        {'es':'Junio'},
                        {'es':'Julio'},
                        {'es':'Agosto'},
                        {'es':'Septiembre'},
                        {'es':'Octubre'},
                        {'es':'Noviembre'},
                        {'es':'Diciembre'}
                    ]

def get_current_date(language=''):
    """ 
        Returns the date according to the chosen language, by default English
        Format: 23 April 2023
    """
    
    # Get the current datetime object
    now = datetime.now()
    
    # Format the datetime object to a string with the given format
    date_str = now.strftime('%d %B %Y')
    
    language = language.replace('/', '')
    
    if language != '':
        for month in MONTHS_BY_LANGUAGE:
            if language in month:
                day = now.strftime('%d')
                month = MONTHS_BY_LANGUAGE[int(now.strftime('%-m'))-1][language]
                year = now.strftime('%Y')
                date_str = day +' '+ month +' '+ year
                return date_str
            else:
                return None
    
    # Return the formatted date string
    return date_str