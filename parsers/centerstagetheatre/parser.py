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
    dates = [ { 'date': str } ] 
    # TODO: Find a way to make this intelligent
    return dates