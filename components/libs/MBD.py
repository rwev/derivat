"""
Implements MemBerDict, a nested dictionary offering member attributes for faster access and improved aesthetic.
Standard Python dictionaries can be converted to an MBD instance with convertDictToMBD. 
"""

from collections import OrderedDict

class MBD(OrderedDict):
    _closed = False
    def _close(self):
        self._closed = True
        for key, val in self.items():
            if isinstance(val, MBD):
                val._close()
    def _open(self):
        self._closed = False
    def __missing__(self, key):
        if self._closed:
            raise KeyError
        value = self[key] = MBD()
        return value
    def __getattr__(self, key):
        if key.startswith('_'):
            raise AttributeError
        return self[key]
    def __setattr__(self, key, value):
        if key.startswith('_'):
            self.__dict__[key] = value
            return
        self[key] = value

def convertDictToMBD(dict):
    mdb = MBD()
    for k in dict.keys():
        if type(dict[k]) == dict:
            mdb = convertDictToMBD(dict[k])
        else:
            setattr(mdb, k, dict[k])
    return mdb

def convertMBDtoDict(mdb):
    dict = {}
    for k in mdb.keys():
        if type(mdb[k]) == dict:
            mdb = convertMBDtoDict(mdb[k])
        else:
            dict[k] = mdb[k]
    return dict
