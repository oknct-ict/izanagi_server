import mycommand
import myconst

def receive_ide(websock, command, message):
	if command == myconst.SYN:
		receive_ide_syn(websock, message);
	return;

def receive_ide_syn(websock, message):
	mycommand.send_ack(websock, myconst.IDE);
	mycommand.send_source_to_android(message);
	return;

