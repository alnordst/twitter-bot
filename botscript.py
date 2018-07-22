import datetime
import json
import tweepy


def init():
    auths = []
    with open('auth.json') as f:
        auths = json.loads(f.read())

    apis = []
    for auth in auths:
        keys = tweepy.OAuthHandler(auth["consumer_key"], auth["consumer_secret"])
        keys.set_access_token(auth["access_token"], auth["access_token_secret"])
        api = tweepy.API(keys)
        apis.append(api)

    return apis


def get_queries():
    configs = []
    with open('config.json') as f:
        configs = json.loads(f.read())

    # queries are full searches to be performed, there is expected
    # to be one query for each set of authentication keys
    queries = []
    for query_set in configs:
        # a subquery is a set of  search terms centered around a
        # particular source
        subqueries = []
        for item in query_set:
            if item["days"][datetime.date.today().weekday()].isupper():
                source_string = "from:" + item["source"]
                # query_terms are the terms that make up a subquery
                # outside of the source string
                query_terms = []
                for term in item["terms"]:
                    start_time = parse_time(term["start"])
                    end_time = parse_time(term["end"])
                    now = datetime.datetime.now().time()

                    if start_time < now and now < end_time:
                        query_terms.append("(" + term["query"] + ")")

                if query_terms:
                    subquery_string = " OR ".join(query_terms)
                    subquery = "(" + source_string + " " + subquery_string + ")"

                    subqueries.append(subquery)

        queries.append(" OR ".join(subqueries))

    return queries


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


apis = init()
queries = get_queries()
last_update_time = read_and_update_timestamp()
print("last update: " + str(last_update_time))

for index, api in enumerate(apis):
    try:
        retweet_from_query(api, queries[index], last_update_time)
    except OUTOFINDEXEXCEPTION:
        print("api " + index + " has no queries")
