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
        for connection_type in connection_types.VALID_TYPES:
            self._connections[connection_type] = {}

    @connection_types.validater(1)
    def append(self, connection_type, connection, user_id):
        session_id = mycommand.random_str(16);
        self._connections[connection_type].update({session_id: {USER:user_id, CONN:connection}});
        return session_id;
        
    @connection_types.validater(1)
    def delete(self, connection_type, session_id):
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
    def is_connectioned_user(self, connection_type, user_id):
        lists = self._connections[connection_type].values();
        for l in lists:
            if user_id in l[USER]:
                return True;
        return False;
        
    @connection_types.validater(1)
    def get_connection(self, connection_type, session_id):
        print"hoge";
        self.output(connection_type);
        print "hage";
        print "kiteru", self._connections[connection_type].keys()
        keys = self._connections[connection_type].keys()
        for key in keys:
            print key, self._connections[connection_type][key][CONN];
            if session_id == key:
                return self._connections[connection_type][key][CONN];
        return None;
        
CONNECTION_MANAGER = _ConnectionManager()

if __name__ == "__main__":
    pass
