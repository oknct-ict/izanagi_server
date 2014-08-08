import mycommand
import myconst
from connection_manager import CONNECTION_MANAGER

def receive_ide(websock, user_id, command, data):
    res = "";
    # login
    if command == myconst.LOGIN_REQ:
        res = receive_ide_login(websock, user_id, data);
    # save
    elif command == myconst.SAVE_REQ:
        res = receive_ide_save(websock, user_id, data);
    # renew
    elif command == myconst.RENEW_REQ:
        res = receive_ide_renew(websock, user_id, data);
    # open
    elif command == myconst.OPEN_REQ:
        res = receive_ide_open(websock, user_id, data);
    # view_list
    elif command == myconst.VIEW_LIST_REQ:
        res = receive_ide_view_list(websock, user_id, data);
    # delete
    elif command == myconst.DELETE_REQ:
        res = receive_ide_delete(websock, user_id, data);
    return res;

def receive_ide_login(websock, user_id, password):
    res = CONNECTION_MANAGER.check_user(user_id, password);
    if res is myconst.SUCCESS:
        res = CONNECTION_MANAGER.append(myconst.IDE, websock, user_id);
    return res;

def receive_ide_save(websock, message):
    return;

def receive_ide_renew(websock, message):
    return;

def receive_ide_open(websock, message):
    return;

def receive_ide_view_list(websock, message):
    return;

def receive_ide_delete(websock, message):
    return;

