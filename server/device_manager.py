#!/usr/bin/env python
#coding:utf-8

import myconst
import mycommand

IDE         = myconst.IDE
ANDROID     = myconst.ANDROID
USER        = myconst.USER
DEVICE_ID   = myconst.DEVICE_ID

class _DeviceManger(object):
    def __init__(self):
        self._devices = {};

    def append(self, device_id, user_id, session_id):
        self._devices.update({device_id: {USER:user_id, ANDROID:session_id}});

    '''
    デバイスIDは張っているのか
    '''
    def is_device_id(self, device_id):
        if device_id in self._devices:
           return True;
        return False;


    '''
    指定したデバイスIDを消去する
    '''
    def delete(self, device_id):
        if self.is_device_id(device_id) is False:
            return False;
        del self._devices[device_id];
        return True;

    '''
    指定したsession_idから消去する
    '''
    def delete_session_id(self, session_id):
        for device_id in self._devices:
            if self._devices[device_id][ANDROID] == session_id:
                self.delete(device_id);
                return True;
        return False;
    
    '''
    IDEとAndroidがコネクションを張る
    '''
    def connection(self, device_id, session_id):
        if self.is_device_id(device_id) is False:
            return False;
        data = devices[device_id];
        data.update({IDE:session_i});
        self._devices.update({device_id: data});
        return True;
    
    '''
    IDEとAndroidがコネクションを張っているのか
    '''
    def is_connection_ide(self, device_id):
        if self.is_device_id(device_id) is False:
            return False;
        if IDE in self._devices[device_id]:
            return True;
        return False;
    
    '''
    IDEとAndroidのコネクションを切断する

    '''
    def disconnection(self, device_id):
        if self.is_connection_ide(device_id) is False:
            return False;
        del self._devices[device_id][IDE];
        return True;

    '''
    user_idからdevice_idを求める

    '''
    def get_device_id(self, user_id):
        device_ids = []
        for device_id in self._devices:
            if self._devices[device_id][USER] == user_id:
                device_ids.append(device_id);
        return device_ids;

    '''
    user_idからdevice_idを求める

    '''
    def get_session_id(self, device_id):
        if self.is_device_id(device_id) is False:
            return None;
        return self._devices[device_id][ANDROID];



DEVICE_MANAGER = _DeviceManger()

if __name__ == "__main__":
    pass

