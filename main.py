import json
import tweepy
import datetime
import time
import calendar
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

    dbFile = open( 'output/plays.json', 'r')
    db = json.load( dbFile )['plays']

    with open( 'sources.json') as sourceFile:

        sourceData = json.load( sourceFile )

        for source in sourceData['sources']:
            print( f"Scraping %s..." % source['name'] )

            if source['parser'] == 'centrestagetheatre':
                collection += parserCST.parseCST( source )

    # Filter anything in the past
    curDate = datetime.date.today()
    for play in collection:
        filteredList = []
        for playdate in play['dates']:
            
            actualPlayDate = datetime.datetime.strptime(playdate + f' {curDate.year}', "%B %d %Y").date() 
          
            if actualPlayDate.month > curDate.month or (actualPlayDate.month == curDate.month and actualPlayDate.day >= curDate.day):
                filteredList.append( playdate )
            else:
                print( f"Filtered out past show on {playdate}")

        play['dates'] = filteredList

    # Reconcile anything we've already got
    bFound = False
    for play in collection:
        for dbPlay in db:
            if dbPlay['title'] == play['title']:
                bFound = True
    
        if bFound == False:
            db.append( play )

    # If there is anything in the next week -- tweet the first one
    for play in db:
        for playdate in play['dates']:
            actualPlayDate = datetime.datetime.strptime(playdate + f' {curDate.year}', "%B %d %Y").date()
            if actualPlayDate.month == curDate.month and actualPlayDate.day <= curDate.day + 7 and play['posted'] == False:
                postTweet( play, playdate )
                play['posted'] = True
                break
                

    savePlays( db )

       
def postTweet( play, datestr ):
    print( f"Tweeting about {play['title']} on {datestr}")
    
    # Login to Twitter App
    with open( 'secret/twittercreds.json') as twitterCreds:
        twitterData = json.load( twitterCreds )

        oauth = OAuth( twitterData )
        api = tweepy.API( oauth )

        update = f"Coming this week: {play['title']} on {datestr}. For more info check out {play['link']}"
        print( update )
        api.update_status( update )

def savePlays( collection ):
    with open( 'output/plays.json', 'w')  as output:
        json.dump( { 'plays': collection }, output )

main()
