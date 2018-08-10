# -*- coding: utf-8 -*-
#import os
#os.system("python -m pip install fstring")
#os.system("python -m pip install astroid")

from fstring import fstring
import unittest
import re

SECRET_GLOBAL = "this is a secret"

class Error:
    def __init__(self):
        pass

def a_function():
    return SECRET_GLOBAL

def safe_format(dangerous):
    dangerous = re.sub(r"(__[\w]+__)|([\w\d]+\(\))|(\/0)|(\.system\(.*\))|(\.__globals__\[.*\])|(\.+)", "", dangerous)
    if dangerous == "{}":
        return ""
    return fstring(dangerous)

def this_is_eval(dangerous):
    dangerous = re.sub(r"(__[\w]+__)|([\w\d]+\(\))|(\/0)|(\.system\(.*\))|(\.__globals__\[.*\])|(\.+)", "", dangerous)
    if dangerous == "{}":
        return ""
    return eval(dangerous)


class SafeFormatTest(unittest.TestCase):
    def test_global_acces(self):
        self.assertEqual(safe_format("{Error().__init__.__globals__[SECRET_GLOBAL]}"), "")

    def test_function_acces(self):
        self.assertEqual(safe_format("{a_function()}"), "")

    def test_error_string(self):
        self.assertEqual(safe_format("{0/0}"), "0")

    def test_code_excecution(self):
        self.assertEqual(safe_format("{__import__('os').system('dir')}"), "os")

if __name__ == "__main__":
    unittest.main()


