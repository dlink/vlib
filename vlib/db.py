import os
import MySQLdb
import conf
import singleton

DEBUG = 0
DEBUG_SQL = 0

PORT = 3306
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

        # get port number:
        params["port"] = params.get('port', PORT)
        self.params = params
        self.connect(params)

    def connect(self, params):
        if DEBUG:
            print 'db:connect(%s)' % params
        self.close()

        # Create connection:
        self.connection = MySQLdb.connect(host        = params["host"],
                                          user        = params["user"],
                                          passwd      = params["passwd"],
                                          db          = params["db"],
                                          port        = int(params["port"]),
                                          charset     = "utf8",
                                          )

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
        self.cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        if 'timezone' in self.params:
            self.cursor.execute("set time_zone = '%s'" % self.params['timezone'])

    def close_cursor(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None

    def _execute(self, sql, params=None):
        if self.debug_sql: 
            print "SQL:", sql, params
        try:
            rv = self.cursor.execute(sql, params)
            self.lastrowid_store = self.cursor.lastrowid
            self.rowcount_store = self.cursor.rowcount
            return rv
        except MySQLdb.OperationalError, e:
            from datetime import datetime
            self.connect(self.params)
            self.open_cursor()
            rv = self.cursor.execute(sql, params)
            self.lastrowid_store = self.cursor.lastrowid
            return rv
        except Exception, e:
            raise
        
    def query(self, sql, from_trans=False, params=None):
        try:
            # Cursor may be set in the startTransaction() call.
            if not from_trans:
                self.open_cursor()
            self._execute(sql, params=params)
            data = self.cursor.fetchall()
        finally:
            if not from_trans:
                self.close_cursor()

        return data

    def startTransaction(self):
        self.open_cursor()
        self.query('start transaction',True)
    
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
            print "db.__del__()"
        self.close()

class Factory(object):
    def create(self, **params):
        if not params:  # default to config settings
            params = conf.Factory.create().data['database']
        return Db(params)

class SingletonFactory(object):
    '''Factory class for providing unique Db class instances.'''

    def __init__(self):
        if DEBUG: print "Factory.__init__()"
        self._instances = {}
        
    def create(self, **params):
        '''Given the parameters:
               engine, host, db, user, password, [ port ], [ dictcursor ]
           Return a singleton instance of the Db class for those arguments.
        '''
        if not params:  # default to config settings
            params = conf.Factory.create().data['database']

        if DEBUG:
            print "Factory.create(params={\n%s})"  % params
            
        params["port"] = params.get('port', PORT)
        if params['engine'] != 'mysql':
            raise DbError('Unsupported database engine: %s' % params['engine'])

        # db connection signature:
        signature = "%(engine)s:%(host)s:%(db)s:%(user)s:%(port)s:" \
            "%(dictcursor)s" % params
        if DEBUG: 
            print "Db.Factory: signature = %s" % signature,

        # already instantiated?
        if signature in self._instances:
            if DEBUG:
                print "Already instantiated."
            return self._instances[signature]

        db_ = Db(params)
        self._instances[signature] = db_
        if DEBUG: 
            print "Created."
        return db_

# Use this instance to create singleton Db instances:
singletonFactory = SingletonFactory()   

def getInstance():
    return singletonFactory.create()
