import json
import requests
import key as k

# An api key is emailed to you when you sign up to a plan
# Get a free API key at https://api.the-odds-api.com/

API_KEY = k.getApiKey() #replace k.getApiKey() with your personal API key gathered from the website above

SPORT = 'upcoming' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

REGION = 'us' # uk | us | eu | au

MARKET = 'h2h' # h2h | spreads | totals

ODDS = 'american' # decimal  | american


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# First get a list of in-season sports
#   the sport 'key' from the response can be used to get odds in the next request
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

sports_response = requests.get('https://api.the-odds-api.com/v3/sports', params={
    'api_key': API_KEY
})

sports_json = json.loads(sports_response.text)

if not sports_json['success']:
    print(sports_json['msg'])

else:
    #listofSports='List of in season sports:' + sports_json['data']
    print('List of in season sports:', sports_json['data'])
    with open('output.json','w') as outfile:
        json.dump('List of in season sports:',outfile, indent=4, sort_keys=True)
        json.dump(sports_json['data'],outfile, indent=4, sort_keys=True)
        outfile.close()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# Now get a list of live & upcoming games for the sport you want, along with odds for different bookmakers
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
    'api_key': API_KEY,
    'sport': SPORT,
    'region': REGION,
    'mkt': MARKET,
    'oddsFormat' : ODDS,
})

odds_json = json.loads(odds_response.text)

if not odds_json['success']:
    print(odds_json['msg'])

else:
    NUMEvents = 'Number of events: ' + str(len(odds_json['data']))
    RequestsRem = 'Remaining requests ' + str(odds_response.headers['x-requests-remaining'])
                                                        
    with open('output.json','a') as outfile:
        json.dump('%%%%%%%%%%%%%%%   ODDS BEGIN   %%%%%%%%%%%%%%%%%%%%%%', outfile, indent=4, sort_keys=True)
        json.dump(NUMEvents, outfile, indent=4, sort_keys=True)
        json.dump(odds_json['data'],outfile, indent=4, sort_keys=True)
        json.dump(RequestsRem, outfile, indent=4, sort_keys=True)
        outfile.close()
        
    print('Number of events:', len(odds_json['data']))
    print(odds_json['data'])

    # Check your usage
    print('Remaining requests ', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])