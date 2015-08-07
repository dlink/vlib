from vlib.datatable import DataTable
from vlib.odict import odict

DEBUG = 0

class DataRecordError(Exception): pass

class DataRecord(DataTable):
    '''Preside over a single Db Record'''

    def __init__(self, db, table, id, primary_key='id'):
        '''Create a Record Object given
              a vlib.db Object, a table name, and a record Id

           Meant to be subclassed, as follows:

           from datarecord import DataRecord

           class user(DataRecord):
              def __init__(self, id):
                 DataRecord.__init__(db.getInstance(), 'user', id)

           u = User(1)
           print u.name

        '''
        self.db    = db      
        self.table = table
        self.id    = id
        self.primary_key = primary_key

        DataTable.__init__(self, db, table)
        self.debug_sql = DEBUG
        self._loadData()

    def _loadData(self):
        '''Read a single Db Record and add it to self.__dict__

           So the following examples syntax will work:

             user.first_name,
             message.id
             message.created
        '''
        self.setFilters('%s=%s' % (self.primary_key, self.id))
        results = self.getTable()
        if not results:
            raise DataRecordError('%s table: Record not found, %s: %s' %
                              (self.table.title(), self.primary_key, self.id))

        # store data in a dictionary
        self.data = odict(results[0])

        # store data as properties of self
        self.__dict__.update(results[0])
