# -*- coding: utf-8 -*-
import requests
import re
import base64
from bs4 import BeautifulSoup

session = requests.Session()

cookie = dict(PHPSESSID="ulpueaidavnfq6phf8ji1d3kt5",
              fusion_visited="TRUE",
              fusion_user="107397.967cdfabd2cbdf1d12bdd8a1590ecf1c",
              fusion_lastvisit="1540809182")

def _get(url):
    response = session.get(url, cookies=cookie)
    return response.content

def _post(url, data):
    response = session.post(url, cookies=cookie, data=data)
    return response.content

def parse_web_page(content):
    soup = BeautifulSoup(content, 'html.parser')
    body = soup.find(class_="main-body")
    return str(body)

def challenge_1():
    base_url = "https://www.hellboundhackers.org/challenges/timed/timed1/index.php?b64="
    url = "https://www.hellboundhackers.org/challenges/timed/timed1/index.php"
    content = _get(url)
    body = parse_web_page(content)
    m = re.search(r"(?<=(random\sstring:\s))[\w\=]+", body)
    base_text = m.group(0)
    base_url += base64.b64decode(base_text).decode("utf-8")
    content = _get(base_url)
    print(parse_web_page(content))

def challenge_2():
    url = "https://www.hellboundhackers.org/challenges/timed/timed2/index.php"
    post_url = "https://www.hellboundhackers.org/challenges/timed/timed2/index.php?check"
    content = _get(url)
    body = parse_web_page(content)
    m = re.search(r"(?<=(your\sstring\sis:\s))\w+", body)
    base_text = m.group(0)
    ans = 0
    for s in base_text:
        if "0"<=s<="9":
            ans += int(s)
    data = dict(ans=ans, submit="Check")
    content = _post(post_url, data)
    print(parse_web_page(content))


if __name__ == "__main__":
    challenge_2()
