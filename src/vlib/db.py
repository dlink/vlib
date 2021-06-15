import os
from . import conf
from . import singleton

DEBUG = 0
DEBUG_SQL = 0

MYSQL_PORT = 3306
MSSQL_PORT = 1433
AUTOCOMMIT = True

DEBUG_PROCESSLIST = 0
DEBUG_OPENCLOSE = 0

class DbError(Exception): pass

class Db (object):
    '''Preside over Database connection and Database cursor.

       example:
         db = Db({'engine':'mysql', 'host':'db1', 'db':'books', 
                  'user':'bookmgr', 'passwd':'mepassword', 'dictcursor':True })

       Use db.factory.create() for reusing single database connections.
    '''
    
    def __init__(self, params):
        '''Db Class constructor
           Params: engine, host, db, user, password, [ port ], [ dictcursor ]
        '''
        
        self.connection = None
        self.debug_sql  = DEBUG_SQL or ('DEBUG_VLIB' in os.environ)
        self.cursor = None
        self.lastrowid_store = None
        self.rowcount_store = None

        self.params = params
        self.connect(params)

    def __repr__(self):
        return '%s.%s:%s' % (self.__class__.__module__,
                             self.__class__.__name__,
                             self.params['db'])

    def connect(self, params):
        if DEBUG:
            print('db:connect(%s)' % params)
        self.close()
        self.engine = engine = params['engine']

        # support environement vars for passwd
        passwd = params['passwd']
        if passwd.startswith('$'):
            passwd = os.environ[passwd[1:]]

        # Create connection:

        if engine == 'mysql':
            import pymysql.cursors
            self.connection = pymysql.connect(
                host     = params["host"],
                user     = params["user"],
                password = passwd,
                database = params["db"],
                cursorclass=pymysql.cursors.DictCursor
            )

        elif engine == 'mssql':
            import pymssql
            self.connection = pymssql.connect(
                server   = params["host"],
                user     = params["user"],
                password = params["passwd"],
                database = params["db"],
                port     = int(params.get('port', MSSQL_PORT)),
                charset  = "utf8")

        else:
            raise DbError('Unsupported database engine: %s' % engine)

        self.connection.autocommit(AUTOCOMMIT)
        
    def open_cursor(self):
        '''
        if 'dictcursor' in params:
            self.cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        else:
            self.cursor = self.connection.cursor()
        '''
        # N.B.: This class MUST be used as a short-lived object. 
        # A new object has to be created each time the db is accessed
        # anew, otherwise this self variable will cause great trouble.
        self.close_cursor()
        if self.engine == 'mysql':
            self.cursor = self.connection.cursor()
        else:
            self.cursor = self.connection.cursor(as_dict=True)
        if self.engine != 'mssql' and 'timezone' in self.params:
            self.cursor.execute("set time_zone = '%s'"
                                % self.params['timezone'])

    def close_cursor(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None

    def _execute(self, sql, params=None):
        if self.debug_sql: 
            print("SQL:", sql, params)

        rv = self.cursor.execute(sql, params)
        if self.engine != 'mssql':
            # not working for mssql for some reason
            self.lastrowid_store = self.cursor.lastrowid
        self.rowcount_store = self.cursor.rowcount
        return rv
        
    def query(self, sql, from_trans=False, params=None):
        '''Use query for SQL statements that return data
             eq.: select, desc, show tables, etc
           Also see: execute()
        '''
        return self.execute(sql, from_trans, params, query=True)

    def execute(self, sql, from_trans=False, params=None, query=False):
        '''Execute an SQL statement that does not return data
             eq.: insert, update, create, etc
           Also see: query()

           It was nec. to break query() and execute() into two methods
           to support mssql driver.
        '''
        try:
            # Cursor may be set in the startTransaction() call.
            if not from_trans:
                self.open_cursor()
            self._execute(sql, params=params)
            if query:
                data = self.cursor.fetchall()
        finally:
            if not from_trans:
                self.close_cursor()
        if query:
            return data

    def startTransaction(self):
        self.open_cursor()
        if self.engine == 'mysql':
            sqlcmd = 'start transaction'
        else:
            sqlcmd = 'begin transaction'
        self.execute(sqlcmd)
    
    def rollback(self):
        self.connection.rollback()
        self.close_cursor()
    
    def commit(self):
        self.connection.commit()
        self.close_cursor()
    
    def close(self):
        self.close_cursor()
        if self.connection: 
            self.connection.close()

    @property
    def lastrowid(self):
        return self.lastrowid_store
    
    @property
    def rowcount(self):
        return self.rowcount_store
    
    def __del__(self):
        if DEBUG:
            print("db.__del__()")
        self.close()

class Factory(object):
    def create(self, **params):
        if not params:  # default to config settings
            params = conf.Factory.create().data['database']
        return Db(params)

class SingletonFactory(object):
    '''Factory class for providing unique Db class instances.'''

    def __init__(self):
        if DEBUG: print("Factory.__init__()")
        self._instances = {}
        
    def create(self, **params):
        '''Given the parameters:
               engine, host, db, user, password, [ port ], [ dictcursor ]
           Return a singleton instance of the Db class for those arguments.
        '''
        if not params:  # default to config settings
            params = conf.Factory.create().data['database']

        if DEBUG:
            print("Factory.create(params={\n%s})"  % params)
            
        # db connection signature:
        signature = "%(engine)s:%(host)s:%(db)s:%(user)s:" \
            "%(dictcursor)s" % params
        if DEBUG: 
            print("Db.Factory: signature = %s" % signature, end=' ')

        # already instantiated?
        if signature in self._instances:
            if DEBUG:
                print("Already instantiated.")
            return self._instances[signature]

        db_ = Db(params)
        self._instances[signature] = db_
        if DEBUG: 
            print("Created.")
        return db_

# Use this instance to create singleton Db instances:
singletonFactory = SingletonFactory()   

def getInstance():
    return singletonFactory.create()
