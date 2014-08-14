#!/usr/bin/env python
#coding:utf-8

import mycommand
import myconst
import user_manager
from connection_manager import CONNECTION_MANAGER

USER = "user_id"
PASS = "password"
RES = "result"

def receive_ide(websock, session_id, command, data):
    # login
    if command == myconst.LOGIN_REQ:
        command = myconst.LOGIN_RES;
        session_id = receive_ide_login(websock, data[USER], data[PASS]);
        # login accept 
        if session_id is None:
            session_id = "";
            data = {RES:myconst.USER_DATA_FAULT};
        else:
            data = {RES:myconst.OK};
        
    # save
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

def receive_ide_login(websock, user_id, password):
    # userdata check
    if user_manager.check_db(user_id, password) is False:
        # no user data 
        return None;
    # connection 
    session_id = CONNECTION_MANAGER.append(myconst.IDE, websock, user_id);
    return session_id;

def receive_ide_save():
    return;

def receive_ide_renew():
    return;

def receive_ide_open():
    return;

def receive_ide_view_list():
    return;
