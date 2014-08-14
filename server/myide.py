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
        session_id, res = receive_ide_login(websock, data[USER], data[PASS]);
        data = {RES:res};
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
        return ("", myconst.USER_DATA_FAULT);
    # access_point num check
    if CONNECTION_MANAGER.possible_append(myconst.IDE, user_id) is False:
        # access_point is over 
        return ("", myconst.ACCESS_POINT_OVER);
    # connection 
    session_id = CONNECTION_MANAGER.append(myconst.IDE, websock, user_id);
    return (session_id, myconst.OK);

def receive_ide_save():
    return;

def receive_ide_renew():
    return;

def receive_ide_open():
    return;

def receive_ide_view_list():
    return;
