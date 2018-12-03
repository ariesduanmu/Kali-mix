# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

session = requests.Session()

cookie = dict(PHPSESSID="ulpueaidavnfq6phf8ji1d3kt5", 
              fusion_visited="TRUE", 
              fusion_user="107397.f0f6a1205aae13cceb868822d7a4d5d9", 
              fusion_lastvisit="1542519603")

def _get(url):
    response = session.get(url, cookies=cookie)
    return response.content

def _post(url, data=None):
    if data is None:
        response = session.post(url, cookies=cookie)
    else:
        response = session.post(url, cookies=cookie, data=data)
    return response.content

def parse_web_page(content, class_name="main-body"):
    soup = BeautifulSoup(content, 'html.parser')
    body = soup.find(class_=class_name)
    return str(body)
