# This test relies on a conf file that sets
# 
# database.engine = 'mssql'

import conf
import db

conf_ = conf.getInstance()
db_ = db.getInstance()
engine = conf_['database']['engine']
print(engine)
if engine == 'mysql':
    r = db_.query('SELECT * FROM customers limit 1')
else:
    r = db_.query('SELECT top(1) * FROM address')
print(r)
