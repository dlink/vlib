#!/usr/local/bin/python

import re

def pretty_sql(sql, html=False):
    # Line break and color code:
    keywords = ['select', 'from', 'where', 'order by', 'group by',
                'having', 'limit', 'insert into', 'values']
    # Line break with indentation and color code:
    keywords2 = ['and', 'case', 'else', 'end', 'join', 'when']
    # Color code only:
    keywords3 = ['as', 'coalesce', 'on', 'or', 'then']

    keywords += [k.upper() for k in keywords]
    keywords2 += [k.upper() for k in keywords2]
    keywords3 += [k.upper() for k in keywords3]
    
    if html:
        indent = '&nbsp;' * 3
        nl = '<br \>'
        f1 = "<font color='blue'>"
        f1b= "<font color='green'>"
        f2 = '</font>'
    else:
        indent = ' ' * 3
        nl = '\n'
        f1 = ''
        f1b= ''
        f2 = ''
        
    sql = re.sub(r'\s+', ' ', sql)
    for k in keywords:
        sql = re.sub(r'\b(%s)\s+' % k,
                     r'%s%s\1%s%s%s' % (nl, f1, f2, nl, indent),
                     sql)
    for k in keywords2:
        sql = re.sub(r'\b(%s)\s+' % k,
                     r'%s%s%s\1%s ' % (nl, indent, f1b, f2),
                     sql)
    for k in keywords3:
        sql = re.sub(r'\b(%s)\s+' % k,
                     r'%s\1%s ' % (f1b, f2),
                     sql)
    return sql
