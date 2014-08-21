#!/usr/bin/env python
#coding:utf-8

import functools

IDE = "ide"
ANDROID = "android"
VALID_TYPES = frozenset([IDE, ANDROID])

def is_valid_type(type_name):
    return type_name in VALID_TYPES

def validater(arg_id):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not is_valid_type(args[arg_id]):
                return;
            return func(*args, **kwargs)
        return wrapper
    return deco

if __name__ == "__main__":
    pass
