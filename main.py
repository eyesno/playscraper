import json
from parsers.centerstagetheatre import parser as parserCST

sources = [ { 'name': 'CentreStage Theatre',
              'parser': 'centrestagetheatre',
              'nowplaying': 'https://www.centrestagetheatre.ca/index.php/now-playing',
              'comingsoon': 'https://www.centrestagetheatre.ca/coming-soon' }  
]


def main():
    collection = []

    for source in sources:
        print( f"Scraping %s..." % source['name'] )

        if source['parser'] == 'centrestagetheatre':
            collection += parserCST.parseCST( source )

    savePlays( collection )
        

    for play in collection:
        print( play['title'])
       # print( play['dates'][0]['date'])  
       # print( play['subtitle']) 
       # print( play['description']) 
    

def savePlays( collection ):
    with open( 'plays.json', 'w')  as output:
        json.dump( { 'plays': collection }, output )

main()
