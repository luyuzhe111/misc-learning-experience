import twitter
import json

ACCESS_TOKEN = ''
ACCESS_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''


def main():
    print('Loading data from Twitter...')
    t = twitter.Api(consumer_key=CONSUMER_KEY,
                    consumer_secret=CONSUMER_SECRET,
                    access_token_key=ACCESS_TOKEN,
                    access_token_secret=ACCESS_SECRET)

    elonmusk = get_tweets(t, 'elonmusk', 3200)
    elonmusk_json = [tweet.AsDict() for tweet in elonmusk]

    kanyewest = get_tweets(t, 'kanyewest', 3200)
    kanyewest_json = [tweet.AsDict() for tweet in kanyewest]

    # filter out tweets that contain urls, user names, are replies to others
    def filter_data(x):
        no_url = len(x['urls']) == 0 and 'media' not in x.keys()
        no_mention = len(x['user_mentions']) == 0
        no_reply = 'in_reply_to_screen_name' not in x.keys()
        return no_url and no_mention and no_reply

    elonmusk_json_filtered = list(filter(filter_data, elonmusk_json))
    elon_tweets = [x['text'] for x in elonmusk_json_filtered]

    kanye_json_filtered = list(filter(filter_data, kanyewest_json))
    kanye_tweets = [x['text'] for x in kanye_json_filtered]

    print(len(elon_tweets))
    print(len(kanye_tweets))

    with open('tweets_data/elonmusk.json', 'w') as jsonfile:
        json.dump(elon_tweets, jsonfile)

    with open('tweets_data/kanyewest.json', 'w') as jsonfile:
        json.dump(kanye_tweets, jsonfile)


def get_tweets(tapi, username, num_tweets):
    tweets = tapi.GetUserTimeline(screen_name=username, count=200)
    max_id = min([tweet.id for tweet in tweets])

    assert num_tweets <= 3200, 'No more than 3200 tweets can be requested'
    while len(tweets) < num_tweets:
        prev_max_id = max_id
        older_tweets = tapi.GetUserTimeline(screen_name=username, max_id=max_id, count=200)
        max_id = min([tweet.id for tweet in older_tweets])
        # stop if user has fewer than 3200 tweets
        if prev_max_id == max_id:
            return tweets
        tweets.extend(older_tweets)
        print(max_id, len(tweets))

    return tweets[:num_tweets]


if __name__ == '__main__':
    main()
