#!/usr/bin/env python
#coding:utf-8

from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import myconst
import json
import random
from connection_manager import CONNECTION_MANAGER
    
def send_ide(websock, session_id, command, data):
    json_data = make_json(myconst.IDE, session_id, command, data);
    print "send_ide_no";
    get_ws = CONNECTION_MANAGER.get_connection(myconst.IDE, session_id);
    print websock, get_ws;
    if websock == get_ws:
        websock.send(json_data);

def send_android(websock, session_id, command, data):
    json_data = make_json(myconst.ANDROID, session_id, command, data);
    get_ws = get_conection(session_id);
    ws.send(json_data);

def make_json(connect_type, session_id, command, data):
    json_data = json.dumps({
        "type":connect_type,
        "session_id":session_id,
        "command":command,
        "data":data});
    return json_data;

def random_str(length):
    strlist = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz123456789";
    random_str = "";
    for i in range(length):
        x = random.randint(0, len(strlist) - 1);
        random_str += strlist[x];
    print random_str;
    return random_str;


