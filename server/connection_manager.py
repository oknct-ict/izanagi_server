#!/usr/bin/env python
#coding:utf-8

"""
This module import by
form connection_manager impot CONNECTION_MANAGER
"""

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

CONNECTION_MANAGER = _ConnectionManager()

if __name__ == "__main__":
    pass
