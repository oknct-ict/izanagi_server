import mycommand
import myconst
from connection_manager import CONNECTION_MANAGER

def receive_android(websock, user_id, command, data):
    # login
    if command == myconst.LOGIN_REQ:
        receive_android_syn(websock, user_id, data);
    return res;

def receive_android_login(user_id, password):
    res = CONNECTION_MANAGER.check_user(user_id, password)
    if res is SUCCESS:
        res = CONNECTIOM_MANAGER.append(ANDROID, websock, user_id);
    return res;
