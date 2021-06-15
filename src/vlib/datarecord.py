from vlib.datatable import DataTable
from vlib.odict import odict

from vlib.utils import is_int

DEBUG = 0

class DataRecordError(Exception): pass
class DataRecordNotFound(DataRecordError): pass

class DataRecord(DataTable):
    '''Preside over a single Db Record'''

    def __init__(self, db, table, id, primary_key='id'):
        '''Create a Record Object given
              a vlib.db Object, a table name, and a record Id

           id column can also be an sql where clause, like
               'order_no="TC-100903401"'

           Meant to be subclassed, as follows:

           from datarecord import DataRecord

           class User(DataRecord):
              def __init__(self, id):
                 DataRecord.__init__(db.getInstance(), 'user', id)

           u = User(1)
           print u.name

           u2 = User("name='Fernandez'")
           print u2.phone

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
        if is_int(self.id):
            filter = '%s=%s' % (self.primary_key, self.id)
        else:
            # id is an sql where_clause
            filter = self.id

        self.setFilters(filter)
        results = self.getTable()
        if not results:
            raise DataRecordNotFound('%s table: Record not found, %s: %s' %
                              (self.table.title(), self.primary_key, self.id))

        # store data in a dictionary
        self.data = odict(results[0])

        # store data as properties of self
        self.__dict__.update(results[0])

    @property
    def fields(self):
        '''Return DataRecord field names'''
        return sorted(self.data.keys())
