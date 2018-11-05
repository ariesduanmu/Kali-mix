# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

session = requests.Session()

cookie = dict(fusion_visited="TRUE",
              PHPSESSID="al11d6nl2iheuqtbu6atofnjr3", 
              fusion_user="107397.885fbb1d0ea886d93a5560ea41db98eb", 
              fusion_lastvisit="1541032580")

def _get(url):
    response = session.get(url, cookies=cookie)
    return response.content

def _post(url, data=None):
    if data is None:
        response = session.post(url, cookies=cookie)
    else:
        response = session.post(url, cookies=cookie, data=data)
    return response.content

def parse_web_page(content):
    soup = BeautifulSoup(content, 'html.parser')
    body = soup.find(class_="main-body")
    return str(body)
