import random
import twitter


ACCESS_TOKEN = ''
ACCESS_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''


def main():
    elon_tweets, kanye_tweets = load_data()
    game_driver(elon_tweets, kanye_tweets)


def load_data():
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

    print(len(elon_tweets), len(elon_tweets))

    return elon_tweets, kanye_tweets


def game_driver(elon_tweets, kanye_tweets):
    '''
    Interacts with the user
    :param elon_tweets:
    :param kanye_tweets:
    '''
    all_data = elon_tweets + kanye_tweets

    user_response = 'y'

    correct_guess = 0
    total_guess = 0
    while user_response == 'y':
        print()
        print('Who tweeted this, Elon or Kanye [E/K]?')
        print()
        prompt = random.choice(all_data)
        print(prompt)
        print()
        user_answer = input('Your answer is: ')

        while len(user_answer) == 0:
            user_answer = input('Please enter something! Your answer is: ')

        correct = False
        if prompt in elon_tweets:
            correct = user_answer[0].lower() == 'e'

        if prompt in kanye_tweets:
            correct = user_answer[0].lower() == 'k'

        if correct:
            correct_guess += 1
            print('Answer correct!')
        else:
            print('Answer wrong!')

        total_guess += 1

        print()
        continue_or_not = input('Do you want to keep playing? [Y/n]: ')
        user_response = continue_or_not[0] if len(continue_or_not) > 0 else 'n'

    print()
    print('Correct: ', correct_guess, 'out of', total_guess)


def get_tweets(tapi, username, num_tweets):
    '''
    Twitter has put a 200 limit on the number of tweets retrieved every time. This function
    is used to iteratively request data.
    :param tapi:
    :param username:
    :param num_tweets:
    :return: num_tweets by username
    '''

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

    return tweets[:num_tweets]


if __name__ == '__main__':
    main()
