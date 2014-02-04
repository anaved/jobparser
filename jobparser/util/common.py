#!/usr/bin/env python

import datetime
from job.models import STAB

def st2ab(state):
    return STAB.objects.filter(state = state.upper())[0].abbreviation

def ab2st(abbreviation):
    return STAB.objects.filter(abbreviation = abbreviation.upper())[0].state

def shorten(t):
    state = t[0].strip()
    if len(state) > 2:
        return st2ab(state)
    else:
        return state

def daysago(t):
    if t[0] == "":
        return datetime.date.today()
    daysback = int(t[0])
    return datetime.date.today() - datetime.timedelta(days=daysback)

def expminmax(t):
    if len(t) == 1 and int(t[0]) > 2:
        return None
    if t[0]=="" and int(t[1]) > 3:
        return None
    if t[1]=="" and int(t[0]) > 2:
        return None
    if int(t[0]) > 2:
        return None
    return True

def mmm(m):
    month_dict={
    'Jan':1,
    'Feb':2,
    'Mar':3,
    'Apr':4,
    'May':5,
    'Jun':6,
    'Jul':7,
    'Aug':8,
    'Sep':9,
    'Oct':10,
    'Nov':11,
    'Dec':12,
    }
    try:
         month=month_dict[m]
    except Exception as e:
         raise Exception("Could not match month string %s" % m)
    return month

def validate_date(t):
        if datetime.datetime.date(t) > datetime.datetime.date(datetime.datetime.now()) or t is None:
            return datetime.datetime.now()
        return t

def currtime():
    x= datetime.datetime.now()
    return [x.hour,x.minute,x.second]

def mm_dd_yyyy(t):    
    year = int(t[2])
    day = int(t[1])
    month = int(t[0])
    currtime()
    return validate_date(datetime.datetime(year, month, day,*currtime()))

def dd_mm_yyyy(t):
    year = int(t[2])
    day = int(t[0])
    month = int(t[1])
    return validate_date(datetime.datetime(year, month, day,*currtime()))

def mmm_dd(t):
    m = t[0]
    month = mmm(m)
    day = int(t[1])
    
    return validate_date(datetime.datetime(datetime.date.today().year, month, day,*currtime()))

def mm_dd(t):
    month = int(t[0])
    day = int(t[1])
    return validate_date(datetime.datetime(datetime.date.today().year, month, day))

def mmm_dd_yyyy(t):
    m = t[0]
    if m == "":
        return datetime.date.today()
    month = mmm(m)
    day = int(t[1])
    year = int(t[2])
    return validate_date(datetime.datetime(year, month, day,*currtime()))

def dd_mmm_yyyy(t):
    m = t[1]
    month = mmm(m)
    day = int(t[0])
    year = int(t[2])
    return validate_date(datetime.datetime(year, month, day,*currtime()))

def mm_dd_yy(t):    
    y = int(t[2])
    day = int(t[1])
    month = int(t[0])
    year = datetime.date.today().year/100*100+y
    return validate_date(datetime.datetime(year, month, day,*currtime()))

