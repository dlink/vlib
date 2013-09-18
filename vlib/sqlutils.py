#!/usr/local/bin/python

import re

def pretty_sql(sql, html=False):
    # Line break and color code:
    keywords = ['select', 'from', 'where', 'order by', 'group by',
                'having', 'limit', 'insert into', 'values']
    # Line break with indentation and color code:
    keywords2 = ['and', 'case', 'else', 'end', 'left join', 'join', 'when']
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

    # Second pass - indent subqueries
    # (To really do this correctly we need a full sql parse)
    sql2 = ''
    ind = ''
    for i, x in enumerate(sql.split(nl)):
        # Start indenting after the second SELECT
        if 'select' in x and i > 1:
            ind = indent*2
        sql2 += '%s%s%s' % (ind, x, nl)
        # Stop indenting after the join's ON statement (hokey I know)
        if re.search(r'\) %sas%s \w+ %son%s' % (f1b, f2, f1b, f2), x):
            ind = ''
    return sql2
