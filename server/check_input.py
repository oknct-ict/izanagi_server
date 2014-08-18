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

'''
ユーザー登録情報が正しいか
@param data             辞書型のJSONデータ
@return user_id     ユーザーID
@return password    パスワード
@return mail        メールアドレス
@return grade       学年
@return res         正しい：0、正しくない：エラーコード
'''
def register(data):
    if USER not in data or \
        PASS not in data or \
        MAIL not in data or \
        GRADE not in data:
        print "tarinai";
        return myconst.DATA_DEFICIENCY;
    user_id = data[USER];
    password = data[PASS];
    mail = data[MAIL];
    grade = data[GRADE];
    if is_correct_str(user_id, 16, LEN_ALPHA) != myconst.OK or \
        is_correct_str(password, 32, LEN_ALPHA) != myconst.OK or \
        is_correct_str(mail, 64, LEN) != myconst.OK:
        print "nagasatoka";
        return myconnst.DATA_NON_REGULATED;
    return myconst.OK;

'''
ログイン情報が正しいか
@param data             辞書型のJSONデータ
@return user_id         ユーザーID
@return password        パスワード
@return res             正しい：0、正しくない：エラーコード
'''
def login(data):
    if USER not in data or PASS not in data:
        return myconst.DATA_DEFICIENCY;
    user_id = data[USER];
    password = data[PASS];
    print "check_login", user_id, password;
    return myconst.OK;





