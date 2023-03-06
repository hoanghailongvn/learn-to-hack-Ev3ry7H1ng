import datetime
import hashlib

def get_random(chars=20):
    return hashlib.md5(str(datetime.datetime.now()).encode() + b"SeCReT?!").hexdigest()[:chars]