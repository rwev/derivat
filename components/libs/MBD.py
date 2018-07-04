"""
Implements MemBerDict, a nested dictionary offering member attributes for faster access and improved aesthetic.
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