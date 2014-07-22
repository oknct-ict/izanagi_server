import os
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template
import json

app = Flask(__name__);

@app.route('/')
def index():
	return render_template('index.html');

@app.route('/echo')
def echo():
	if request.environ.get('esgi.websocket'):
		websock = request.environ['wsgi.websocket'];
		while True:
			data = websock.receive();
			if not data:
				break;
			jsonData = json.loads(data);
			append_list_websock(websock, jsonData["type"]);
			send_response(websock, jsonData["type"], jsonData["command"], jsonData["message"]);
	return;				

def append_list_websock(websock, connectType):
	if connectType == "ide":
		if is_websock_list(ide_list, websock) == True:
			return;
		ide_list.append(websock);
	else:
		if is_websock_list(android_list, websock) == True:
				return;
		android_list.append(websock);
	return;

def is_websock_list(lists, websock):
	for ws in lists:
		if ws == websock:
			return True;
	return False;	

def send_response(websock, connectType, command, message):
	if command == "SYN":
		if message != "":
			send_source_to_android(message);
		else:
			send_ack(websock, connectType);
	return;

def send_source_to_android(message):
	jsonData = make_json("android", "SYN", message);
	for ws in android_list:
		ws.send(jsonData);
	return;
		
def send_ack(websock, connectType):
	jsonData = make_json(connectType, "ACK", "");
	websock.send(jsonData);
	return;

def make_json(connectType, command, message):
	jsonData = json.dumps({
		"type":connectType,
		"command":command,
		"message":message});
	return jsonData;

