#!/usr/local/bin/python

import re

def pretty_sql(sql, html=False):
    # Line break and color code 1:
    keywords = ['select', 'from', 'where', 'order by', 'group by',
                'having', 'limit', 'insert into', 'values']

    # Line break with indentation and color code 2:
    keywords2 = ['and', 'case', 'else', 'end',
                 r'(left |right )?(inner |outer )?join',
                 'when']

    # Color code only 3:
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
        sql = re.sub(r'\s*\b(%s)\s+' % k,
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
