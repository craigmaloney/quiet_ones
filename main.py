import os
import slack
from datetime import datetime
from collections import Counter
import csv

THRESHOLD = 3


def main():

    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
    users_list = client.users_list()
    users = {}
    channels_list = client.channels_list()

    users = {}
    posts_by_user = Counter()

    for user in users_list['members']:
        if not(user['deleted'] and user['is_bot']):
            email = user['profile'].get('email')
            if email is not None:
                updated = datetime.now() - datetime.fromtimestamp(user['updated'])
                users[user['id']] = {
                        'name': user['profile'].get('real_name'),
                        'email': email,
                        'inactive': updated.days > 30}
                posts_by_user[user['id']] = 0

    for channel in channels_list['channels']:
        if channel['is_archived'] is True:
            continue
        client.conversations_join(channel=channel['id'])

        for history in client.conversations_history(channel=channel['id'], limit=200):
            for message in history['messages']:
                if 'user' in message and message['user'] in users:
                    posts_by_user[message['user']] += 1

    posts_by_user_less_than_threshold = \
        Counter({k: count for k, count in posts_by_user.items() if count <= THRESHOLD})
    with open('quiet_ones.csv', 'w') as csvfile:
        field_names = ['username', 'email', 'count', 'inactive']
        writer = csv.DictWriter(csvfile, fieldnames=field_names, dialect='excel')
        writer.writeheader()
        for user, count in posts_by_user_less_than_threshold.items():
            writer.writerow({
                'username': users[user]['name'],
                'email': users[user]['email'],
                'count': count,
                'inactive': users[user]['inactive']
                })


if __name__ == '__main__':
    main()
