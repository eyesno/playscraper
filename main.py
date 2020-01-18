import json
from parsers.centerstagetheatre import parser as parserCST

def main():
    collection = []

    with open( 'sources.json') as sourceFile:

        sourceData = json.load( sourceFile )

        for source in sourceData['sources']:
            print( f"Scraping %s..." % source['name'] )

            if source['parser'] == 'centrestagetheatre':
                collection += parserCST.parseCST( source )

    savePlays( collection )
       
    

def savePlays( collection ):
    with open( 'output/plays.json', 'w')  as output:
        json.dump( { 'plays': collection }, output )

main()
