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
    Android:アイテム（一列）をまるごと消去する
    '''
    def delete_android(self, device_id):
        del self._devices[device_id];

    '''
    IDE:アイテムの中の値（IDE）だけ消す
    '''
    def delete_ide(self, device_id):
        data = self._devices[device_id];
        if IDE in data:
            del data[IDE];
            self._devices[device_id] = data;
    
    '''
    指定したデバイスIDで、辞書の中身を消去する
    '''
    def delete(self, connection_type, device_id):
        if connection_type is ANDROID:
            print "delete_android  go";
            self.delete_android(device_id);
        else:
            self.delete_ide(device_id);

    '''
    指定したsession_idを消去する
    '''
    def delete_session_id(self, connection_type, session_id):
        for device_id in self._devices:
            if connection_type in self._devices[device_id]:
                if self._devices[device_id][connection_type] is session_id:
                    print "deletre_session_id", connection_type, session_id;
                    self.delete(connection_type, device_id);
                    return True;
        return False;
    
    '''
    IDEとAndroidがコネクションを張る
    '''
    def connection(self, device_id, session_id):
        if self.is_device_id(device_id) is False:
            return False;
        data = self._devices[device_id];
        data.update({IDE:session_id});
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
    def get_device_id_from_user_id(self, user_id):
        device_ids = []
        for device_id in self._devices:
            if self._devices[device_id][USER] == user_id:
                device_ids.append(device_id);
        return device_ids;

    '''
    androidのsession_idからdevice_idを求める

    '''
    def get_device_id_from_android(self, android):
        for device_id in self._devices:
            if self._devices[device_id][ANDROID] == android:
                return device_id;
        return None;

    
    '''
    device_idからsession_id(Android)を求める

    '''
    def get_session_android(self, device_id):
        if self.is_device_id(device_id) is False:
            return None;
        return self._devices[device_id][ANDROID];

    '''
    device_idからsession_id(IDE)を求める

    '''
    def get_session_ide(self, device_id):
        if self.is_device_id(device_id) is False:
            return None;
        return self._devices[device_id][IDE];

    def output(self):
        print self._devices;

DEVICE_MANAGER = _DeviceManger()

if __name__ == "__main__":
    pass

