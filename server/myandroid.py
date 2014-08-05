import mycommand
import myconst

def receive_android(websock, command, message):
	if command == myconst.SYN:
		receive_android_syn(websock, message);
	return;

def receive_android_syn(websock, message):
	mycommand.send_ack(websock, myconst.ANDROID);
	return;

