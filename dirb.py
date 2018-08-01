import threading
from queue import Queue
from textwrap import dedent
import os
import sys
import re

import argparse
import requests
from urllib.parse import urljoin

queue = Queue()

def create_workers(response_codes, number_of_threads):
    for _ in range(number_of_threads):
        t = threading.Thread(target=work, args=(response_codes,))
        t.daemon = True
        t.start()

def work(response_codes):
    while True:
        url = queue.get()
        print_response_code(url, response_codes)
        queue.task_done()

def dir_buster(url, wordlist, file_extensions):
    for word in read_wordlist(wordlist):
        queue.put(urljoin(url, word))
        if not file_extensions is None:
            for ext in file_extensions:
                queue.put(urljoin(url, f"{word}.{ext}"))
    queue.join()



def read_wordlist(wordlist):
    """yields a word from a \n delimited wordlist"""
    with open(wordlist) as f:
        for line in f:
            yield line.rstrip()

def print_response_code(url, response_codes):
    """gets response code from url and print if it matches a condition"""
    code = requests.head(url).status_code
    if response_codes is None or code in response_codes:
        print(f"{url}\t\tWith response code {code}")


def parse_arguments():
    """Arguments parser."""
    parser = argparse.ArgumentParser(usage='%(prog)s [options] <url>',
                                     description='Fun with xor by @Ludisposed @Qin',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=dedent('''Examples:
                                                      python dirbuster.py  -c "200, 301,        401" -w "wordlist.txt" -e "html,php,py" <url>'''))
    parser.add_argument('-c', '--code', type=str, help='Http response codes to filter on')
    parser.add_argument('-w', '--wordlist', type=str, help='Wordlist you want to fuzz with')
    parser.add_argument('-e', '--extension', type=str, help='Filename extensions you want to fuzz')
    parser.add_argument('-t', '--thread', type=int, default=10, help="number of thread")
    parser.add_argument('url', type=str, help='Url you want to fuzz')
    args = parser.parse_args()

    try:
        requests.head(args.url).status_code
    except Exception as e:
        print("[!] Url is not responding")
        sys.exit(1)

    if not args.wordlist is None and not os.path.isfile(args.wordlist):
        print("[!] Wordlist is not valid")
        sys.exit(1)

    if not args.code is None and re.match(r"^(\s*\d{1,3}\s*)(,\s*\d{1,3}\s*)*$", args.code) is None:
        print("[!] Response codes are not valid, logging all response codes")
        args.code = None

    if not args.code is None:
        args.code = list(map(int, re.sub(r"\s+", "", args.code).split(",")))

    if not args.extension is None and re.match(r"^(\s*[a-z]+\s*)(,\s*[a-z]+\s*)*$", args.extension.lower()) is None:
        print("[!] Extensions are not valid, only searching for directories")
        args.extension = None

    if not args.extension is None:
        args.extension = re.sub(r"\s+", "", args.extension).split(",")

    return args.url, args.code, args.wordlist, args.extension, args.thread

if __name__ == '__main__':
    url, response_codes, wordlist, file_extensions, number_of_threads = parse_arguments()
    create_workers(response_codes, number_of_threads)
    dir_buster(url, wordlist, file_extensions)



