
from json import JSONEncoder
from datetime import datetime
from bson.objectid import ObjectId
from collections import OrderedDict

class MyJsonEncode(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, set):
            return JSONEncoder.default(self, [i for i in o])
        elif isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, OrderedDict):
            return '{' + ','.join([self.encode(k) + ':' + self.encode(v) for (k, v) in o.iteritems()]) + '}'
        else:
            return JSONEncoder.default(self, o)
