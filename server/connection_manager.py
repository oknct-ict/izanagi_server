#!/usr/bin/env python
#coding:utf-8

"""
This module import by
form connection_manager impot CONNECTION_MANAGER
"""
import mycommand
import connection_types

USER = "user_id"
CONN = "connection"

class _ConnectionManager(object):
    def __init__(self):
        self._connections = {}
        self._connection_count = {}
        for connection_type in connection_types.VALID_TYPES:
            self._connections[connection_type] = {}
            self._connection_count[connection_type] = {}

    @connection_types.validater(1)
    def append(self, connection_type, connection, user_id):
        session_id = mycommand.get_random_str(16);
        self._connections[connection_type].update({session_id: {USER:user_id, CONN:connection}});
        # user already connectioned 
        if user_id in self._connection_count[connection_type]:
            count = self._connection_count[connection_type][user_id] + 1;
            self._connection_count[connection_type][user_id] = count;
        # first time connectioned
        else:
            self._connection_count[connection_type].update({user_id:1});
        print user_id, self._connection_count[connection_type][user_id];
        return session_id;
        
    @connection_types.validater(1)
    def delete(self, connection_type, session_id):
        # connection count update
        user_id = self._connections[connection_type][session_id][USER];
        count = self._connection_count[connection_type][user_id]
        if count == 0:
            del self._connection_count[connection_type][user_id];
        else:
            self._connection_count[connection_type][user_id] = count - 1;
        # connection delete
        del self._connections[connection_type][session_id];
        return;
        
    @connection_types.validater(1)
    def output(self, connection_type):
        for session_id in self._connections[connection_type]:
            print "session_id:" , session_id, \
                " user_id:", self._connections[connection_type][session_id][USER], \
                " connection:", self._connections[connection_type][session_id][CONN];
        return;
        
    @connection_types.validater(1)
    def possible_append(self, connection_type, user_id):
        if user_id in self._connection_count[connection_type]:
            if self._connection_count[connection_type][user_id] > 2:
                return False;
        return True;

    @connection_types.validater(1)
    def is_connectioned_user(self, connection_type, user_id):
        if user_id in self._connection_count[connection_type]:
                return True;
        return False;
        
    @connection_types.validater(1)
    def get_connection(self, connection_type, session_id):
        keys = self._connections[connection_type].keys()
        for key in keys:
            if session_id == key:
                print "session_id is exist";
                return self._connections[connection_type][key][CONN];
        print "session_id is not exist";
        return None;
        
    @connection_types.validater(1)
    def is_valid_websocket(self, connection_type, session_id, websock):
        get_ws = self.get_connections(connection_type, session_id);
        if websock == get_ws:
            return True;
        return False;

CONNECTION_MANAGER = _ConnectionManager()

if __name__ == "__main__":
    pass
