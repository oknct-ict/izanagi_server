#!/usr/bin/env python
#coding:utf-8

from flask import g
import pymongo
import myconst
import mycommand

PRO_ID      = myconst.PRO_ID
FILE_ID     = myconst.FILE_ID
FILE_NAME   = myconst.FILE_NAME
FILE_LIST   = myconst.FILE_LIST
DIR         = myconst.DIR
CODE        = myconst.CODE

def save(file_name, project_id, directory, code):
    file_id = mycommand.get_random_str(16);
    g.db.files.insert({FILE_ID:file_id, FILE_NAME:file_name, PRO_ID:project_id, DIR:directory, CODE:code});
    return file_id;

def renew(file_id, code):
    g.db.files.update({FILE_ID:file_id}, {"$set":{CODE:code}});
    return;

def _open(file_id):
    data = g.db.files.find_one({FILE_ID:file_id});
    return data[CODE];

def delete(file_id):
    g.db.files.remove({FILE_ID:file_id});
    return;

def get_lists(project_id):
    lists = g.db.files.find({PRO_ID:project_id});
    file_list = [];
    if lists is not None:
        for value in lists:
            data = {FILE_ID:value[FILE_ID], FILE_NAME:value[FILE_NAME], DIR:value[DIR]};
            file_list.append(data);
    return (file_list, myconst.OK);

def rename(file_id, file_name):
    g.db.files.update({FILE_ID:file_id}, {"$set":{FILE_NAME:file_name}});
    return;

def redir(file_id, directory):
    g.db.files.update({FILE_ID:file_id}, {"$set":{DIR:directory}});
    return;

def info(file_id):
    data = g.db.files.find_one({FILE_ID:file_id});
    return (data[FILE_NAME], data[DIR], data[PRO_ID]);

def check_unique_file_name(project_id, file_name):
    print project_id, file_name;
    if g.db.files.find_one({PRO_ID:project_id, FILE_NAME:file_name}) is None:
        print file_name, "new file_name";
        return True;
    return False;

def is_valid_file_id(file_id):
    if g.db.files.find_one({FILE_ID:file_id}) is None:
        print "fils is none";
        return False;
    return True
