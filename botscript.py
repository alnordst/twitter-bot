import tweepy
import auth

def init():
    keys = tweepy.OAuthHandler(auth.consumer_key, auth.consumer_secret)
    keys.set_access_token(auth.access_token, auth.access_token_secret)
    api = tweepy.API(keys)
    return api
    
def retweet_from_query(api, query, depth = 10):
    for tweet in tweepy.Cursor(api.search, q=query).items(depth):
        try:
            tweet.retweet()
            
        except tweepy.TweepError as e:
            print(e.reason)
            
        except StopIteration:
            break

        
api = init()
retweet_from_query(api, query = "from:mtamaryland 449")
retweet_from_query(api, query = "from:metrorailinfo ballston OR orange OR 'silver line'")
