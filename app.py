import os
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template, g, redirect
import pymongo
import json

app = Flask(__name__);

IDE = "ide";
ANDROID = "android";
SYN = "SYN";
ACK = "ACK";
connect_list = {IDE:[], ANDROID:[]};

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
	disconnect_websock(websock);
	return "Disconnect";				

def receive(websock, json_data):
	connect_type = json_data["type"];
	command = json_data["command"];
	message = json_data["message"];
	append_connection(websock, connect_type);
	if connect_type == IDE:
		receive_ide(websock, command, message);
	else:
		receive_android(websock, command, message);
	return;

def receive_ide(websock, command, message):
	if command == SYN:
		receive_ide_syn(websock, message);
	return;

def receive_android(websock, command, message):
	if command == SYN:
		receive_android_syn(websock, message);
	return;

def receive_ide_syn(websock, message):
	send_ack(websock, IDE);
	send_source_to_android(message);
	return;

def receive_android_syn(websock, message):
	send_ack(websock, ANDROID);
	return;

def append_connection(websock, connect_type):
	if is_connectioned(websock, connect_type):
		return;
	connect_list[connect_type].append(websock);

def is_connectioned(websock, connect_type):
	return websock in connect_list[connect_type];

def send_ack(websock, connect_type):
	json_data = make_json(connect_type, ACK, "");
	websock.send(json_data);
	return;

def send_source_to_android(source):
	json_data = make_json(ANDROID, ACK, source);
	for ws in connect_list[ANDROID]:
		if not ws.closed: 
			ws.send(json_data);
		else:
			connect_list[ANDROID].remove(ws);
	return;

def disconnect_websock(websock):
	if websock in connect_list[IDE]:
		connect_list[IDE].remove(websock);
	elif websock in connect_list[ANDROID]:
		connect_list[ANDROID].remove(websock);
	return;

def make_json(connect_type, command, message):
	json_data = json.dumps({
		"type":connect_type,
		"command":command,
		"message":message});
	return json_data;

def output_websock():
	print("===output===");
	print(IDE);
	for ws in connect_list[IDE]:
		print(ws);
	print(ANDROID);
	for ws in connect_list[ANDROID]:
		print(ws);
	print("===end===");
	
if __name__ == '__main__':
		app.debug = True
		server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler);
		server.serve_forever();
