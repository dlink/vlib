# $Id: datatable.py 38 2010-06-02 17:06:10Z rlowe $

import re
import sys
import types

DEBUG = 0
DEBUG_SQL = 0
WRITEBACK = 1

class DataTableError (Exception): pass

class DataTable(object):
    '''Database table abstraction Layer
    '''

    def __init__ (self, db, tablename):
        '''Instantiate a DataTable.
        '''
        self.db = db
        self.tablename = tablename

        #self.autocommit = autocommit

        self.columns   = [] #self.table_columns 
        self.filters   = []
        self.group_by  = []
        self.order_by  = []
        self.limit     = ''
        self.debug     = DEBUG
        self.debug_sql = DEBUG_SQL
        self.writeback = WRITEBACK

    #def setAutocommit (self, state):
    #   '''Turn autocommit on (1) or off (0). Default is on.  See __init__()'''
    #    self.autocommit = state
    
    def startTransaction(self):
        self.db.startTransaction()
        
    def rollback(self):
        self.db.rollback()
        
    def commit(self):
        '''Commit Transaction Bock.
           Also see self.autocommit.
        '''
        self.db.commit()

    def setWriteBack (self, switch):
        '''Set writeback switch.
        0 - do not write data to disk
        1 - writeback data to disk  (DEFAULT)

        Allows calling program to turn off writeback, for Debuging.
        Example:
            if not WRITEBACK: myDataTable.setWriteBack(0)
        '''
        if self.debug:
            print __name__, self.tablename, "setWriteBack (%s)" % switch
        self.writeback = switch
        
    def setColumns (self, columns):
        '''Set User defined column list to be used SELECT CLAUSE of
        subsequent SQL statements.

        The columns arg can be either a string or a list of strings.
        
        Examples: dobj.setColumns ("username")
                  dobj.setColumns (["username", "lastname"])
        '''
        
        if isinstance(columns, str):
            columns = [columns]
        self.columns = columns
        
    def setFilters (self, filters=None):
        '''Set filters to be used in WHERE CLAUSES of
        subsequent SQL SELECT and UPDATE statements.

        The filters arg can be either a string or a list of strings.
        
        Examples: dobj.setFilters ("email like 'fred%'")
                  dobj.setFilters (["email like 'fred%'", "name = 'Fred'"])
                  dobj.setFilters ({'email': 'fred@foo.bar', 'name': 'Fred'})
        '''

        if isinstance(filters, (str, unicode)):
            filters = [filters]
        elif isinstance(filters, dict):
            filters2 = []
            for k,v in filters.items():
                if v:
                    filters2.append("%s = '%s'" % (k, sqlize(v)))
                else:
                    filters2.append("%s is null" % k)
            filters = filters2
        self.filters = filters

    def setOrderBy (self, order_by):
        '''Set list of columns used in ORDER BY CLAUSE of
        subsequent SQL SELECT statements.
        '''
        
        if isinstance(order_by, str):
            order_by = [order_by]
        self.order_by = order_by

    def setGroupBy (self, group_by):
        '''Set list of columns used in GROUP BY CLAUSE of
        subsequent SQL SELECT statements.
        '''        
        if isinstance(group_by, str):
            group_by = [group_by]
        if isinstance(group_by, int):
            group_by = [str(group_by)]
        self.group_by = group_by
        
    def setLimit (self, limit):
        '''Set value of LIMIT CLAUSE in subsequent SQL SELECT statements.'''
        self.limit = limit
        
    def getTable (self):
        '''Performs an SQL SELECT statement. 

        Use setColumns(), setFilters(), setOrderBy(), and setLimits()
        prior to calling.
        
        Example: from datatable import DataTable
                 users = DataTable('user')
                 users.setColumns (['name', 'color'])
                 users.setFilters (['group_id = 200', "status = 'A'"])
                 recordset = users.getTable()

        Which is equivalent to:
            select name, color from user where group_id = 200 and status = 'A'
            
        Returns tuple sets as a list of Dictionaries
            [ { 'name': 'Fred', 'color': 'red'},
              { 'name': 'Barbara', 'color': 'blue'} ]
        '''
        
        if self.debug: print __name__, self.tablename, "getTable ()"
        
        table = self.db.query(self._getSQL())
        return table

    def _getSQL (self):
        '''Build SQL statement based on values of columns, filters, etc.
        Used by getTable().
        '''

        self.aliases = []
        if not self.columns:
            self.columns = ['*']
        select = 'select %s' % ', '.join(self.columns)
        From   = 'from %s' % self.tablename
        where  = ''
        if self.filters:
            where = 'where %s' % ' and '.join(self.filters)
        group_by = ''
        if self.group_by:
            group_by = 'group by %s' % ', '.join(self.group_by)
        order_by = ''
        if self.order_by:
            order_by = 'order by %s' % ', '.join(self.order_by)
        limit = ''
        if self.limit:
            limit = 'limit %s' % self.limit
        sql = '%s %s %s %s %s %s' % (select, From, where, group_by, order_by, 
                                     limit)
        if self.debug_sql: print __name__, self.tablename, "SQL:\n ", sql
        return sql;


    def replaceRow (self, record):
        return self.insertRow(record, 1)
        
    def insertRow (self, record, replace_cmd = 0):
        '''Performs an SQL INSERT statement.
        (or SQL REPLACE if replace_cmd = 1)

        Uses dictionary record passed in for column and values

        Example:
           user = { 'name': 'Ralph', 'color': 'blue' }
           users = DataTable('user')
           users.insertRow(user)

        Which is equivalent to:
           insert into user (name, color) values ('Ralph', 'blue')

        Returns id of row inserted.
        '''

        sql_cmd = 'insert'
        if replace_cmd: sql_cmd = 'replace'
        if DEBUG: print __name__, self.tablename, '%sRow()' % sql_cmd
        if len(record) < 1:
            raise DataTableError ('Record to insert is blank')
        columnlist = []
        valuelist  = []
        for column in record:
            columnlist.append(column)
            valuelist.append(sqlize(record[column]))

        valuelist2 = []
        for value in (valuelist):
            if value is None:
                valuelist2.append('null')
            elif isinstance(value, (int, long, float)):
                valuelist2.append(str(value))
            else:
                valuelist2.append("'%s'" % value)
        
        sql = "%s into %s (%s) values (%s)" % (
            sql_cmd,
            self.tablename,
            ', '.join(columnlist),
            ', '.join(valuelist2))
            #', '.join(map(lambda x: "'%s'" % x, valuelist)))
            #', '.join(["'%s'" % x for x in valuelist])
            
        if self.debug_sql: print __name__, self.tablename, "SQL:\n ", sql
        id = 0
        try:
            if self.writeback:
                self.db.query(sql)
                #id = cursor.insert_id() # MySQLdb 1.0.1
                id = self.db.lastrowid    # MySQLdb 1.2.1
                #self.db.commit()        # Needed for MySQLdb 1.2.1
                #if self.autocommit: 
                #    self.db.commit() 
                
        except Exception, e:
            raise DataTableError (
                "Unable to insert row into %s: %s" % (self.tablename, e))
        return id

    def updateRows (self, record):
        '''Performs an SQL UPDATE statement.

        Use setFilters() prior to calling.  Or will raise Error.

        Example:
            modified_columns = { "color": "yellow", "location": "nyc" }
            users = DataTable('user')
            users.setFilters ( ["date >= '2007-06-01'", "status = 'A'" ] )
            users.updateRows (modified_fields)

        Which is equivalent to:
            update user set color = 'yellow', location = 'nyc'
                 where date >= '2007-06-01' and status = 'A'

        Returns number of rows inserted.
        '''
        
        if self.debug:
            print __name__, self.tablename, "updateRows (%s)" % record
        if len(record) < 1:
            raise DataTableError ('Record to insert is blank')

        # set_statment = "set col1 = 'mojo', col2 = 'jojo', ..."
        setters = []
        for column, value in record.items():
            if value is None:
                setters.append("%s = NULL" % column)
            else:
                setters.append("%s = '%s'" % (column, sqlize(value)))
        set_statement = "set %s" % ', '.join(setters)

        where  = ''
        if self.filters:
            where = 'where %s' % ' and '.join(self.filters)
        else:
            raise DataTableError(
                'Unable to updateRow (%s).  No filter specified' %record)
        
        sql = "update %s %s %s" % (
            self.tablename,
            set_statement,
            where)

        if self.debug_sql: print __name__, self.tablename, "SQL:\n ", sql
        rowcount = 0
        try:
            if self.writeback:
                rowcount = self.db.query(sql)
                #if self.autocommit:
                #    self.db.commit()
        except Exception, e:
            raise DataTableError (
                "Unable to update row into %s: %s" % (self.tablename, e))
        return rowcount
    
    def deleteRows (self):
        '''Performs an SQL DELETE statement.

        Use setFilters() prior to calling.  Or will raise Error.

        Example:
            users = DataTable('user')
            users.setFilters ( ["date >= '2007-06-01'", "status = 'A'" ] )
            users.deleteRows ()

        Which is equivalent to:
            delete from user where date >= '2007-06-01' and status = 'A'

        Returns number of rows deleted.
        '''
        
        if self.debug:
            print __name__, self.tablename, "deleteRows ()"

        where  = ''
        if self.filters:
            where = 'where %s' % ' and '.join(self.filters)
        else:
            raise DataTableError(
                'Unable to deleteRows ().  No filter specified')
        
        sql = "delete from %s %s" % (
            self.tablename,
            where)

        if self.debug_sql: print __name__, self.tablename, "SQL:\n ", sql
        rowcount = 0
        try:
            if self.writeback:
                rowcount = self.db.query(sql)
                #if self.autocommit:
                #    self.db.commit()
        except Exception, e:
            raise DataTableError (
                "Unable to delete row from %s: %s" % (self.tablename, e))
        return rowcount
    
    def columnDefs(self):
        '''Read table metadata information from database
        return LIST of the form
        [{'name': 'adoption_id', 'type': 'int(10) unsigned'},
         {'name': 'professor_id', 'type': 'int(10) unsigned'}, ... ]
        '''
        
        try:
            table = self.db.query('show columns from %s' % self.tablename)
        except Exception, e:
            raise DataTableError(e)

        #$table_alias = self.getAlias() - table alias to come
        columnDefs = []
        table_columns = []
        column_types  = []
        for row in table:
            columnDefs.append({'name': row['Field'],
                               'type': row['Type']})
            table_columns.append(row['Field'])
            column_types.append(row['Type'])
        self.table_columns = table_columns
        self.column_types  = column_types           
        return columnDefs
        #if self.use_lowercase_names:
        #    self.table_columns = [c.lower() for c in self.table_columns]
        # '''

def sqlize(s):
    '''Change single quotes to two single quotes.
    This makes strings with single quotes in them suitable for
    insertion into sql databases.'''
    if isinstance(s, (str, unicode)):
        #s = s.encode('latin-1','replace').replace("'", "''")
        s = s.replace("'", "''")
        s = s.replace('\\', '\\\\')
    return s

#import db
#db_ = db.singletonFactory.create()
#dt = DataTable(db_, 'adoptions')
#dt.setFilters('party_id=1')
#print dt.getTable()
