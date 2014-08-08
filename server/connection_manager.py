#!/usr/bin/env python
#coding:utf-8

"""
This module import by
form connection_manager impot CONNECTION_MANAGER
"""
from flask import g
import pymongo
import connection_types
import myconst

class _ConnectionManager(object):
    def __init__(self):
        self._connections = {}
        for connection_type in connection_types.VALID_TYPES:
            self._connections[connection_type] = {}

    @connection_types.validater(1)
    def get_connections(self, connection_type, user_id):
        if user_id in self._connections[connection_type]:
            return self._connections[connection_type][user_id];
        return None;

    @connection_types.validater(1)
    def remove(self, connection_type, user_id):
        if self.get_connections(connection_type, user_id) is None:
            return myconst.ERROR_NO_USER;
        del  self._connections[connection_type][user_id];
        return myconst.SUCCESS;

    @connection_types.validater(1)
    def append(self, connection_type, connection, user_id):
        self._connections[connection_type].update({user_id:connection});
        return myconst.SUCCESS;

    @connection_types.validater(1)
    def output(self, connection_type):
        print connection_type;
        print self._connections[connection_type].items();

    def check_user(self, user_id, password):
        if (g.db.users.find_one({"id":user_id, "pass":password})) is None:
            return myconst.ERROR_NO_USER;
        return myconst.SUCCESS;

CONNECTION_MANAGER = _ConnectionManager()

if __name__ == "__main__":
    pass
