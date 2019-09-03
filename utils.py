import os
import calendar
from datetime import datetime, date
import time

def utc(x = time.time(), totimestamp=False, format = 'BOTH'):
    if totimestamp == False:
        return timeformat(datetime.utcfromtimestamp(x), format)
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
    else:
        return x.strftime(typ)


if __name__ == '__main__':
    print(utc(format='HOUR'))
