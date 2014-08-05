import os
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template, g, redirect
import pymongo
import json
import server.myconnect as myconnect
import server.myide as myide
import server.myandroid as myandroid
import server.myconst as myconst

app = Flask(__name__);

@app.route('/')
def index():
	return render_template('index.html');

@app.route('/echo')
def echo():
	websock = "";
	if request.environ.get('wsgi.websocket'):
		websock = request.environ['wsgi.websocket'];
		while True:
			data = websock.receive();
			if not data:
				break;
			json_data = json.loads(data);
			receive(websock, json_data);
			myconnect.output_websock();
	myconnect.disconnect_websock(websock);
	myconnect.output_websock();
	return "Disconnect";				

def receive(websock, json_data):
	connect_type = json_data["type"];
	command = json_data["command"];
	message = json_data["message"];
	myconnect.append_connection(websock, connect_type);
	if connect_type == myconst.IDE:
		myide.receive_ide(websock, command, message);
	else:
		myandroid.receive_android(websock, command, message);
	return;

if __name__ == '__main__':
		app.debug = True
		server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler);
		server.serve_forever();
