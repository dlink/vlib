#!/usr/local/bin/python

import os
from datetime import datetime

from functools import update_wrapper

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

def uniqueId(with_millisec=False):
    """Return system time to the millisec as set of numbers"""
    d = str(datetime.now())
    if with_millisec:
        return d[0:4]+d[5:7]+d[8:10]+'-'+d[11:13]+d[14:16]+d[17:19]+'-'+d[20:]
    else:
        return d[0:4]+d[5:7]+d[8:10]+'-'+d[11:13]+d[14:16]+d[17:19]

def shift(alist):
    '''Shift the first element off of an array, and return it'''
    return alist.pop(0)

class Str2DateError(Exception): pass

def str2datetime(s, format="%Y-%m-%d %H:%M:%S"):
    """Convert str in the form of "2010-11-11 17:39:52" or
                                  "2010-11-11"          to a
       datetime.datetime Object
    """
    from datetime import datetime
    if len(s) == 10:
        s += ' 00:00:00'
    try:
        return datetime.strptime(s, format)
    except Exception as e:
        raise Str2DateError('Unable to convert "%s" to datetime: %s: %s'
                            % (s, e.__class__.__name__, e))

def str2date(s):
    """Convert str in the form of "2010-11-11" to a
       datetime.date Object
    """
    from datetime import date
    try:
        return date(*list(map(int, (s[0:4], s[5:7], s[8:10]))))
    except Exception as e:
        raise Str2DateError('Unable to convert "%s" to datetime: %s: %s'
                            % (s, e.__class__.__name__, e))

def format_datetime(d, with_seconds=False, format=None):
    '''Given a datetime object
       Return formated String as follows:

          Format: None   : 11/22/2013 01:46[:00] am
                  ISO8601: 2013-11-21T01:46:00-05:00 (EST)
    '''
    try:
        if format == 'ISO8601':
            return d.strftime("%Y-%m-%dT%H:%M:%S-05:00")
        elif format == 'RFC-2822':
            return d.strftime('%a, %d %b %Y %H:%M:%S -0500') # zone=EST
        elif with_seconds:
            return d.strftime("%m/%d/%Y %I:%M:%S %p").lower()
        else:
            return d.strftime("%m/%d/%Y %I:%M %p").lower()
    except Exception as e:
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
    
    keys, values = list(d.keys()), list(d.values())
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
        if X and isinstance(X[0], (list, tuple)):
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
    return o.strip() # strip off final \n so we can print it

    
def any_in(items, thing):
    for i in items:
        if i in thing:
            return True
    return False

def list2csv(data):
    '''Given a Table of data as a LIST of LISTs
       Return in CSV format as a STR
    '''
    o = ''
    for row in data:
        row2 = []
        for c in row:
            if isinstance(c, str) and any_in(',"\'', c):
                # put quotes on strings
                row2.append('"%s"' % c)
            else:
                row2.append(c)
        o += ','.join(map(str, row2)) + '\n'
    return o
            

def lazyproperty(fn):
    '''A decorator that computes a property variable and then caches.
    http://stackoverflow.com/questions/3012421/python-lazy-property-decorator
    '''
    attr_name = '_lazy_' + fn.__name__
    @property
    def _lazyproperty(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazyproperty

def rev_move(src, dst, max_revs=20, copy=False, debug=False):
    """Rev destination file, if it exists, before moving src to dst.
       Multiple calls to the same dst file might create this set of files:
             tanner
             tanner_1
             tanner_2
             tanner_3
    """
    import shutil

    #debug = True

    import os

    # use absolute path
    dst = os.path.realpath(dst)

    # append filename to destination if necesary.
    if os.path.isdir(dst):
        sname = os.path.basename(src)
        dst += '/%s' % sname

    # debug
    if debug:
        print("src:", src)
        print("dst:", dst)
    if not os.path.exists(src):
        raise Exception('utils.revmove: Source %s does not exist' % src)

    # rev dest file(s) if necessary.
    if os.path.exists(dst):
        import re
        ddirname = os.path.dirname(dst)
        dname    = os.path.basename(dst)
        pattern = re.compile('%s(_(\d+)$|$)' % dname)

        # gather up all the name and name_n files:
        revfiles = {}
        for file in os.listdir(ddirname):
            match = pattern.match(file)
            if match:
                num = match.group(2)
                num = int(num) if num else None
                if num < max_revs and max_revs != 0:
                    revfiles[num] = file
                else:
                    # purge files with revs greater than max_revs:
                    killfile = "%s/%s" % (ddirname, file)
                    if debug: print('killing file: %s' % killfile)
                    if os.path.isdir(killfile):
                        shutil.rmtree(killfile)
                    else:
                        os.remove(killfile)

        # move them to new revs:
        file_base = dname + '_'
        for i in sorted(list(revfiles.keys()), reverse=True):
            j = int(i) + 1 if i else 1
            oldfile = "%s/%s" % (ddirname, revfiles[i])
            newfile = "%s/%s_%s" % (ddirname, dname, j)
            if debug:
                print("move %s %s" % (oldfile, newfile))
            try:
                shutil.copy2(oldfile, newfile)
            except Exception as e:
                shutil.copyfile(oldfile, newfile)
    if debug:
        cmd = 'copy' if copy else 'move'
        print("%s %s %s" % (cmd, src, dst))

    if os.path.abspath(src) == os.path.abspath(dst):
        return
    try:
        shutil.copy2(src, dst)
    except Exception as e:
        shutil.copyfile(src, dst)
    if not copy:
        os.remove(src)

def is_int(s):
    '''Return True if s can be converted to an int'''
    try:
        int(s)
        return True
    except ValueError:
        return False

def strip_html(html):
    if isinstance(html, str):
        import re
        return re.sub('<[^>]*>', '', html).strip()
