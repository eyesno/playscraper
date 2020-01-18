import json
from parsers.centerstagetheatre import parser as parserCST

sources = [ { 'name': 'CentreStage Theatre',
              'parser': 'centrestagetheatre',
              'urls': ['https://www.centrestagetheatre.ca/index.php/now-playing',
                       'https://www.centrestagetheatre.ca/coming-soon']
            }  
]


def main():
    collection = []

    for source in sources:
        print( f"Scraping %s..." % source['name'] )

        if source['parser'] == 'centrestagetheatre':
            collection += parserCST.parseCST( source )

    savePlays( collection )
       
    

def savePlays( collection ):
    with open( 'plays.json', 'w')  as output:
        json.dump( { 'plays': collection }, output )

main()
