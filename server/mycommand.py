#!/usr/bin/env python
#coding:utf-8

import myconst
import json
import random
import hashlib

'''
Websocketを使ってIDE か Androidに送信をする
@param websock
@param connection_type
@param session_id
@param command
@param data
'''
def send_websock(websock, connection_type, session_id, request_id, command, data):
    if command == myconst.NO_SEND:
        print "no send";
        return;
    json_data = make_json(connection_type, session_id, request_id, command, data);
    print "send:", json_data;
    websock.send(json_data);

'''
エラーだった
@param websock
@param connection_type
'''
def send_json_error(websock, connection_type):
    json_data = make_json(connection_type, "", "", myconst.JSON_ERROR, {});
    print "send:", json_data;
    websock.send(json_data);

'''
送信するときに必要なjson形式をつくる
@param connect_type
@param session_id
@param command
@param data
@return json_data
'''
def make_json(connect_type, session_id, request_id, command, data):
    json_data = json.dumps({
        "type":connect_type,
        "session_id":session_id,
        "request_id":request_id,
        "command":command,
        "data":data}, ensure_ascii=False);
    return json_data;

'''
指定された文字数のランダムな文字列を生成する
@param length           作りたい文字列の長さ
@return random_str      ランダム文字列
'''
def get_random_str(length):
    strlist = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz123456789";
    random_str = "";
    for i in range(length):
        x = random.randint(0, len(strlist) - 1);
        random_str += strlist[x];
    print random_str;
    return random_str;

'''
文字列をSHA256にする
@param password     作りたい文字列
@return             SHA256された文字列
'''
def get_sha256(string):
    return hashlib.sha256(string).hexdigest();


'''
リクエストIDを生成する
@return             Int型
'''
def get_request_id():
    return random.randint(0, 2 ** 31);
    

