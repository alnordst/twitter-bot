import auth
import datetime
import json
import tweepy


def init():
    keys = tweepy.OAuthHandler(auth.consumer_key, auth.consumer_secret)
    keys.set_access_token(auth.access_token, auth.access_token_secret)
    api = tweepy.API(keys)
    return api


def get_query():
    instructions = []
    with open('config.json') as f:
        instructions = json.loads(f.read())
        
    queries = []
    for item in instructions:
        if item["days"][datetime.date.today().weekday()].isupper():
            source_string = "from:" + item["source"]
            subqueries = []
            for term in item["terms"]:
                start_time = parse_time(term["start"])
                end_time = parse_time(term["end"])
                now = datetime.datetime.now().time()
                
                if start_time < now and now < end_time:
                    subqueries.append("(" + term["query"] + ")")
            
            if subqueries:
                subquery_string = " OR ".join(subqueries)
                query = "(" + source_string + " " + subquery_string + ")"
                
                queries.append(query)
    
    return " OR ".join(queries)
    
    
def parse_time(time_string):
    hour, minute = time_string.split(':')
    time = datetime.time(hour=int(hour), minute=int(minute))
    return time
    
    
def read_and_update_timestamp():
    last_update = None
    
    try:
        with open("last_update.timestamp") as f:
            last_update = parse_datetime(f.read())
    except (OSError, TypeError, ValueError) as e:
        print("Couldn't read timestamp from file.")
        last_update = datetime.datetime.combine(datetime.date.today(), datetime.time())
        
    with open("last_update.timestamp", "w") as f:
        now = datetime.datetime.now().replace(microsecond=0)
        f.write(now.isoformat(sep=' '))
        
    return last_update
    

def parse_datetime(datetime_string):
    date, time = datetime_string.split(' ')
    year, month, day = date.split('-')
    hour, minute, second = time.split(':')
    return datetime.datetime(int(year), int(month), int(day),
                             int(hour), int(minute), int(second))


def retweet_from_query(api, query, last_update_time):
    if(query):
        for tweet in tweepy.Cursor(api.search, q=query, result_type='recent').items(20):
            try:
                if last_update_time < tweet.created_at and not tweet.retweeted:
                    tweet.retweet()
                
            except tweepy.TweepError as e:
                print(e.reason)
                
            except StopIteration:
                break

        
api = init()

query = get_query()
print("query: " + query)

last_update_time = read_and_update_timestamp()
print("last update: " + str(last_update_time))

retweet_from_query(api, query, last_update_time)