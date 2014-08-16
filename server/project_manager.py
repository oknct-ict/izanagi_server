#!/usr/bin/env python
#coding:utf-8

from flask import g
import pymongo
import mycommand
import myconst

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

def is_valid_project_id(project_id):
    if g.db.projects.find_one({PRO_ID:project_id}) is None:
        print "project is none";
        return False;
    return True;

def delete(project_id):
    g.db.projects.remove({PRO_ID:project_id});
    return;

def rename(project_id, project_name):
    g.db.projects.update({PRO_ID:project_id}, {"$set":{PRO_NAME:project_name}});
    return;

def get_lists(user_id):
    lists = g.db.projects.find({USER:user_id});
    project_list = {};
    if lists is not None:
        for value in lists:
            project_list.update({value["project_id"]:value["project_name"]});
    print project_list.values();
    return (project_list, myconst.OK);

