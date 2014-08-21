#!/usr/bin/env python
#coding:utf-8

import myconst
import mycommand
import user_manager
import project_manager
import file_manager
import check_input
from device_manager import DEVICE_MANAGER
from connection_manager import CONNECTION_MANAGER

IDE         = myconst.IDE
ANDROID     = myconst.ANDROID
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
DEVICE_ID   = myconst.DEVICE_ID
DEVICES     = "devices"

'''
app.pyから呼ばれ、コマンドを見て関数を呼ぶ
@param websock
@param session_id
@oaram command   
@param data

@return session_id
@return command
@return data
'''
def receive_ide(websock, session_id, command, data):
    # user register
    if command == myconst.REGISTER:
        res = receive_ide_register(websock, data);
        data = {RES:res}
    # login
    elif command == myconst.LOGIN:
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
    if command == myconst.PRO_CREATE:
        project_id, res = receive_ide_pro_create(user_id, data);
        data = {PRO_ID:project_id, RES:res};
    # project_list
    elif command == myconst.PRO_LIST:
        project_lists, res = receive_ide_pro_list(user_id);
        data = {PRO_LIST:project_lists, RES:res};
    # project_delete
    elif command == myconst.PRO_DELETE:
        res = receive_ide_pro_delete(user_id, data);
        data = {RES:res};
    # project_rename
    elif command == myconst.PRO_RENAME:
        res = receive_ide_pro_rename(user_id, data);
        data = {RES:res};
    # file_save
    elif command == myconst.SAVE:
        file_id, res = receive_ide_save(user_id, data);
        data = {RES:res, FILE_ID:file_id};
    # renew
    elif command == myconst.RENEW:
        res = receive_ide_renew(data);
        data = {RES:res};
    # open
    elif command == myconst.OPEN:
        code, res = receive_ide_open(data);
        data = {RES:res, CODE:code};
    # delete
    elif command == myconst.DELETE:
        res = receive_ide_delete(data);
        data = {RES:res};
    # list
    elif command == myconst.LIST:
        file_lists, res = receive_ide_list(user_id, data);
        data = {RES:res, FILE_LIST:file_lists};
    # rename
    elif command == myconst.RENAME:
        res = receive_ide_rename(data);
        data = {RES:res};
    # redir
    elif command == myconst.REDIR:
        res = receive_ide_redir(data);
        data = {RES:res};
    # info
    elif command == myconst.INFO:
        file_name, directory, project_id, res = receive_ide_info(data);
        data = {RES:res, FILE_NAME:file_name, DIR:directory, PRO_ID:project_id};
    # who_android
    elif command == myconst.WHO_ANDROID:
        devices, res = receive_ide_who_android(user_id);
        data = {RES:res, DEVICES:devices};
    # run_request
    elif command == myconst.RUN_REQUEST:
        res = receive_ide_run_request(data, session_id);
        data = {RES:res};

    # response
    print session_id, command, data;
    return (session_id, data);

def receive_ide_register(websock, data):
    res = check_input.register(data);
    if res != myconst.OK:
        return (res);
    user_id = data[USER];
    password = data[PASS];
    address = data[MAIL];
    grade = data[GRADE];
    # check is user_id unique
    if user_manager.check_unique_user_id(user_id) is False:
        return (myconst.USER_EXISTING);
    user_manager.append(user_id, password, address, grade);
    return (myconst.OK);

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

def receive_ide_save(user_id, data):
    res = check_input.save(data);
    if res != myconst.OK:
        return ("", res);
    file_name = data[FILE_NAME];
    project_id = data[PRO_ID];
    directory = data[DIR];
    code = data[CODE];
    # check use_id and project_id
    if project_manager.is_valid_project_id(user_id, project_id) is False:
        return ("", myconst.PROJECT_NO_EXISTING);
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
    # check use_id and project_id
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

def receive_ide_info(data):
    res = check_input.info(data);
    if res != myconst.OK:
        return ("", "", "", res);
    file_id = data[FILE_ID];
    # check is file id
    if file_manager.is_valid_file_id(file_id) is False:
        return ("", "", "", myconst.FILE_NO_EXISTING);
    file_name, directory, project_id = file_manager.info(file_id);
    return (file_name, directory, project_id, myconst.OK);

def receive_ide_who_android(user_id):
    device_ids = DEVICE_MANAGER.get_device_id(user_id);
    devices = [];
    for device in device_ids:
        devices.append({DEVICE_ID:device});
    return (devices, myconst.OK);

def receive_ide_run_request(data, session_id):
    res = check_input.run_request(data);
    if res != myconst.OK:
        return (res);
    print "ko";
    device_id = data[DEVICE_ID];
    code = data[CODE];
    if DEVICE_MANAGER.is_device_id(device_id) is False:
        return (myconst.DEVICE_ID_NO_EXISTING);
    res = send_run_request(device_id, code, session_id);
    return (res);

def send_run_request(device_id, code, ide_session_id):
    session_id = DEVICE_MANAGER.get_session_id(device_id);
    websock = CONNECTION_MANAGER.get_connection(ANDROID, session_id);
    if session_id is None or websock is None:
        return (myconst.USER_NO_EXISTING);
    if DEVICE_MANAGER.connection(device_id, ide_session_id) is False:
        return (myconst.DEVICE_ID_NO_EXISTING);
    request_id = mycommand.get_request_id();
    data = {CODE:code};
    print "kokomadekitayo";
    mycommand.send_websock(websock, ANDROID, session_id, request_id, myconst.RUN_START, data);
    return (myconst.OK);

