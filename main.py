import json
import tweepy
from parsers.centerstagetheatre import parser as parserCST

def OAuth( twitterData ):
    try:
        auth = tweepy.OAuthHandler( twitterData['consumer_key'],
                                    twitterData['consumer_secret'] )
        auth.set_access_token(twitterData['access_token'], twitterData['access_token_secret'])
        return auth
    except Exception as e:
        return None

    return None

def main():
    collection = []

    with open( 'sources.json') as sourceFile:

        sourceData = json.load( sourceFile )

        for source in sourceData['sources']:
            print( f"Scraping %s..." % source['name'] )

            if source['parser'] == 'centrestagetheatre':
                collection += parserCST.parseCST( source )

    savePlays( collection )

    # Login to Twitter App
    with open( 'secret/twittercreds.json') as twitterCreds:
        twitterData = json.load( twitterCreds )

        oauth = OAuth( twitterData )
        api = tweepy.API( oauth )

       # api.update_status( 'This is an automated test tweet. #ignoreit')
       
    

def savePlays( collection ):
    with open( 'output/plays.json', 'w')  as output:
        json.dump( { 'plays': collection }, output )

main()
