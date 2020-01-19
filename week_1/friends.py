"""
Course: "Python Web Services Creation Course", Week 1
Task: display the age distribution of friends for the specified user
"""
import requests
import json
import os

from datetime import datetime
from collections import defaultdict


def get_user_id(access_token, user_uid):
    url_id = f"https://api.vk.com/method/users.get?v=5.71&access_token={access_token}&user_ids={user_uid}"
    req_id = requests.get(url_id)
    data = json.loads(req_id.text)

    if 'error' in data:
        print(data['error']['error_msg'])
        raise SystemExit

    return data['response'][0]['id']


def get_friends(access_token, user_id):
    url_friends = f"https://api.vk.com/method/friends.get?v=5.71&access_token={access_token}" \
                  f"&user_id={user_id}&fields=bdate"
    req_friends = requests.get(url_friends)
    data = json.loads(req_friends.text)

    if 'error' in data:
        print(data['error']['error_msg'])
        raise SystemExit

    return data['response']['items']


def calc_age(uid):
    access_token = os.environ.get('ACCESS_TOKEN')
    user_id = get_user_id(access_token, uid)
    friends = get_friends(access_token, user_id)

    current_year = datetime.now().year
    ages_dict = defaultdict(int)

    for friend in friends:
        if 'bdate' in friend:
            bdate = friend['bdate'].split('.')
            if len(bdate) == 3:
                age = current_year - int(bdate[-1])
                ages_dict[age] += 1

    ages_list = [(age, ages_dict[age]) for age in ages_dict]

    return sorted(sorted(ages_list, key=lambda x: x[0]), key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    res = calc_age('margo_mey')
    print(res)
