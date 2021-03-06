#!/usr/local/bin/python

import re


def sql_pretty(sql, lowercase_kw=True, html=False):
    '''Return formated SQL String'''

    # Line break and color code 1:
    keywords = ['select', 'from', 'where', 'order by', 'group by',
                'having', 'limit', 'insert into', 'values']

    # Line break with indentation and color code 2:
    keywords2  = ['and', 'case', 'else', 'end', 'when']
    keywords2b = [r'(left |right )?(inner |outer )?join',]

    # Color code only 3:
    keywords3 = ['as', 'coalesce', 'on', 'or', 'then']

    if html:
        indent = '&nbsp;' * 3
        nl = '<br \>\n'
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
        k2 = k if lowercase_kw else '\\1'
        sql = re.sub(r'\s*\b(%s)\s+' % k,
                     r'%s%s%s%s%s%s' % (nl, f1, k2, f2, nl, indent),
                     sql, 0, re.IGNORECASE)
    for k in keywords2:
        k2 = k if lowercase_kw else '\\1'
        sql = re.sub(r'\b(%s)\s+' % k,
                     r'%s%s%s%s%s ' % (nl, indent, f1b, k2, f2),
                     sql, 0, re.IGNORECASE)
    for k in keywords2b:
        sql = re.sub(r'\b(%s)\s+' % k,
                     r'%s%s%s\1%s ' % (nl, indent, f1b, f2),
                     sql, 0, re.IGNORECASE)
    for k in keywords3:
        k2 = k if lowercase_kw else '\\1'
        sql = re.sub(r'\b(%s)\s+' % k,
                     r'%s%s%s ' % (f1b, k2, f2),
                     sql, 0, re.IGNORECASE)

    # Second pass - indent subqueries
    # (To really do this correctly we need a full sql parse)
    sql2 = ''
    ind = ''
    for i, x in enumerate(sql.split(nl)):
        # Remove blank line from the top
        if i == 0 and x == '':
            continue
        # Start indenting after the second SELECT
        if 'select' in x and i > 1:
            ind = indent*2
        sql2 += '%s%s%s' % (ind, x.rstrip(), nl)
        # Stop indenting after the join's ON statement (hokey I know)
        if re.search(r'\) %sas%s \w+ %son%s' % (f1b, f2, f1b, f2), x):
            ind = ''
    return sql2

def pretty_sql(sql, lowercase_kw=True,  html=False):
    '''Same thing as sql_pretty()'''

    return sql_pretty(sql, lowercase_kw, html)

