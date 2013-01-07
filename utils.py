#!/usr/local/bin/python
# $Id: utils.py 2893 2012-01-04 16:05:14Z rlowe $

import os
from datetime import datetime

from functools import update_wrapper
from colors import *

class MissingArguments(Exception): pass

def validate_num_args(s, num_args, args):
    if len(args) < num_args:
        pluralization = 's'
        if num_args == 1: 
            pluralization = ''
        error_msg = '%s takes %s argument%s.' % (s, num_args, pluralization)

        if not args:
            error_msg += '  None given.'
        else:
            error_msg += '  Only %s given: %s' % (len(args), ", ".join(args))
        raise MissingArguments(error_msg)

def console_width():
    """Get the width of the console screen (if any)."""
    try:
        return int(os.environ["COLUMNS"])
    except (KeyError, ValueError):
        pass

    try:
        # Call the Windows API (requires ctypes library)
        from ctypes import windll, create_string_buffer
        h = windll.kernel32.GetStdHandle(-11)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            import struct
            (bufx, bufy,
             curx, cury, wattr,
             left, top, right, bottom,
             maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            return right - left + 1
    except:
        pass

    # Parse the output of stty -a
    if os.isatty(1):
        import re
        out = os.popen("stty -a").read()
        m = re.search(r"columns (\d+);", out)
        if m:
            return int(m.group(1))

    # sensible default
    return 80


def echoized(func_or_cls):
    ''' Echos a function's signature prior to evaluating it, of does the
        same for all methods of a class. 

        ISSUES:
          If used on a single method of a class, it fails to identify the
          arg names, and self is not distinguished from other args.
          
          (or in conjunction with @cached)
    '''
    from inspect import getargspec, isclass, ismethod
    def newf(*args, **kwds):
        'Echos function signature'
        try:
            spec = getargspec(f)
        except Exception, e:
            spec = getargspec(f.__call__)
        sargs = list(args)
        cls = ''
        # pull the class name in front for instance and class methods
        if spec.args:       
            arg0 = spec.args.pop(0)
            if arg0 == 'self':
                cls = sargs.pop(0).__class__.__name__
            elif arg0 == 'cls':
                cls = sargs.pop(0).__name__
        s = ['%s=%s' % (sa, a) for sa, a in zip(spec.args, sargs)]
        s.extend(map(str, sargs[len(spec.args):]))           # *args
        s.extend('%s=%s' % (k, v) for k, v in kwds.items())  # **kwds
        print colorcall((f.__name__, cls), *s)
        return f(*args, **kwds)
    # if class, add echoizing to all methods in class
    if isclass(func_or_cls):
        cls = func_or_cls
        for name in cls.__dict__:
            item = getattr(cls, name)
            if ismethod(item) or hasattr(item, '__call__'):
                setattr(cls, name, echoized(item))
        return cls
    f = func_or_cls
    if f.__doc__:
        newf.__doc__ = '\n'.join([f.__doc__, newf.__doc__])
    # use new composite docstring instead of just orig func's
    return update_wrapper(newf, f, assigned=('__module__', '__name__'))

def uniqueId(with_millisec=False):
    """Return system time to the millisec as set of numbers"""
    d = str(datetime.now())
    if with_millisec:
        return d[0:4]+d[5:7]+d[8:10]+'-'+d[11:13]+d[14:16]+d[17:19]+'-'+d[20:]
    else:
        return d[0:4]+d[5:7]+d[8:10]+'-'+d[11:13]+d[14:16]+d[17:19]

def shift(alist):
    return alist.pop(0)

class Str2DateError(Exception): pass

def str2datetime(s):
    """Convert str in the form of "2010-11-11 17:39:52" to a                    
       datetime.datetime Object                                                 
    """
    from datetime import datetime
    try:
        return datetime(*map(int, (s[0:4], s[5:7], s[8:10], s[11:13],
                                   s[14:16], s[17:19])))
    except Exception, e:
        raise Str2DateError('Unable to convert "%s" to datetime: %s: %s'
                            % (s, e.__class__.__name__, e))

def format_datetime(d, with_seconds=False):
    '''Given a datetime object
    Return a string in the form of "mm/dd/yyyy hh:mm (am/pm)"
    '''
    try:
        if with_seconds:
            return d.strftime("%m/%d/%Y %I:%M:%S %p").lower()
        else:
            return d.strftime("%m/%d/%Y %I:%M %p").lower()
    except Exception, e:
        return d

def format_date(d):
    '''Given a datetime object
    Return a string in the form of "mm/dd/yyyy"
    '''
    return d.strftime("%m/%d/%Y")

