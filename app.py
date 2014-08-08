import os
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template, g, redirect
import pymongo
import json
import server.myide as myide
import server.myandroid as myandroid
import server.myconst as myconst
from server.connection_manager import CONNECTION_MANAGER

app = Flask(__name__);

@app.route('/')
def index():
    return render_template('index.html');

@app.route('/echo')
def echo():
    user_id = "";
    if request.environ.get('wsgi.websocket'):
        websock = request.environ['wsgi.websocket'];
        while True:
            data = websock.receive();
            if not data:
                break;
            json_data = json.loads(data);
            user_id = json_data["id"];
            print(json_data);
            receive(websock, json_data);
            CONNECTION_MANAGER.output(myconst.IDE);
    print "Disconnect";
    CONNECTION_MANAGER.remove(myconst.IDE, user_id);
    CONNECTION_MANAGER.remove(myconst.ANDROID, user_id);
    return "Disconnect";

def receive(websock, json_data):
    connect_type = json_data["type"];
    user_id = json_data["id"];
    command = json_data["command"];
    data = json_data["data"];
    result = json_data["result"];
    if connect_type == myconst.IDE:
        myide.receive_ide(websock, user_id, command, data);
    else:
        myandroid.receive_android(websock, user_id, command, data);
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
