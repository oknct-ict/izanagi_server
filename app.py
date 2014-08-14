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
from server.connection_manager import CONNECTION_MANAGER

app = Flask(__name__);

@app.route('/')
def index():
    return render_template('test.html');

@app.route('/websock/ide/')
def websock_ide():
    websock = None;
    if request.environ.get('wsgi.websocket'):
        websock = request.environ['wsgi.websocket'];
        while True:
            data = websock.receive();
            if not data:
                break;
            json_data = json.loads(data);
            session_id, command, data = get_json(json_data);
            session_id, command, data = myide.receive_ide(websock, session_id, command, data);
            mycommand.send_ide(websock, session_id, command, data);
    if websock is not None:
        CONNECTION_MANAGER.remove(myconst.IDE, websock);
    return "Disconnect";

@app.route('/websock/android/')
def websock_android():
    websock = None;
    if request.environ.get('wsgi.websocket'):
        websock = request.environ['wsgi.websocket'];
        while True:
            data = websock.receive();
            if not data:
                break;
            json_data = json.loads(data);
    if websock is not None:
        CONNECTION_MANAGER.remove(myconst.ANDROID, websock);
    return "Disconnect";

def get_json(json_data):
    session_id = json_data["session_id"];
    command = json_data["command"];
    data = json_data["data"];
    return (session_id, command, data);

    if connect_type == myconst.IDE:
        myide.receive_ide(websock, session_id, command, data);
    else:
        myandroid.receive_android(websock, session_id, command, data);
    return;

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
