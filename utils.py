import os
import calendar
from datetime import datetime, date


def utc(x, totimestamp=False):
    if totimestamp == False:
        return timeformat(datetime.utcfromtimestamp(x), 'BOTH')
    else:
        d = datetime(*x)
        epoch = datetime(1970,1,1)
        return int((d - epoch).total_seconds())

def timeformat(x=datetime.now(), typ='DATE'):
    if type(x) != type(datetime.now()):
        x = datetime(x)
    if typ == 'DATE':
        return x.strftime('%Y-%m-%d')
    elif typ =='HOUR':
        return x.strftime('%H:%M:%S')
    elif typ=='BOTH':
        return x.strftime('%Y-%m-%d')+'%20'+x.strftime('%H:%M:%S')
