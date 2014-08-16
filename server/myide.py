#!/usr/bin/env python
#coding:utf-8

import mycommand
import myconst
import user_manager
import project_manager
from connection_manager import CONNECTION_MANAGER

USER = "user_id"
PASS = "password"
MAIL = "address"
GRADE = "grade"
RES = "result"
PRO_ID = "project_id"
PRO_NAME = "project_name"
PRO_LIST = "project_list"

def receive_ide(websock, session_id, command, data):
    # user register
    if command == myconst.REGISTER_REQ:
        command = myconst.REGISTER_RES;
        session_id, res = receive_ide_register(websock, data[USER], data[PASS], data[MAIL], data[GRADE]);
        data = {RES:res}
    # login
    elif command == myconst.LOGIN_REQ:
        command = myconst.LOGIN_RES;
        session_id, res = receive_ide_login(websock, data[USER], data[PASS]);
        data = {RES:res}
    # session_id whether correct websock?
    else:
        if CONNECTION_MANAGER.is_valid_websocket(myconst.IDE, session_id, websock) is False:
            # not correct 
            return (None, None, None);   
    # get user_id from session_id
    user_id = CONNECTION_MANAGER.get_user_id(myconst.IDE, session_id);
    
    # project_create
    if command == myconst.PRO_CREATE_REQ:
        command = myconst.PRO_CREATE_RES;
        project_id, res = receive_ide_pro_create(user_id, data[PRO_NAME]);
        data = {PRO_ID:project_id, RES:res};
    # project_list
    elif command == myconst.PRO_LIST_REQ:
        command = myconst.PRO_LIST_RES;
        project_lists, res = receive_ide_pro_list(user_id);
        data = {PRO_LIST:project_lists, RES:res};
    # file_save
    elif command == myconst.SAVE_REQ:
        receive_ide_save();
    # renew
    elif command == myconst.RENEW_REQ:
        receive_ide_renew();
    # open
    elif command == myconst.OPEN_REQ:
        receive_ide_open();
    # delete
    elif command == myconst.DELETE_REQ:
        receive_ide_delete();
    # response
    print session_id, command, data;
    return (session_id, command, data);

def receive_ide_register(websock, user_id, password, address, grade):
    # check is user_id unique
    if user_manager.check_unique_user_id(user_id) is False:
        return ("", myconst.USER_EXISTING);
    user_manager.append(user_id, password, address, grade);
    session_id = CONNECTION_MANAGER.append(myconst.IDE, websock, user_id);
    return (session_id, myconst.OK);

def receive_ide_login(websock, user_id, password):
    # userdata check
    if user_manager.is_valid_user_id(user_id, password) is False:
        # no user data 
        return ("", myconst.USER_DATA_FAULT);
    # access_point num check
    if CONNECTION_MANAGER.possible_append(myconst.IDE, user_id) is False:
        # access_point is over 
        return ("", myconst.ACCESS_POINT_OVER);
    # connection 
    session_id = CONNECTION_MANAGER.append(myconst.IDE, websock, user_id);
    return (session_id, myconst.OK);

def receive_ide_pro_create(user_id, project_name):
    # check is project_name unique
    if project_manager.check_unique_project_name(user_id, project_name) is False:
        return ("", myconst.PROJECT_EXISTING);
    # project create
    project_id = project_manager.create(user_id, project_name);
    return (project_id, myconst.OK);
    
def receive_ide_pro_list(user_id):
    project_list, res = project_manager.get_lists(user_id);   
    return (project_list, res);

def receive_ide_save():
    return;

def receive_ide_renew():
    return;

def receive_ide_open():
    return;

def receive_ide_view_list():
    return;
