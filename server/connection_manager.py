#!/usr/bin/env python
#coding:utf-8

"""
This module import by
form connection_manager impot CONNECTION_MANAGER
"""
from flask import g
import pymongo
import connection_types

class _ConnectionManager(object):
    def __init__(self):
        self._connections = {}
        for connection_type in connection_types.VALID_TYPES:
            self._connections[connection_type] = set()

    @connection_types.validater(1)
    def get_connections(self, connection_type):
        for connection in self._connections[connection_type]:
            yield connection

    @connection_types.validater(1)
    def remove(self, connection_type, connection):
        self._connections[connection_type].discard(connection)

    @connection_types.validater(1)
    def append(self, connection_type, connection):
        self._connections[connection_type].add(connection)

    @connection_types.validater(1)
    def output(self, connection_type):
        for ws in self._connections[connection_type]:
            print(ws);

    def check_user(self, user):
        print(user);
        print(g.db.users.find_one({"id":user}));
        return (g.db.users.find_one({"id":user}));

CONNECTION_MANAGER = _ConnectionManager()

if __name__ == "__main__":
    pass
