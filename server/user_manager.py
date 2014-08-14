#!/usr/bin/env python
#coding:utf-8

from flask import g
import pymongo

USER = "user_id"
PASS = "password"
MAIL = "address"

def append(user_id, password, mail):
    g.db.users.insert({USER:user_id, PASS:password, MAIL:mail});
    return;
    
def check_db(user_id, password):
    print user_id, password;
    if g.db.users.find_one({USER:user_id, PASS:password}) is None:
        return False;
    return True;


    
