def isNone(obj, key = None):
  if type(obj) == dict and key != None:
    if not obj.has_key(key): return True
    if isNone(obj[key]): return True
  if obj == None: return True
  if obj == "": return True
  if type(obj) == list and len(obj) == 0: return True
  if type(obj) == dict and len(obj.keys()) == 0: return True
    