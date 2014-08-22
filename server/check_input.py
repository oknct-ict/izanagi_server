#!/usr/bin/env python
#coding:utf-8

import myconst

USER    = myconst.USER
PASS    = myconst.PASS
MAIL    = myconst.MAIL
GRADE   = myconst.GRADE
RES     = myconst.RES
PRO_ID  = myconst.PRO_ID
PRO_NAME= myconst.PRO_NAME
FILE_ID     = myconst.FILE_ID
FILE_NAME   = myconst.FILE_NAME
DIR         = myconst.DIR
CODE        = myconst.CODE
DEVICE_DATA = myconst.DEVICE_DATA
DEVICE_ID   = myconst.DEVICE_ID
LOG         = myconst.LOG
EXE_RES     = myconst.EXE_RES
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
        print "len error!";
        return myconst.DATA_NON_REGULATED;
    # char code check
    if case == LEN_ALPHA:
        if string.isalnum() == False:
            print string, "alfa num not error!";
            return myconst.DATA_NON_REGULATED;
    return myconst.OK

def input_json(data):
    if "session_id" not in data or \
        "request_id" not in data or \
        "command" not in data or \
        "data" not in data or \
        "type" not in data:
        print "json _ error";
        return myconst.DATA_DEFICIENCY;
    return myconst.OK;
    
def register(data):
    if USER not in data or \
        PASS not in data or \
        MAIL not in data or \
        GRADE not in data:
        return myconst.DATA_DEFICIENCY;
    if is_correct_str(data[USER], 16, LEN_ALPHA) != myconst.OK or \
        is_correct_str(data[PASS], 32, LEN_ALPHA) != myconst.OK or \
        is_correct_str(data[MAIL], 64, LEN) != myconst.OK:
        return myconst.DATA_NON_REGULATED;
    return myconst.OK;

def login(data):
    if USER not in data or PASS not in data:
        return myconst.DATA_DEFICIENCY;
    return myconst.OK;

def login_android(data):
    if login(data) != myconst.OK or \
        DEVICE_DATA not in data or \
        DEVICE_ID not in data[DEVICE_DATA]:
        return myconst.DATA_DEFICIENCY;
    return myconst.OK

def pro_create(data):
    if PRO_NAME not in data:
        return myconst.DATA_DEFICIENCY;
    if is_correct_str(data[PRO_NAME], 64, LEN_ALPHA) != myconst.OK:
        return myconst.DATA_NON_REGULATED;
    return myconst.OK;

def pro_delete(data):
    if PRO_ID not in data:
        return myconst.DATA_DEFICIENCY;
    return myconst.OK;

def pro_rename(data):
    if PRO_ID not in data or PRO_NAME not in data:
        return myconst.DATA_DEFICIENCY;
    return myconst.OK

def save(data):
    if FILE_NAME not in data or \
        PRO_ID not in data or \
        DIR not in data or \
        CODE not in data:
        return myconst.DATA_DEFICIENCY;
    if is_correct_str(data[FILE_NAME], 64, LEN_ALPHA) != myconst.OK or \
        is_correct_str(data[DIR], 64, LEN) != myconst.OK or \
        is_correct_str(data[PRO_ID], 16, LEN_ALPHA) != myconst.OK:
        return myconst.DATA_NON_REGULATED;
    return myconst.OK;

def renew(data):
    if FILE_ID not in data or CODE not in data:
        return myconst.DATA_DEFICIENCY;
    return myconst.OK;

def _open(data):
    if FILE_ID not in data:
        return myconst.DATA_DEFICIENCY;
    return myconst.OK;

def delete(data):
    if FILE_ID not in data:
        return myconst.DATA_DEFICIENCY;
    return myconst.OK;

def _list(data):
    if PRO_ID not in data:
        return myconst.DATA_DEFICIENCY;
    return myconst.OK;

def rename(data):
    if FILE_ID not in data or FILE_NAME not in data:
        return myconst.DATA_DEFICIENCY;
    if is_correct_str(data[FILE_NAME], 64, LEN_ALPHA) != myconst.OK:
        return myconst.DATA_NON_REGULATED;
    return myconst.OK;

def redir(data):
    if FILE_ID not in data or DIR not in data:
        return myconst.DATA_DEFICIENCY;
    if is_correct_str(data[DIR], 64, LEN) != myconst.OK:
        return myconst.DATA_NON_REGULATED;
    return myconst.OK;

def info(data):
    if FILE_ID not in data:
        return myconst.DATA_DEFICIENCY;
    return myconst.OK;

def run_request(data):
    if CODE not in data or DEVICE_ID not in data:
        return myconst.DATA_DEFICIENCY;
    return myconst.OK

def run_start(data):
    if RES not in data or DEVICE_ID not in data:
        return myconst.DATA_DEFICIENCY;
    return myconst.OK;

def log_android(data):
    if LOG not in data or DEVICE_ID not in data:
        return myconst.DATA_DEFICIENCY;
    return myconst.OK;

def run_end(data):
    if EXE_RES not in data or DEVICE_ID not in data:
        return myconst.DATA_DEFICIENCY
    return myconst.OK;

