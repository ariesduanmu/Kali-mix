import requests
import re
from urllib.parse import quote, unquote

session = requests.Session()

def natas29(url):
    response = session.get(f"{url}index.pl?")
    print(response.text)       

if __name__ == '__main__':
    url = 'http://natas29:airooCaiseiyee8he8xongien9euhe8b@natas29.natas.labs.overthewire.org/'
    print(natas29(url))
