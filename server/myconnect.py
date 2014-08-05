from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import myconst

connect_list = {myconst.IDE:[], myconst.ANDROID:[]}

def append_connection(websock, connect_type):
	if is_connectioned(websock, connect_type):
		return;
	connect_list[connect_type].append(websock);

def is_connectioned(websock, connect_type):
	return websock in connect_list[connect_type];

def disconnect_websock(websock):
	if websock in connect_list[myconst.IDE]:
		connect_list[myconst.IDE].remove(websock);
	elif websock in connect_list[myconst.ANDROID]:
		connect_list[myconst.ANDROID].remove(websock);
	return;

def get_websocket(connect_type):
	for ws in connect_list[connect_type]:
		if not ws.closed:
			return (ws);
		else:
			connect_list[connect_type].remove(ws);
	return None;

def output_websock():
	print("===output===");
	print(myconst.IDE);
	for ws in connect_list[myconst.IDE]:
		print(ws);
	print(myconst.ANDROID);
	for ws in connect_list[myconst.ANDROID]:
		print(ws);
	print("===end===");
	
