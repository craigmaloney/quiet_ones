import os
import slack
from datetime import datetime
from collections import Counter

THRESHOLD = 3


def main():

    oldest = 0  # seconds since the Epoch
    latest = int((datetime.now() - datetime(1970, 1, 1)).total_seconds())
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
    users_list = client.users_list()
    users = {}
    channels_list = client.channels_list()

    users = {}
    posts_by_user = Counter()

    for user in users_list['members']:
        if not(user['deleted'] and user['is_bot']):
            users[user['id']] = "{name} ({email})".format(
                    name=user['profile'].get('real_name'),
                    email=user['profile'].get('email'))
            posts_by_user[users[user['id']]] = 0

    for channel in channels_list['channels']:
        if channel['is_archived'] is True:
            continue
        client.conversations_join(channel=channel['id'])
        history = client.conversations_history(channel=channel['id'], oldest=oldest, latest=latest)

        for message in history['messages']:
            if 'user' in message:
                posts_by_user[users[message['user']]] += 1

    posts_by_user_less_than_threshold = \
        Counter({k: count for k, count in posts_by_user.items() if count <= THRESHOLD})
    for user, count in posts_by_user_less_than_threshold.items():
        print(user, 'posted', count, 'messages')


if __name__ == '__main__':
    main()
