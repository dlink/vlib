#!/usr/local/bin/python

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

def echoif(switch):
    '''Decorator - calls echoized
       eq.:
         @echoif(DEBUG_CALLSTACK)
         class OrderPricing(objec):
            ...
    '''
    if switch:
        return echoized
    return lambda unchanged: unchanged


def echoized(func_or_cls):
    """Decorator
       Echos a function's signature prior to evaluating it, of does the
        same for all methods of a class. 

        ISSUES:
          If used on a single method of a class, it fails to identify the
          arg names, and self is not distinguished from other args.
          
          (or in conjunction with @cached)
          
        eq.:
          op = OrderPricing()
          op = echoized(OrderPricing)()

          e = Editions(nid=nid)
          e = echoized(Editions)(nid=nid)
    """
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

def str2datetime(s, format="%Y-%m-%d %H:%M:%S"):
    """Convert str in the form of "2010-11-11 17:39:52" to a
       datetime.datetime Object
    """
    from datetime import datetime
    try:
        return datetime.strptime(s, format)
    except Exception, e:
        raise Str2DateError('Unable to convert "%s" to datetime: %s: %s'
                            % (s, e.__class__.__name__, e))

def str2date(s):
    """Convert str in the form of "2010-11-11" to a
       datetime.date Object
    """
    from datetime import date
    try:
        return date(*map(int, (s[0:4], s[5:7], s[8:10])))
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

def table2csv(data):    
    '''Give a LIST or TUPLE
       Return: A CSV table as STRING or the input data if not LIST or TUPLE
    '''
    o = ''
    if isinstance(data, (list, tuple)):
        if isinstance(data[0], (list, tuple)):
            for row in data:
                o +=  ",".join(map(str, row))
                o += '\n'
        else:
            o += "\n".join(map(str, data))
    else:
        return data
    return o

def formatdict(d, width=console_width(), indent=0, keylen=0, color=False):
    '''Recursively format contents of dictionaries in sorted tabular order.
       Optionally a certain width, indented, and/or a specific key length.

       >>> utils.formatdict(batch_item)
               active: 1
             batch_id: 3250
             on_press: None
             order_id: 2007372
            page_list: None
                  qty: 2
         removed_date: None
    '''

    key_color = lightgreen
    val_color = lambda v: \
        lightcyan(v) if isinstance(v, (int, bool, type(None))) or \
        str(v).isdigit() else darkcyan(v)
    
    keys, values = d.keys(), d.values()
    key_lens = [len(str(k)) for k in keys]
    val_lens = [len(str(v)) for v in values]
    if not keylen:
        keylen = max(key_lens or [0])
    total_len = sum(key_lens + val_lens) + len(key_lens) * 4
    keys.sort()
    out = ''
    if total_len < width:
        for k in keys:
            if isinstance(d[k], dict):
                d[k] = formatdict(d[k], width - keylen, keylen, 
                                  color=color).rstrip()
        if color:
            out += '{%s}\n' % ', '.join(['%s: %s' % (key_color(k), 
                                                     val_color(d[k]))
                                         for k in keys])
        else:
            out += '{%s}\n' % ', '.join(['%s: %s' % (k, d[k]) for k in keys])
        return out
    if indent:
        out += '\n'
    for k in keys:
        if isinstance(d[k], dict):
            key = str(k).rjust(keylen)
            if color:
                key = key_color(key)
            out += '%s%s: ' % (' ' * indent, key)
            out += formatdict(d[k], width - keylen, keylen + indent + 2,
                              color=color)
        elif isinstance(d[k], list):
            key = str(k).rjust(keylen)
            if color:
                key = key_color(key)
            out += '%s%s: ' % (' ' * indent, key)
            ind = 0
            for v in d[k] or ['']:
                out += '%s- %s\n' % (' ' * ind, val_color(v) if color else v)
                ind = keylen + indent + 2
        else:
            key = str(k).rjust(keylen)
            val = d[k]
            if color:
                key = key_color(key)
                val = val_color(val)
            line = '%s: %s\n' % (key, val)
            out += word_wrap(line, width, indent, keylen + indent + 2)
    return out

def word_wrap(string, width, ind1=0, ind2=0):
    '''Wrap long lines of text.
       Prefer spaces or non-alpha-numeric break points.

            ind1 = initial indentation
            ind2 = hanging indentation
    '''    
    lines = (' ' * ind1 + string).split('\n')
    newstring = ''
    for string in lines:
        if len(string) > width:
            for _ in range(10000): 
                # find position of nearest whitespace char to the left of 'width'
                marker = width - 1
                while not string[marker].isspace() and marker >= 0:
                    marker -= 1
                if marker + 1 == ind2:  # no space breaks: try non-word char
                    marker = width - 1
                    while string[marker].isalnum() and marker >= 0:
                        marker -= 1
                    marker += 1         # put break char at end of line
                    if marker == ind2:  # no nice break points: break on char
                        marker = width - 1
                # no room to wrap - bail out
                if len(string) > marker:   # this breaks things sometimes
                    break   # relying on counter to avoid inf looping instead
                # remove line from original string and add it to the new string
                newstring += string[:marker] + '\n'
                string = ' ' * ind2 + string[marker:].lstrip(' ')
                # break out of loop when finished
                if len(string) <= width:
                    break
        newstring += string + '\n'
    return newstring[:-1]

def valid_email(email):
    '''Given an email address
       Return whether it is in valid format as BOOLEAN
    '''
    import re
    if email==None:
        return False

    regex1 = r"^[a-zA-Z0-9._%+-]+\@[a-zA-Z0-9._%-]+\.[a-zA-Z]{2,}$",
    regex2 = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:[a-zA-Z]{2}|com|org|net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum)\b"

    return re.match(regex2, email) != None

def pretty(X):
    '''Return X formated nicely for the console'''
    o = ''
    if isinstance(X, (list, tuple)):
        if isinstance(X[0], (list, tuple)):
            for row in X:
                o +=  ",".join(map(str, row)) + '\n'
        else:
            o += "\n".join(map(str, X)) + '\n'
    elif isinstance(X, dict):
        keys = sorted(X.keys())
        for k in keys:
            o +=  "%s: %s" % (k, X[k]) + '\n'
    else:
        o += str(X)
    return o

    
