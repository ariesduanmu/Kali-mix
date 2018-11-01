# -*- coding: utf-8 -*-
import re
import base64
import wget
import hashlib
import numpy as np
from pyzbar import pyzbar
from io import BytesIO
from fractions import gcd
from bs4 import BeautifulSoup
from numpy.linalg import solve

from utils import _get, _post, parse_web_page


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

def challenge_3():
    url = "https://www.hellboundhackers.org/challenges/timed/timed3/index.php"
    post_url = "https://www.hellboundhackers.org/challenges/timed/timed3/index.php?check"
    wordlist_url = "https://www.hellboundhackers.org/challenges/timed/timed3/data.txt"
    filename = wget.download(wordlist_url)
    with open(filename, "rb") as f:
        wordlist = f.read().split(b",")

    content = _get(url)
    body = parse_web_page(content)
    m = re.search(r"(?<=(your\sstring\sis:\s))\w+", body)
    md5 = m.group(0)
    for w in wordlist:
        if hashlib.md5(w).hexdigest() == md5:
            data = dict(ans=w.decode("utf-8"), submit="Check")
            content = _post(post_url, data)
            print(parse_web_page(content))
            return
    print("No Match")

def challenge_4():
    url = "https://www.hellboundhackers.org/challenges/timed/timed4/index.php"
    post_url = "https://www.hellboundhackers.org/challenges/timed/timed4/index.php?check"
    def rule(s):
        r = s[0] + s[-1]
        for i in range(2,len(s)):
            if i % 2 == 0:
                r += s[i]
            else:
                r += s[i-2]
        return r
    content = _get(url)
    body = parse_web_page(content)
    m = re.search(r"(?<=(Your\sword\sis:\s<strong>))\w+", body)
    s = m.group(0)
    data = dict(ans=rule(s), submit="Check")
    content = _post(post_url, data)
    print(parse_web_page(content))

def challenge_5():
    url = "https://www.hellboundhackers.org/challenges/timed/timed5/index.php"
    post_url = "https://www.hellboundhackers.org/challenges/timed/timed5/index.php?password="
    content = _get(url)
    body = parse_web_page(content)
    m1 = re.search(r"(?<=(Your\sgoal\sis\sto\smake\s))\w+", body)
    m2 = re.search(r"(?<=(into\s))\w+", body)
    first_num = int(m1.group(0))
    second_num = int(m2.group(0))
    answer = "minus_" if first_num > second_num else "plus_"
    answer += str(abs(first_num-second_num))
    content = _get(post_url+answer)
    print(parse_web_page(content))

def challenge_6():
    '''Unreachable for me, as I Can't get response from google haha
    '''
    pass

def challenge_7():
    url = "https://www.hellboundhackers.org/challenges/timed/timed7/barcode.php"
    content = _get(url)
    barcodes = pyzbar.decode(Image.open(BytesIO(content)))
    if len(barcodes) > 0:
        barcode = barcodes[0]
        data = barcode.data.decode('utf-8')
    

def challenge_8():
    url = "https://www.hellboundhackers.org/challenges/timed/timed8/index.php"
    content = _get(url)
    body = parse_web_page(content)
    m = re.search(r"(?<=(where\sans\s=\sa<br/><br/>))[a0-9\+\-x\/\=]+", body)
    equation = m.group(0)
    print(f"[*] {equation}")
    left, right = equation.split("=")
    left1, left2 = left.split("+")
    left2_1, left2_2 = left2.split("x")
    ans = int(right) - (int(left2_1)*int(left2_2))
    print(f"[*]{ans}")
    content = _post(url, {"ans":ans})
    print(parse_web_page(content))

def challenge_9():
    url = "https://www.hellboundhackers.org/challenges/timed/timed9/index.php"
    content = _get(url)
    body = parse_web_page(content)
    m1 = re.search(r"(?<=(the\sfirst\s))[0-9]+", body)
    m2 = re.search(r"(?<=(beginning\swith\s))[0-9]+", body)
    m3 = re.search(r"(?<=(and\s))[0-9]+", body)

    int_1, int_2, int_3 = int(m1.group(0)), int(m2.group(0)), int(m3.group(0))

    def fib(i, j, l):
        s = i+j
        for _ in range(l-2):
            k = i+j
            i = j
            j = k
            s += k
        return s

    ans = fib(int_2, int_3, int_1)
    content = _post(url, dict(answer=ans, submit="Answer!"))
    print(parse_web_page(content))

def challenge_10():
    url = "https://www.hellboundhackers.org/challenges/timed/timed10/index.php"
    content = _get(url)
    body = parse_web_page(content)
    m = re.search(r"(?<=(following\sintegers:\s))[0-9\s]+", body)
    numbers = list(map(int, m.group(0).split(" ")))
    g = gcd(numbers[0], numbers[1])
    for n in numbers[2:]:
        g = gcd(g, n)
    content = _post(url, dict(answer=g, submit="Answer!"))
    print(parse_web_page(content))

def challenge_11():
    url = "https://www.hellboundhackers.org/challenges/timed/timed11/index.php"
    content = _get(url)
    soup = BeautifulSoup(content, 'html.parser')
    body = soup.find(class_="main-body")
    table = body.table
    rows = table.find_all('tr')
    X = []
    y = []
    for row in rows[1:]:
        cols = row.find_all('td')
        i, j = [float(col.center.contents[0]) for col in cols]
        X += [[i**k for k in range(6,-1,-1)]]
        y += [j]
    X = np.array(X)
    y = np.array(y)
    s = solve(X, y)
    print(s)
    m = re.search(r"(?<=(f\())[0-9\.]+", str(body))
    k = float(m.group(0))
    ans = np.dot(np.array([k**i for i in range(6,-1,-1)]), s.T)
    print(ans)
    content = _post(url, dict(answer=ans, submit="Answer!"))
    print(parse_web_page(content))




if __name__ == "__main__":
    challenge_11()
