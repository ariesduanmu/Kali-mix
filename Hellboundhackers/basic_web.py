# -*- coding: utf-8 -*-
import requests
from utils import _get, _post, parse_web_page

cookie = dict(PHPSESSID="ulpueaidavnfq6phf8ji1d3kt5", 
              fusion_visited="TRUE", 
              fusion_user="107397.f0f6a1205aae13cceb868822d7a4d5d9", 
              fusion_lastvisit="1542519603")

def challenge_3():
    URL = "https://www.hellboundhackers.org/challenges/basic3/index.php"
    response = requests.get(URL, headers={"user-agent":"bwh3_user_agent"}, cookies=cookie)
    content = response.content
    print(parse_web_page(content))



if __name__ == "__main__":
    challenge_3()
