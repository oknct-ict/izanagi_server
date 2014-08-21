#!/usr/bin/env python
#coding:utf-8

from flask import g
import pymongo
import mycommand

USER = "user_id"
PASS = "password"
MAIL = "address"
GRADE = "grade"

def append(user_id, password, mail, grade):
    pass_sha256 = mycommand.get_sha256(password);
    g.db.users.insert({USER:user_id, PASS:pass_sha256, MAIL:mail, GRADE:grade});
    return;
    
'''
このユーザーIDは唯一かどうか
@param user_id 
@return 存在しない：True、存在する：False
'''
def check_unique_user_id(user_id):
    if g.db.users.find_one({USER:user_id}) is None:
        # uesr_id is unique
        return True;
    # user_id is already register
    return False;
    
'''
DBに入っているユーザーIDとパスワードと一致するかどうか
@param user_id
@param password
@return 一致する：True、一致しない：False
'''
def is_valid_user_id(user_id, password):
    pass_sha256 = mycommand.get_sha256(password);
    if g.db.users.find_one({USER:user_id, PASS:pass_sha256}) is None:
        return False;
    return True;


    
