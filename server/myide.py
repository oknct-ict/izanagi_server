#!/usr/bin/env python
#coding:utf-8

import myconst
import user_manager
import project_manager
import file_manager
import check_input
from connection_manager import CONNECTION_MANAGER

USER        = myconst.USER 
PASS        = myconst.PASS
MAIL        = myconst.MAIL
GRADE       = myconst.GRADE
RES         = myconst.RES
PRO_ID      = myconst.PRO_ID
PRO_NAME    = myconst.PRO_NAME
PRO_LIST    = myconst.PRO_LIST
FILE_ID     = myconst.FILE_ID
FILE_NAME   = myconst.FILE_NAME
FILE_LIST   = myconst.FILE_LIST
DIR         = myconst.DIR
CODE        = myconst.CODE


'''
app.pyから呼ばれ、コマンドを見て関数を呼ぶ
@param websock
@param session_id
@oaram command      必ずhoge_REQの形式になる
@param data

@return session_id
@return command　   必ずhoge_RESの形式になる
@return data
'''
def receive_ide(websock, session_id, command, data):
    # user register
    if command == myconst.REGISTER_REQ:
        command = myconst.REGISTER_RES;
        session_id, res = receive_ide_register(websock, data);
        data = {RES:res}
    # login
    elif command == myconst.LOGIN_REQ:
        command = myconst.LOGIN_RES;
        session_id, res = receive_ide_login(websock, data);
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
        project_id, res = receive_ide_pro_create(user_id, data);
        data = {PRO_ID:project_id, RES:res};
    # project_list
    elif command == myconst.PRO_LIST_REQ:
        command = myconst.PRO_LIST_RES;
        project_lists, res = receive_ide_pro_list(user_id);
        data = {PRO_LIST:project_lists, RES:res};
    # project_delete
    elif command == myconst.PRO_DELETE_REQ:
        command = myconst.PRO_DELETE_RES;
        res = receive_ide_pro_delete(user_id, data);
        data = {RES:res};
    # project_rename
    elif command == myconst.PRO_RENAME_REQ:
        command = myconst.PRO_RENAME_RES;
        res = receive_ide_pro_rename(user_id, data);
        data = {RES:res};
    # file_save
    elif command == myconst.SAVE_REQ:
        command = myconst.SAVE_RES;
        file_id, res = receive_ide_save(data);
        data = {RES:res, FILE_ID:file_id};
    # renew
    elif command == myconst.RENEW_REQ:
        command = myconst.RENEW_RES;
        res = receive_ide_renew(data);
        data = {RES:res};
    # open
    elif command == myconst.OPEN_REQ:
        command = myconst.OPEN_RES;
        code, res = receive_ide_open(data);
        data = {RES:res, CODE:code};
    # delete
    elif command == myconst.DELETE_REQ:
        command = myconst.DELETE_RES;
        res = receive_ide_delete(data);
        data = {RES:res};
    # list
    elif command == myconst.LIST_REQ:
        command = myconst.LIST_RES;
        file_lists, res = receive_ide_list(user_id, data);
        data = {RES:res, FILE_LIST:file_lists};
    # rename
    elif command == myconst.RENAME_REQ:
        command = myconst.RENAME_RES;
        res = receive_ide_rename(data);
        data = {RES:res};
    # redir
    elif command == myconst.REDIR_REQ:
        command = myconst.REDIR_RES;
        res = receive_ide_redir(data);
        data = {RES:res};

    # response
    print session_id, command, data;
    return (session_id, command, data);

def receive_ide_register(websock, data):
    res = check_input.register(data);
    if res != myconst.OK:
        return ("", res);
    user_id = data[USER];
    password = data[PASS];
    address = data[MAIL];
    grade = data[GRADE];
    # check is user_id unique
    if user_manager.check_unique_user_id(user_id) is False:
        return ("", myconst.USER_EXISTING);
    user_manager.append(user_id, password, address, grade);
    session_id = CONNECTION_MANAGER.append(myconst.IDE, websock, user_id);
    return (session_id, myconst.OK);

def receive_ide_login(websock, data):
    res = check_input.login(data);
    if res != myconst.OK:
        return ("", res);
    user_id = data[USER];
    password = data[PASS];
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

def receive_ide_pro_create(user_id, data):
    res = check_input.pro_create(data);
    if res != myconst.OK:
        return ("", res);
    project_name = data[PRO_NAME];
    # check is project_name unique
    if project_manager.check_unique_project_name(user_id, project_name) is False:
        return ("", myconst.PROJECT_EXISTING);
    # project create
    project_id = project_manager.create(user_id, project_name);
    return (project_id, myconst.OK);
    
def receive_ide_pro_delete(user_id, data):
    res = check_input.pro_delete(data);
    if res != myconst.OK:
        return ("", res);
    project_id = data[PRO_ID];
    # check is project_id
    if project_manager.is_valid_project_id(user_id, project_id) is False:
        return (myconst.PROJECT_NO_EXISTING);
    project_manager.delete(project_id);
    return (myconst.OK);

def receive_ide_pro_rename(user_id, data):
    res = check_input.pro_rename(data);
    if res != myconst.OK:
        return (res);
    project_id = data[PRO_ID];
    project_name = data[PRO_NAME];
    # check is project_id
    if project_manager.is_valid_project_id(user_id, project_id) is False:
        return (myconst.PROJECT_NO_EXISTING);
    if project_manager.check_unique_project_name(user_id, project_name) is False:
        return (myconst.PROJECT_EXISTING);
    project_manager.rename(project_id, project_name);
    return (myconst.OK);

def receive_ide_pro_list(user_id):
    project_list, res = project_manager.get_lists(user_id);   
    return (project_list, res);

def receive_ide_save(data):
    res = check_input.save(data);
    if res != myconst.OK:
        return ("", res);
    file_name = data[FILE_NAME];
    project_id = data[PRO_ID];
    directory = data[DIR];
    code = data[CODE];
    # check is file_name unique
    if file_manager.check_unique_file_name(project_id, file_name) is False:
        return ("", myconst.FILE_EXISTING);
    # file create
    file_id = file_manager.save(file_name, project_id, directory, code);
    return (file_id, myconst.OK);

def receive_ide_renew(data):
    res = check_input.renew(data);
    if res != myconst.OK:
        return (res);
    file_id = data[FILE_ID];
    code = data[CODE];
    # check is file id
    if file_manager.is_valid_file_id(file_id) is False:
        return (myconst.FILE_NO_EXISTING);
    file_manager.renew(file_id, code);
    return (myconst.OK);

def receive_ide_open(data):
    res = check_input._open(data);
    if res != myconst.OK:
        return ("", res);
    file_id = data[FILE_ID];
    # check is file id
    if file_manager.is_valid_file_id(file_id) is False:
        return ("", myconst.FILE_NO_EXISTING);
    code = file_manager._open(file_id);
    return (code, myconst.OK);

def receive_ide_delete(data):
    res = check_input.delete(data);
    if res != myconst.OK:
        return (res);
    file_id = data[FILE_ID];
    # check is file id
    if file_manager.is_valid_file_id(file_id) is False:
        return (myconst.FILE_NO_EXISTING);
    file_manager.delete(file_id);
    return (myconst.OK);

def receive_ide_list(user_id, data):
    res = check_input._list(data);
    if res != myconst.OK:
        return ({}, res);
    project_id = data[PRO_ID];
    if project_manager.is_valid_project_id(user_id, project_id) is False:
        return ({}, myconst.PROJECT_NO_EXISTING);
    file_lists, res = file_manager.get_lists(project_id);
    return (file_lists, res);

def receive_ide_rename(data):
    res = check_input.rename(data);
    if res != myconst.OK:
        return (res);
    file_id = data[FILE_ID];
    file_name = data[FILE_NAME];
    # check is file id
    if file_manager.is_valid_file_id(file_id) is False:
        return (myconst.FILE_NO_EXISTING);
    file_manager.rename(file_id, file_name);
    return (myconst.OK);

def receive_ide_redir(data):
    res = check_input.redir(data);
    if res != myconst.OK:
        return (res);
    file_id = data[FILE_ID];
    directory = data[DIR];
    # check is file id
    if file_manager.is_valid_file_id(file_id) is False:
        return (myconst.FILE_NO_EXISTING);
    file_manager.redir(file_id, directory);
    return (myconst.OK);

