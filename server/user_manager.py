#!/usr/bin/env python
#coding:utf-8

from flask import g
import pymongo
import mycommand

USER = "user_id"
PASS = "password"
MAIL = "address"

def append(user_id, password, mail):
    pass_sha256 = mycommand.get_sha256(password);
    g.db.users.insert({USER:user_id, PASS:pass_sha256, MAIL:mail});
    return;
    
def check_db(user_id, password):
    pass_sha256 = mycommand.get_sha256(password);
    print user_id, pass_sha256;
    if g.db.users.find_one({USER:user_id, PASS:pass_sha256}) is None:
        print "no_user"
        return False;
    print "yse"
    return True;


    
