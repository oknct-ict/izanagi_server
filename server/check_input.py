#!/usr/bin/env python
#coding:utf-8

import myconst

USER    = myconst.USER
PASS    = myconst.PASS
MAIL    = myconst.MAIL
GRADE   = myconst.GRADE
LEN         = 0;
LEN_ALPHA   = 1;

'''
文字列が正しいか（文字列の長さや、英数字のみ）かを判定する
@param string
@param str_len
@param case
@return 正しい：0、不正：エラーコード

'''
def is_correct_str(string, str_len, case):
    # length check
    if len(string) > str_len or len(string) == 0:
        print "len ";
        return myconst.DATA_NON_REGULATED;
    # char code check
    if case == LEN_ALPHA:
        if string.isalnum() is False:
            print string, "alfa num not";
            return myconst.DATA_NON_REGULATED;
    return myconst.OK

def register(data):
    if USER not in data or \
        PASS not in data or \
        MAIL not in data or \
        GRADE not in data:
        print "tarinai";
        return myconst.DATA_DEFICIENCY;
    if is_correct_str(data[USER], 16, LEN_ALPHA) != myconst.OK or \
        is_correct_str(data[PASS], 32, LEN_ALPHA) != myconst.OK or \
        is_correct_str(data[MAIL], 64, LEN) != myconst.OK:
        print "nagasatoka";
        return myconnst.DATA_NON_REGULATED;
    return myconst.OK;

def login(data):
    if USER not in data or PASS not in data:
        return myconst.DATA_DEFICIENCY;
    return myconst.OK;


