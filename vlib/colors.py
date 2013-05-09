#!/usr/bin/env python

from string import digits, punctuation
from odict import odict

COLORS = odict({'darkred'     : '\033[0;31m',
                'darkgreen'   : '\033[0;32m',
                'darkyellow'  : '\033[0;33m',
                'darkblue'    : '\033[0;34m',
                'darkmagenta' : '\033[0;35m',
                'darkcyan'    : '\033[0;36m',
                'darkgray'    : '\033[0;30m',
                'lightgray'   : '\033[0;38m',
                'lightred'    : '\033[31;1m',
                'lightgreen'  : '\033[32;1m',
                'lightyellow' : '\033[33;1m',
                'lightblue'   : '\033[34;1m',
                'lightmagenta': '\033[35;1m',
                'lightcyan'   : '\033[36;1m',
                'white'       : '\033[37;1m',
                'reset'       : '\033[0m',
                # abbreviations
                'dr'          : '\033[0;31m',
                'dg'          : '\033[0;32m',
                'dy'          : '\033[0;33m',
                'db'          : '\033[0;34m',
                'dm'          : '\033[0;35m',
                'dc'          : '\033[0;36m',
                'dgy'         : '\033[0;30m',
                'lgy'         : '\033[0;38m',
                'lr'          : '\033[31;1m',
                'lg'          : '\033[32;1m',
                'ly'          : '\033[33;1m',
                'lb'          : '\033[34;1m',
                'lm'          : '\033[35;1m',
                'lc'          : '\033[36;1m',
                'w'           : '\033[37;1m',
                'r'           : '\033[0m'})

BG_COLORS = odict({'black'  : '\033[40m',
                   'red'    : '\033[41m',
                   'green'  : '\033[42m',
                   'yellow' : '\033[43m',
                   'blue'   : '\033[44m',
                   'magenta': '\033[45m',
                   'cyan'   : '\033[46m',
                   'gray'   : '\033[47m'})

STYLES = odict({'bold'     : '\033[1m',
                'underline': '\033[4m',
                'blink'    : '\033[5m',
                'reverse'  : '\033[7m',
                'concealed': '\033[8m'})

for c in COLORS:
    #globals()[c] = lambda t, c=c: COLORS.reset + COLORS[c] + unicode(t) + COLORS.reset
    globals()[c] = lambda t, c=c: COLORS.reset + COLORS[c] + str(t) + COLORS.reset


def colorize(s, **kwds):
    attrs =  COLORS.copy()
    attrs.update(kwds)
    return s.format(**attrs)


def decolorize(s):
    for c in COLORS.values():
        s = s.replace(c, '')
    return s


def colorcall(func_method, *args):
    CLASSNAME = lightcyan
    OP        = lightred
    FUNCNAME  = darkcyan
    ARGNAME   = lightgray
    ARGVALUE  = white
    s = ''
    if isinstance(func_method, tuple):
        f, classname = func_method
        s = CLASSNAME(classname) + OP('.')
    else:
        f = func_method
    s += FUNCNAME(f) + '('
    args = list(args)
    while args:
        a = args.pop(0)
        if '=' in a:
            n, v = a.split('=')[:2]
            s += ARGNAME(n) + OP('=') + ARGVALUE(v)
        else:
            s += ARGVALUE(a)
        if args:
            s+= OP(', ')
    s += ')'
    return s

def label(l, s):
    l, s = map(str, (l, s))
    if '\033' not in l:
        l = lightblue(l)
    if '\033' not in s:
        s = lightyellow(s)
    return l + white(' = ') + s

