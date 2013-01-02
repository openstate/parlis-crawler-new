import sys
import os
import re
import errno
import datetime
import hashlib

def date_to_parlis_str(date):
    return date.strftime('%Y-%m-%d')

def make_md5(text):
    return hashlib.md5(text).hexdigest()

# from http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
def mkdirs(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise