import simplejson as json 
from collections import namedtuple

def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)

def _json_object_hook(dobj):
    dobj['json_dict'] = dobj.copy()
    X =  namedtuple('X', dobj.keys(), rename=True)
    X.remove = lambda x: None
    return(X(*dobj.values()))
