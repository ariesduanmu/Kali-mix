import requests
session = requests.Session()

"""
A few things I have noticed

################################################################################

You have this line:
$ENV{'TMPDIR'}="WWWDIR/tmp/";

So our file get's uploaded to this location
However things are not that easy...

http://natas31.natas.labs.overthewire.org/tmp/
--->
Forbidden
You don't have permission to access /tmp/ on this server.

Which probably means that those only have have only write permissions from us
The rest is all done internal

################################################################################

Therefore (I think) this attack needs to happen in 2 stages...

1. Upload a (shellcode, or perl script) to the tmp directory
2. Upload another file that runs our malicious upload
--> Let the return be nicely printed in table format

"""

def natas31(url):
    response = session.get(url)
    print(response.text)

if __name__ == '__main__':
    url = 'http://natas31:hay7aecuungiuKaezuathuk9biin0pu1@natas31.natas.labs.overthewire.org/'
    natas31(url)
