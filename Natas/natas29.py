import requests
from urllib.parse import quote, unquote

session = requests.Session()

def natas29(url, file):
    r = session.get(f"{url}index.pl?file=", params={"file" : file})
    return r.text

def natas29(url):
    # I think there might be a way...
    # Make a perl shell file
    # Try to overwrite a file as our shell file
    # Next call our file and voila?
    # 
    # 
    # I will stop trying stupid shit hahah
    pass

def scrape_page(url):
    for i in range(1, 6):
        filename = quote(f"perl underground {i}") if i!= 1 else quote("perl underground")
        response = requests.get(f"{url}index.pl?file={filename}")

        with open(unquote(f"{filename}.txt"), 'w') as _file:
            for line in response.text:
                try:
                    _file.write(line)
                except UnicodeEncodeError:
                    print("Line failed in {}.txt".format(unquote(filename)))
                    

if __name__ == '__main__':
    url = 'http://natas29:airooCaiseiyee8he8xongien9euhe8b@natas29.natas.labs.overthewire.org/'
    scrape_page(url)
    print(natas29(url))
