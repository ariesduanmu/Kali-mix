import base64
from itertools import cycle
from collections import Counter

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

def repeated_substring(text):
    vals = Counter(_repeated_substring(text))
    return max(vals.items(), key=lambda i: (len(i[0]), i[1]))[0]

BREAK_JSON = b'{"showpassword":"no","bgcolor":"#ffffff"}'
GEN_JSON = b'{"showpassword":"yes","bgcolor":"#ffffff"}'

if __name__ == '__main__':
    cookie = decode_base64(b'ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw')
    password = repeated_substring(xor_repeat(cookie, BREAK_JSON))
    new_cookie = xor_repeat(GEN_JSON, password)
    print(base64.encodestring(new_cookie).rstrip())
