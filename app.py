#!/usr/bin/env python
#coding:utf-8

import os
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template, g, redirect
import pymongo
import json
import server.myide as myide
import server.myandroid as myandroid
import server.myconst as myconst
import server.mycommand as mycommand
import server.check_input as check_input
from server.device_manager import DEVICE_MANAGER
from server.connection_manager import CONNECTION_MANAGER

IDE     = myconst.IDE
ANDROID = myconst.ANDROID

app = Flask(__name__);

@app.route('/')
def index():
    return render_template('index.html');

@app.route("/test")
def test():
    return render_template("test.html");

@app.route("/test2")
def test2():
    return render_template("android.html");

'''
IDEの通信の受け口
'''
@app.route('/websock/ide/')
def websock_ide():
    session_id = None;
    if request.environ.get('wsgi.websocket'):
        websock = request.environ['wsgi.websocket'];
        while True:
            data = websock.receive();
            if not data:
                break;
            json_data = json.loads(data);
            print json_data
            # check json form
            if check_input.input_json(json_data) != myconst.OK:
                # not correct
                mycommand.send_json_error(websock, IDE);
                continue;
            # if not first time login
            if json_data["command"] == myconst.LOGIN and session_id is not None:
                # disconnect
                CONNECTION_MANAGER.delete(IDE, session_id);
                DEVICE_MANAGER.delete_session_id(IDE, session_id);
                session_id = None;
            session_id, request_id, command, data = get_json(json_data);
            session_id, data = myide.receive_ide(websock, session_id, command, data);
            mycommand.send_websock(websock, IDE, session_id, request_id, command, data);
            print "devices";
            DEVICE_MANAGER.output();
            print;
    # sessin_id exist => disconnect
    CONNECTION_MANAGER.delete(IDE, session_id);
    DEVICE_MANAGER.delete_session_id(IDE, session_id);
    return "Disconnect";

'''
Androidの通信の受け口
'''
@app.route('/websock/android/')
def websock_android():
    session_id = None;
    if request.environ.get('wsgi.websocket'):
        websock = request.environ['wsgi.websocket'];
        while True:
            data = websock.receive();
            if not data:
                break;
            json_data = json.loads(data);
            # check json form
            if check_input.input_json(json_data) != myconst.OK:
                # not correct
                mycommand.send_json_error(websock, ANDROID);
                continue;
            print json_data
            # if not first time login
            if json_data["command"] == myconst.LOGIN and session_id is not None:
                # disconnect
                CONNECTION_MANAGER.delete(ANDROID, session_id);
                DEVICE_MANAGER.delete_session_id(ANDROID, session_id);
                session_id = None;
            session_id, request_id, command, data = get_json(json_data);
            session_id, command, data = myandroid.receive_android(websock, session_id, command, data);
            mycommand.send_websock(websock, ANDROID, session_id, request_id, command, data);
            print "devices";
            DEVICE_MANAGER.output();
            print "connections";
            CONNECTION_MANAGER.output(ANDROID);
            print;
    # session_id exist => disconnect
    DEVICE_MANAGER.delete_session_id(ANDROID, session_id);
    CONNECTION_MANAGER.delete(ANDROID, session_id);
    return "Disconnect";

'''
辞書型のJSONを１つ１つの変数に分ける
@param json_data ユーザーから入力されるJSONデータをDictonaryにしたもの
@return session_id
@return command
@return data
'''
def get_json(json_data):
    session_id = json_data["session_id"];
    request_id = json_data["request_id"];
    command = json_data["command"];
    data = json_data["data"];
    return (session_id, request_id, command, data);

@app.before_request
def before_request():
    g.conn = pymongo.Connection();
    g.db = g.conn["izanagi_db"];

@app.teardown_request
def teardown_request(exception):
    g.conn.close();

if __name__ == '__main__':
        app.debug = True
        server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler);
        server.serve_forever();
