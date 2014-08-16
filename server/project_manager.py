#!/usr/bin/env python
#coding:utf-8

from flask import g
import pymongo
import mycommand

PRO_ID = "project_id"
PRO_NAME = "project_name"
USER = "user_id"

def create(user_id, project_name):
    project_id = mycommand.get_random_str(16);
    g.db.projects.insert({PRO_ID:project_id, PRO_NAME:project_name, USER:user_id});
    return project_id;

def check_unique_project_name(user_id, project_name):
    if g.db.projects.find_one({PRO_NAME:project_name, USER:user_id}) is None:
        print project_name, "new project";
        # project_name is unique
        return True;
    # project_name is already created
    return False;

def is_valid_project_id(user_id, project_id):
    if g.db.users.find_one({PRO_ID:project_id, USER:user_id}) is None:
        print "project is none";
        return False;
    return True;

def delete(user_id, project_id):
    return;

