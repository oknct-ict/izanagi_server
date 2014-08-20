#!/usr/bin/env python
#coding:utf-8

import myconst
import user_manager
import check_input
from connection_manager import CONNECTION_MANAGER
from device_manager import DEVICE_MANAGER

USER        = myconst.USER 
PASS        = myconst.PASS
MAIL        = myconst.MAIL
GRADE       = myconst.GRADE
RES         = myconst.RES
DEVICE_ID   = myconst.DEVICE_ID
DEVICE_DATA = myconst.DEVICE_DATA

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
def receive_android(websock, session_id, command, data):
    # user_register
    if command == myconst.REGISTER:
        res = receive_android_register(websock, data);
        data = {RES:res}
    # user_login
    if command == myconst.LOGIN:
        session_id, res = receive_android_login(websock, data);
        data = {RES:res}

    # response
    print session_id, command, data;
    return (session_id, command, data);

def receive_android_register(websock, data):
    res = check_input.register(data);
    if res != myconst.OK:
        return (res);
    user_id = data[USER];
    password = data[PASS];
    address = data[MAIL];
    grade = data[GRADE];
    # chech is user_id unique
    if user_manager.check_unique_user_id(user_id) is False:
        return (myconst.USER_EXISTING);
    user_manager.append(user_id, password, address, grade);
    return (myconst.OK);

def receive_android_login(websock, data):
    res = check_input.login_android(data);
    if res != myconst.OK:
        return ("", res);
    user_id = data[USER];
    password = data[PASS];
    device_id = data[DEVICE_DATA][DEVICE_ID];
    # userdata check
    if user_manager.is_valid_user_id(user_id, password) is False:
        # no user data 
        return ("", myconst.USER_DATA_FAULT);
    # access_point num check
    if CONNECTION_MANAGER.possible_append(myconst.ANDROID, user_id) is False:
        # access_point is over 
        return ("", myconst.ACCESS_POINT_OVER);
    # connection 
    session_id = CONNECTION_MANAGER.append(myconst.ANDROID, websock, user_id);
    # device connection
    DEVICE_MANAGER.append(device_id, user_id, session_id);
    return (session_id, myconst.OK);

