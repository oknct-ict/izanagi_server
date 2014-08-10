import mycommand
import myconst
from connection_manager import CONNECTION_MANAGER

def receive_ide(websock, user_id, command, data):
    "";
    # login
    if command == myconst.LOGIN_REQ:
        receive_ide_login(websock, user_id, data);
    # save
    elif command == myconst.SAVE_REQ:
        receive_ide_save(websock, user_id, data);
    # renew
    elif command == myconst.RENEW_REQ:
        receive_ide_renew(websock, user_id, data);
    # open
    elif command == myconst.OPEN_REQ:
        receive_ide_open(websock, user_id, data);
    # view_list
    elif command == myconst.VIEW_LIST_REQ:
        receive_ide_view_list(websock, user_id, data);
    # delete
    elif command == myconst.DELETE_REQ:
        receive_ide_delete(websock, user_id, data);
    return;

def receive_ide_login(websock, user_id, password):
    res = CONNECTION_MANAGER.check_user_db(user_id, password);
    if res is myconst.SUCCESS:
        res = CONNECTION_MANAGER.append(myconst.IDE, websock, user_id);

    if res == myconst.SUCCESS:
        mycommand.send_websock(websock, myconst.IDE, user_id, myconst.LOGIN_RES, "", res);
    else:
        mycommand.send_websock(websock, myconst.IDE, user_id, myconst.LOGIN_RES, myconst.ERROR_NO_USER, res);

    return;

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

