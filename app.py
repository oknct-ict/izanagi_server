import os
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template, g, redirect
import pymongo
import json

app = Flask(__name__);

NULL_CHARACTER = "";
IDE = "ide";
ANDROID = "android";

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
			if json_data["type"] == IDE:
				if json_data["command"] == "SYN":
					send_ack(websock, IDE);
					send_source_to_android(json_data["message"]);
			else:
				if json_data["command"] == "SYN":
					send_ack(websock, ANDROID);
			output_websock();
	return "Disconnect";				

def is_valid_websock(websock, connect_type):
	return websock in connect_list[connect_type];

def append_list_websock(websock, connect_type):
	if is_valid_websock(websock, connect_type):
		return;
	connect_list[connect_type].append(websock);

def send_ack(websock, connect_type):
	json_data = make_json(connect_type, "ACK", "");
	websock.send(json_data);
	print("send_ack:" + json_data);
	return;

def send_source_to_android(source):
	if source == NULL_CHARACTER:
		return;
	json_data = make_json(ANDROID, "ACK", source);
	for ws in connect_list[ANDROID]:
		ws.send(json_data);
	return;

def make_json(connect_type, command, message):
	json_data = json.dumps({
		"type":connect_type,
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
