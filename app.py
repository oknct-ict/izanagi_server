import os
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template, g, redirect
import pymongo
import json

app = Flask(__name__);

connect_list = {"ide":[], "android":[]};

@app.route('/')
def index():
	return render_template('index.html');

@app.route('/echo')
def echo():
	print("echo come");
	if request.environ.get('wsgi.websocket'):
		websock = request.environ['wsgi.websocket'];
		while True:
			data = websock.receive();
			if not data:
				break;
			print("websock get");
			json_data = json.loads(data);
			print(json_data);
			append_list_websock(websock, json_data["type"]);
			send_response(websock, json_data["type"], json_data["command"], json_data["message"]);
			output_websock();
	return "Disconnect";				

def is_valid_websock(websock, connect_type):
	return websock in connect_list[connect_type];

def append_list_websock(websock, connect_type):
	if is_valid_websock(websock, connect_type):
		return;
	connect_list[connect_type].append(websock);

def send_response(websock, connect_type, command, message):
	if command == "SYN":
		if message != "":
			send_source_to_android(message);
		else:
			send_ack(websock, connectType);
	return;

def send_source_to_android(message):
	json_data = make_json("android", "SYN", message);
	for ws in connect_list["android"]:
		ws.send(json_data);
	return;
		
def send_ack(websock, connectType):
	json_data = make_json(connectType, "ACK", "");
	websock.send(json_data);
	print("send_ack:" + json_data);
	return;

def make_json(connectType, command, message):
	json_data = json.dumps({
		"type":connectType,
		"command":command,
		"message":message});
	return json_data;

def output_websock():
	print("===output===\nide");
	for ws in connect_list["ide"]:
		print(ws);
	print("android");
	for ws in connect_list["android"]:
		print(ws);
	print("===end===");
	
if __name__ == '__main__':
		app.debug = True
		server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler);
		server.serve_forever();
