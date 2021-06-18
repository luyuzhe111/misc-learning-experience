import json
import random


def main():
    with open('tweets_data/elonmusk.json') as f:
        elon_tweets = json.load(f)

    with open('tweets_data/kanyewest.json') as f:
        kanye_tweets = json.load(f)

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


if __name__ == '__main__':
    main()
