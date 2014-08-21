#!/usr/bin/env python
#coding:utf-8

"""
This module import by
form connection_manager impot CONNECTION_MANAGER
"""

import myconst
import mycommand
import connection_types

USER = myconst.USER
CONN = myconst.CONN
DEVICE_ID = myconst.DEVICE_ID
LIMIT_CONNECTION_NUM = 3


'''
IDE⇔サーバ、Android⇔サーバ の通信を管理する。
@インスタンス変数 _connections[connection_type]{}    キー：セッションID、値：ユーザーID、Websocket、デバイスID
@インスタンス変数 _connection_count[connection_type]{}   キー：ユーザーID、値：そのユーザーは現在同時に何個ログインしているのか
connection_type はandroid かideが入る

'''
class _ConnectionManager(object):
    '''
    ConnectionManagerクラスの初期化を行う
    _connections[]{}、_connection_count[]{} 2つのインスタンス変数の空の変数を宣言する
    '''
    def __init__(self):
        self._connections = {}
        self._connection_count = {}
        for connection_type in connection_types.VALID_TYPES:
            self._connections[connection_type] = {}
            self._connection_count[connection_type] = {}

    '''
    コネクションを追加
    @param connection_type      android か ide
    @param connection           実際に通信で使うwebsocket
    @param user_id              ユーザーID
    @param device_id            デバイスID（端末の固有ID)
    @return session_id          セッションID
    '''
    @connection_types.validater(1)
    def append(self, connection_type, connection, user_id, device_id):
        session_id = mycommand.get_random_str(16);
        self._connections[connection_type].update({session_id: {USER:user_id, CONN:connection, DEVICE_ID:device_id}});
        # user already connectioned 
        if user_id in self._connection_count[connection_type]:
            count = self._connection_count[connection_type][user_id] + 1;
            self._connection_count[connection_type][user_id] = count;
        # first time connectioned
        else:
            self._connection_count[connection_type].update({user_id:1});
        print user_id, self._connection_count[connection_type][user_id];
        return session_id;
        
    '''
    コネクションを消去
    @param connection_type      android か ide
    @param session_id           セッションID
    '''
    @connection_types.validater(1)
    def delete(self, connection_type, session_id):
        # connection count update
        user_id = self.get_user_id(connection_type, session_id);
        if user_id is None:
            return;
        count = self._connection_count[connection_type][user_id]
        if count == 1:
            del self._connection_count[connection_type][user_id];
        else:
            self._connection_count[connection_type][user_id] = count - 1;
        # connection delete
        del self._connections[connection_type][session_id];
        print "now connected list";
        self.output(connection_type);
        return;
        
    '''
    現在張っているコネクションを表示
    @param connection_type      android か ide
    '''
    @connection_types.validater(1)
    def output(self, connection_type):
        for session_id in self._connections[connection_type]:
            print "session_id:" , session_id, \
                " user_id:", self._connections[connection_type][session_id][USER], \
                " connection:", self._connections[connection_type][session_id][CONN];
        return;
        
    '''
    指定されたユーザーIDはこれ以上コネクションを張ることができるか
    @param connection_type      android か ide
    @return                     張れる：True、張れない：False
    '''
    @connection_types.validater(1)
    def possible_append(self, connection_type, user_id):
        if user_id in self._connection_count[connection_type]:
            if self._connection_count[connection_type][user_id] > LIMIT_CONNECTION_NUM:
                return False;
        return True;

    '''
    指定されたユーザーIDはコネクションを張っているのか
    @param connection_type      android か ide
    @param user_id              ユーザーID
    @return                     張っている：True、張っていない：False
    '''
    @connection_types.validater(1)
    def is_connectioned_user(self, connection_type, user_id):
        if user_id in self._connection_count[connection_type]:
                return True;
        return False;
        
    '''
    セッションIDからコネクション（Websocket)を求める
    @param connection_type      android か ide
    @param session_id           セッションID
    @return 存在するセッションID:コネクション、存在しない：None
    '''
    @connection_types.validater(1)
    def get_connection(self, connection_type, session_id):
        keys = self._connections[connection_type].keys()
        for key in keys:
            if session_id == key:
                print "session_id is exist";
                return self._connections[connection_type][key][CONN];
        print "session_id is not exist";
        return None;
        
    '''
    セッションIDからuser_idを求める
    @param connection_type      android か ide
    @param session_id           セッションID
    @return 存在するセッションID:ユーザーID、存在しない：None

    '''
    @connection_types.validater(1)
    def get_user_id(self, connection_type, session_id):
        keys = self._connections[connection_type].keys()
        for key in keys:
            if session_id == key:
                print "get connection is ok.", self._connections[connection_type][key][USER];
                return self._connections[connection_type][key][USER];
        print "session_id is not exist";
        return None;

    '''
    セッションIDからdevice_idを求める
    @param connection_type      android か ide
    @param session_id           セッションID
    @return 存在するセッションID:device_id、存在しない：None

    '''
    @connection_types.validater(1)
    def get_device_id(self, connection_type, session_id):
        keys = self._connections[connection_type].keys()
        for key in keys:
            if session_id == key:
                print "get device_id is ok.", self._connections[connection_type][key][DEVICE_ID];
                return self._connections[connection_type][key][DEVICE_ID];
        print "session_id is not exist";
        return None;

    '''
    セッションIDが紐付けられているWebsocketと、引数のWebsocketが正しいかどうか
    @param connection_typ       android か ide
    @param session_id           セッションID
    @param websock              
    @return         正しかった：True、正しくなかった：False 
    '''
    @connection_types.validater(1)
    def is_valid_websocket(self, connection_type, session_id, websock):
        get_ws = self.get_connection(connection_type, session_id);
        if websock == get_ws:
            return True;
        return False;

CONNECTION_MANAGER = _ConnectionManager()

if __name__ == "__main__":
    pass
