"""
Implements MemBerDict, a nested dionary offering member attributes for faster access and improved aesthetic.
Standard Python dionaries can be converted to an MBD instance with convertDictToMBD. 
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

def convertDictToMBD(d):
    mbd = MBD()
    for key, value in d.iteritems():
        if isinstance(value, dict):
            setattr(mbd, key, convertDictToMBD(value))
        else:
            setattr(mbd, key, value)
    return mbd

def convertMBDtoDict(mbd):
    d = {}
    for key, value in mbd.iteritems():
        if isinstance(value, MBD):
            d[key] = convertMBDtoDict(value)
        else:
            d[key] = value
    return d

# print(convertDictToMBD({'valuation': {'output': 'Value', 'style': 'American', 'type': 'OTM', 'dimensions': {'expirations': {'max': 300, 'incr': 30, 'min': 30}, 'strikes': {'max': 110, 'incr': 0.5, 'min': 90}}, 'factors': {'spot_price': 100.25, 'interest_rate': 0.05, 'carry_rate': 0.05, 'volatility': 0.15}}}))
