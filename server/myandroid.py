#!/usr/bin/env python
#coding:utf-8

import myconst
import mycommand
import user_manager
import check_input
from connection_manager import CONNECTION_MANAGER
from device_manager import DEVICE_MANAGER

IDE         = myconst.IDE
ANDROID     = myconst.ANDROID
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
    # run_start (respnse)
    if command == myconst.RUN_START:
        res = receive_android_run_start(session_id, data);
        command = myconst.NO_SEND;
    # log
    if command == myconst.LOG_ANDROID:
        receive_android_log(session_id, data);
        command = myconst.NO_SEND;
    # run_end_android
    if command == myconst.RUN_END_ANDROID:
        receive_android_run_end(session_id, data);
        command = myconst.NO_SEND;

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
    if user_manager.check_unique_user_id(user_id) == False:
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
    if user_manager.is_valid_user_id(user_id, password) == False:
        # no user data 
        return ("", myconst.USER_DATA_FAULT);
    # access_point num check
    if CONNECTION_MANAGER.possible_append(myconst.ANDROID, user_id) == False:
        # access_point is over 
        return ("", myconst.ACCESS_POINT_OVER);
    # connection 
    session_id = CONNECTION_MANAGER.append(myconst.ANDROID, websock, user_id);
    # device connection
    DEVICE_MANAGER.append(device_id, user_id, session_id);
    return (session_id, myconst.OK);

def send_to_ide(session_id, command, data):
    # get device_id
    device_id = DEVICE_MANAGER.get_device_id_from_android(session_id);
    if device_id is None:
        print myconst.SESSION_ID_NO_EXISTING;
        return;
    # get session_id
    session_id = DEVICE_MANAGER.get_session_ide(device_id);
    if session_id is None:
        print myconst.DEVICE_ID_NO_EXISTING;
        return;
    # get websock 
    websock = CONNECTION_MANAGER.get_connection(IDE, session_id);
    if websock is None:
        print myconst.SESSION_ID_NO_EXISTING;
        return;
    # send to ide
    mycommand.send_websock(websock, IDE, session_id, mycommand.get_request_id(), command, data);
    if myconst.RUN_END_IDE is command:
        # device manager disconnected
        DEVICE_MANAGER.delete_session_id(IDE, session_id);
    
def receive_android_run_start(session_id, data):
    # format check
    res = check_input.run_start(data);
    if res != myconst.OK:
        print myconst.RUN_START, res;
        return;
    send_to_ide(session_id, myconst.SENDED_CODE, data);
    
def receive_android_log(session_id, data):
    # format check
    res = check_input.log_android(data);
    if res != myconst.OK:
        print myconst.LOG_ANDROID, res;
        return;
    send_to_ide(session_id, myconst.LOG_IDE, data); 

def receive_android_run_end(session_id, data):
    res = check_input.run_end(data);
    if res != myconst.OK:
       print myconst.RUN_END_ANDROID, res;
       return;
    send_to_ide(session_id, myconst.RUN_END_IDE, data);

