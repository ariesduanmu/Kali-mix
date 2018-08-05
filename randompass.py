# -*- coding: utf-8 -*-
#!/bin/usr/env python3.6

import sys
import argparse
from textwrap import dedent
from random import choice
from string import ascii_lowercase, ascii_uppercase, digits

def random_password(case, length):
    options = [ascii_lowercase, ascii_uppercase, digits, "!@#$%"]
    case = "{:04b}".format(case)
    letters = "".join(options[i] for i in range(4) if case[i] == "1")
    print(f'[+] Password: {"".join([choice(letters) for _ in range(length)])}')

def parse_arguments():
    """Arguments parser."""
    parser = argparse.ArgumentParser(usage='%(prog)s  [opt]',
                                     description='create random password',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=dedent('''
                                                      Model 01: !@#$%
                                                      Model 02: 0-9
                                                      Model 03: 0-9 + !@#$%
                                                      Model 04: A-Z
                                                      Model 05: A-Z + !@#$%
                                                      Model 06: A-Z + 0-9
                                                      Model 07: A-Z + 0-9 + !@#$%
                                                      Model 08: a-z 
                                                      Model 09: a-z + !@#$%
                                                      Model 10: a-z + 0-9
                                                      Model 11: a-z + 0-9 + !@#$%
                                                      Model 12: a-z + A-Z
                                                      Model 13: a-z + A-Z + !@#$%
                                                      Model 14: a-z + A-Z + 0-9
                                                      Model 15: a-z + A-Z + 0-9 + !@#$%"

                                                      Examples:
                                                      python randompass.py  -m 1 -l 10 '''))
    parser.add_argument('-m', '--model', type=int, default=15, help='Model between 1 and 15, default 15')
    parser.add_argument('-l', '--length', type=int, default=8, help='password length, default 8')
    args = parser.parse_args()

    if args.model is not None and (args.model <= 0 or args.model > 15):
        print("[!] Please chose model between 1 and 15")
        sys.exit(1)

    return args.model, args.length

if __name__ == '__main__':
    model, length = parse_arguments()
    random_password(model, length)

