import time
from bs4 import BeautifulSoup
import requests

def parseCST( source ):
    plays = [] 

    for url in source['urls']:
        html = requests.get( url ).text
        soup = BeautifulSoup(html, 'lxml' )
        plays += parseCSTPosts( source, soup, url )
   
    return plays


def parseCSTPosts( source, soup, url ):
    plays = []
    blogposts = soup.findAll("div", {"itemprop": "blogPost"})

    for post in blogposts:
        title = post.findAll("h2", {"itemprop": "name"})[0].text.strip()
        dates = getDates( post.findAll( "p" )[0].text.strip() )
        subtitle = post.findAll( "p" )[1].text.strip()
        description = post.findAll( "p" )[2].text.strip()

        play = {
            'theatre': source['name'],
            'title': title,
            'dates': dates,
            'subtitle': subtitle,
            'description': description,
            'link': url,
            'lastupdate': time.time()
        }

        plays.append( play )

    return plays

def getDates( str ):
    dates = [] 

    tokens = str.split()
    currentMonth = ''

    for token in tokens:
        token = token.strip( ' ,')
        #print( f'Looking at {token}')
        
        if token.lower()[0:3] == 'jan':
            currentMonth = 'January'
        elif token.lower()[0:3] == 'feb':
            currentMonth = 'February'
        elif token.lower()[0:3] == 'mar':
            currentMonth = 'March'
        elif token.lower()[0:3] == 'apr':
            currentMonth = 'April'
        elif token.lower()[0:3] == 'may':
            currentMonth = 'May'
        elif token.lower()[0:3] == 'jun':
            currentMonth = 'June'
        elif token.lower()[0:3] == 'jul':
            currentMonth = 'July'
        elif token.lower()[0:3] == 'aug':
            currentMonth = 'July'
        elif token.lower()[0:3] == 'sep':
            currentMonth = 'September'
        elif token.lower()[0:3] == 'oct':
            currentMonth = 'October'
        elif token.lower()[0:3] == 'nov':
            currentMonth = 'November'
        elif token.lower()[0:3] == 'dec'   :
            currentMonth = 'December'
        else:
            if token.isnumeric() and currentMonth != '':
                dates.append( f'{currentMonth} {token}')
                #print( f"There is a show on {currentMonth} {token}")
        
    # TODO: Find a way to make this intelligent
    return dates