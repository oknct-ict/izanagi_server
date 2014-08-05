from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import myconnect
import myconst
import json

def send_ack(websock, connect_type):
	json_data = make_json(connect_type, myconst.ACK, "");
	websock.send(json_data);
	return;

def send_source_to_android(source):
	json_data = make_json(myconst.ANDROID, myconst.ACK, source);
	ws = myconnect.get_websocket(myconst.ANDROID);
	if not (ws is None):
		ws.send(json_data);
	return;

def make_json(connect_type, command, message):
	json_data = json.dumps({
		"type":connect_type,
		"command":command,
		"message":message});
	return json_data;

