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
        self.limit     = None
        self.debug     = DEBUG
        self.debug_sql = DEBUG_SQL
        self.writeback = WRITEBACK

    #def setAutocommit (self, state):
    #   '''Turn autocommit on (1) or off (0). Default is on.  See __init__()'''
    #    self.autocommit = state
    
    @property
    def table_columns(self):
        return [x['Field'] for x in self.db.query('desc %s' % self.tablename)]

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
            print(__name__, self.tablename, "setWriteBack (%s)" % switch)
        self.writeback = switch

    def describe(self):
        '''Return output of SQL Describe command as a Dict'''
        return self.db.query('desc %s' % self.tablename)

        
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

        The filters arg can be a string, a list of strings, or a dict
        containing strings or lists (to use with "W in (X, Y, Z)")
        
        Examples: dobj.setFilters ("email like 'fred%'")
                  dobj.setFilters (["email like 'fred%'", "name = 'Fred'"])
                  dobj.setFilters ({'email': 'fred@foo.bar', 'name': 'Fred'})
                  dobj.setFilters ({'name': ['Fred', 'foo', 'bar']})
        '''

        if isinstance(filters, str):
            #string
            new_filters = [filters]
        elif isinstance(filters, dict):
            #dict
            new_filters = []
            for k, v in list(filters.items()):
                if v is None:
                    new_filters.append("%s is null" % k)
                elif isinstance(v, list):
                    vals = ["'%s'" % sqlize(val) for val in v]
                    new_filters.append("%s in (%s)" % (k, ", ".join(vals)))
                else:
                    new_filters.append("%s = '%s'" % (k, sqlize(v)))
        else:
            #list
            new_filters = filters
        self.filters = new_filters

    def setOrderBy (self, order_by):
        '''Set list of columns used in ORDER BY CLAUSE of
        subsequent SQL SELECT statements.
        '''
        
        if isinstance(order_by, (int, str)):
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
        
    def get(self, filter=None):
        '''Given an optional SQL filter, or None for All
           Return rows.  (See getTable())
        '''
        o = []
        self.setColumns('*')
        if filter:
            self.setFilters(filter)
        else:
            self.setFilters('1')
        return self.getTable()

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
        
        if self.debug: print(__name__, self.tablename, "getTable ()")
        
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
            order_by = 'order by %s' % ', '.join(map(str, self.order_by))
        limit = ''
        if self.limit is not None:
            limit = 'limit %s' % self.limit
        sql = '%s %s %s %s %s %s' % (select, From, where, group_by, order_by, 
                                     limit)
        if self.debug_sql: print(__name__, self.tablename, "SQL:\n ", sql)
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
        if DEBUG: print(__name__, self.tablename, '%sRow()' % sql_cmd)
        if len(record) < 1:
            raise DataTableError ('Record to insert is blank')

        columns, values = list(zip(*list(record.items())))
        sql = "%s into %s (%s) values (%s)" % (
            sql_cmd,
            self.tablename,
            # support column names with spaces.
            ', '.join(map(self.sql_quote, columns)),
            ', '.join(['%s'] * len(values)),
        )

        if self.debug_sql:
            print(__name__, self.tablename, "SQL:\n ", sql, values)
        id = 0
        try:
            if self.writeback:
                self.db.execute(sql, params=values)
                id = self.db.lastrowid    # MySQLdb 1.2.1

        except Exception as e:
            type, value, traceback = sys.exc_info()
            msg = "Unable to insert row into %s: %r" % (self.tablename, e)
            raise DataTableError(msg, type, value).with_traceback(traceback)
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
            print(__name__, self.tablename, "updateRows (%s)" % record)
        if len(record) < 1:
            raise DataTableError ('Record to insert is blank')

        # set_statment = "set col1 = 'mojo', col2 = 'jojo', ..."
        setters = []
        # We need the values in the same order as the keys later on, so
        # solidify the order of the elements now and use values for the
        # parameter binding later.
        record_items = list(record.items())
        columns, values = list(zip(*record_items))
        for column, value in record_items:
            # Create a PDO template for parameter binding.
            setters.append("%s = %%s" % column)
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

        if self.debug_sql:
            sql_with_vals = sql % tuple(["'%s'" % x for x in values])
            print(__name__, self.tablename, "SQL:\n ", sql_with_vals)
        rowcount = 0
        try:
            if self.writeback:
                self.db.query(sql, params=values)
                rowcount = self.db.rowcount
                #if self.autocommit:
                #    self.db.commit()
        except Exception as e:
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
            print(__name__, self.tablename, "deleteRows ()")

        where  = ''
        if self.filters:
            where = 'where %s' % ' and '.join(self.filters)
        else:
            raise DataTableError(
                'Unable to deleteRows ().  No filter specified')
        
        sql = "delete from %s %s" % (
            self.tablename,
            where)

        if self.debug_sql: print(__name__, self.tablename, "SQL:\n ", sql)
        rowcount = 0
        try:
            if self.writeback:
                self.db.execute(sql)
                rowcount = self.db.rowcount
                #if self.autocommit:
                #    self.db.commit()
        except Exception as e:
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
        except Exception as e:
            raise DataTableError(e)

        #$table_alias = self.getAlias() - table alias to come
        columnDefs = []
        #table_columns = []
        column_types  = []
        for row in table:
            columnDefs.append({'name': row['Field'],
                               'type': row['Type']})
            #table_columns.append(row['Field'])
            column_types.append(row['Type'])
        #self.table_columns = table_columns
        self.column_types  = column_types           
        return columnDefs
        #if self.use_lowercase_names:
        #    self.table_columns = [c.lower() for c in self.table_columns]
        # '''

    def sql_quote(self, column):
        '''Return an SQL quoted column for the given db.engine'''

        if self.db.engine == 'mssql':
            return '[%s]' % column
        else:
            return '`%s`' % column

def sqlize(s):
    '''Change single quotes to two single quotes.
    This makes strings with single quotes in them suitable for
    insertion into sql databases.'''
    if isinstance(s, str):
        #s = s.encode('latin-1','replace').replace("'", "''")
        s = s.replace("'", "''")
        s = s.replace('\\', '\\\\')
    return s

# Tests
#import db
#db_ = db.getInstance()
#dt = DataTable(db_, 'providers')
#dt.setFilters('id=3')
#print dt.getTable()
#print dt.table_columns
#for row in dt.describe():
#    print row
