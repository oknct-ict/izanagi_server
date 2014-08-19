#!/usr/bin/env python
#coding:utf-8

import myconst
import user_manager
import check_input
from connection_manager import CONNECTION_MANAGER

USER = myconst.USER 
PASS = myconst.PASS
MAIL = myconst.MAIL
GRADE = myconst.GRADE
RES = myconst.RES

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
def receive_android(websock, session_id, command, data):
    # user_login
    if command == myconst.LOGIN_REQ:
        command = myconst.LOGIN_RES;
        session_id, res = receive_android_login(websock, data);
        data = {RES:res}

    # response
    print session_id, command, data;
    return (session_id, command, data);

'''
ログインをする
@param websock
@param user_id      ユーザーID
@param password     パスワード（平文）
@return session_id  成功：セッションID、失敗：空文字列
@return res         成功：0、失敗：エラーコード
'''
def receive_android_login(websock, data):
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
    if CONNECTION_MANAGER.possible_append(myconst.ANDROID, user_id) is False:
        # access_point is over 
        return ("", myconst.ACCESS_POINT_OVER);
    # connection 
    session_id = CONNECTION_MANAGER.append(myconst.ANDROID, websock, user_id);
    return (session_id, myconst.OK);

