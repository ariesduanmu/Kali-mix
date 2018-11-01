# -*- coding: utf-8 -*-
from utils import _get, _post, parse_web_page


def challenge_1():
    post_url = "https://www.hellboundhackers.org/challenges/basic1/22.php"
    data = dict(password="1234")
    print(_post(post_url, data))

if __name__ == "__main__":
    challenge_1()