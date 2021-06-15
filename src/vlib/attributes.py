
from vlib.datatable import DataTable

class AttributesError (Exception): pass
class AttributesDataNotFoundError (AttributesError): pass

class Attributes (DataTable):
    '''Preside over attribute database tables that has the following structure

       +-------------+------------------+------+-----+---------+-------+
       | Field       | Type             | Null | Key | Default | Extra |
       +-------------+------------------+------+-----+---------+-------+
       | <attr>_id   | int(10) unsigned | NO   | PRI |         |       |
       | code        | varchar(20)      | NO   |     |         |       |
       | name        | varchar(128)     | NO   |     |         |       |
       | description | varchar(256)     | YES  |     | NULL    |       |
       | active      | int(10 unsigned  | NO   |     |         |       |
       |                                                               |
       | (can have extra columns ...)                                  |
       +-------------+------------------+------+-----+---------+-------+
    '''

    def __init__ (self, db, tablename, id_field=None):
        '''Given a db connection, and a table name, that conforms to the
           Attributes Model load data.
        '''
        DataTable.__init__(self, db, tablename)
        self.id_field = id_field if id_field \
                        else plural2singular(tablename) + '_id'
        self._loadTable()
        self._setConstants()

    def getIdFromCode(self, code, or_add=0):
        code = str(code)
        try:
            id = self.code_map[code.lower()]
        except:
            if not or_add:
                raise AttributesDataNotFoundError(
                    "%s: code '%s' not found" % (self.tablename, code))
            else:
                # add rec
                rec = {'code'       : code.lower(),
                       'name'       : code.replace('_', ' ').title(),
                       'description': code.replace('_', ' ').title(),
                       'active'     : True}
                id = self.insertRow(rec)
                
                # update internal dicts
                self._table[id] = rec
                self._code_map[code.lower()] = id
                self._name_map[code.lower()] = id
        return id

    @property
    def table(self):
        '''Return list of Dicts of all rows'''
        return self._table

    @property
    def code_map(self):
        '''Return DICT of code => id pairs'''
        return self._code_map

    @property
    def name_map(self):
        '''Return DICT of name => id pairs'''
        return self._name_map

    @property
    def list(self):
        '''Return a list of names'''
        return self.getListOf('name')

    def getListOf(self, column):
        '''Return a list of columns values,
           Where column is a column name in the table.
        '''
        return [self.table[x][column] for x in list(self._table.keys())]

    def _loadTable (self):
        '''Loads database table.
           Behavior:  Set self._table     - the table data (list of dicts)
                          self._code_map  - maps codes to ids
                          self._name_map  - maps names to ids
        '''
        self.setColumns('*')
        self.setFilters()
        table_rows = self.getTable()

        # store record and id/code look ups
        table = {}
        code_map = {}
        name_map = {}
        for record in table_rows:
            id   = record[self.id_field]
            code = record['code']
            name = record['name']
            active=record['active']
            if not active:
                continue
            table[id] = record
            code_map[code.lower()] = id
            name_map[name] = id  # potential overwrite of non-uniq name values
        self._table = table
        self._code_map = code_map
        self._name_map = name_map

    def _setConstants(self):
        '''Set up constants like states.INPROGRESS, states.ERROR, etc.,
           or roles.USER, roles.AUTHOR, etc.,
           based on the table's code field.                                                      '''
        for id, data in list(self.table.items()):
            self.__setattr__(data['code'].upper(), id)

    def getColumnValue (self, id, column):
        '''For a given row defined by id, return column value.'''

        #if id not in self.table or column not in self.table[id]:
        #    self.cache_expired = True # reload data
        try:
            return self.table[id][column]
        except:
            raise AttributesDataNotFoundError(
            'Unable to retrieve column %s, id %s in table %s'
            % (column, id, self.tablename))

    def getCode (self, id):
        '''For a given Id, return the Code column.'''
        return self.getColumnValue(id, 'code')

    def getName (self, id):
        '''For a given Id, return Name column.'''
        return self.getColumnValue(id, 'name')

    def getDescription (self, id):
        '''For a given Id, return Description column.'''
        return self.getColumnValue(id, 'description')

    def getId(self, code=None, name=None):
        '''For a given Code, or Name return Id column.'''

        if code:
            code = code.lower()
            if code not in self.code_map:
                self.cache_expired = True # reload table
            try:
                return self.code_map[code]
            except:
                raise AttributesDataNotFoundError(
                    '%s: Unable to getId, unrecognized code: %s'
                    % (self.tablename, code))
        elif name:
            if name not in self.name_map:
                self.cache_expired = True
            try:
                return self.name_map[name]
            except:
                raise AttributesDataNotFoundError(
                    '%s: Unable to getId, unrecognized name: %s'
                    % (self.tablename, name))
        else:
            raise AttributesError('%s: Unable to getId.  Must specify either '
                                 'code or name' % self.tablename)


def plural2singular(name):
    '''Given a noun in its plural, Return it in its singular

       eq. boats --> boat
           parties --> party
    '''
    # spec. cases
    if name == 'statuses':
        return 'status'

    name2 = name

    # ies --> y
    if name[-3:] == 'ies':
        name2 = name[0:-3] + 'y'

    # boats --> boat
    # access --> access (no change)
    elif name[-1] == 's' and name[-2] != 's':
        name2 = name[0:-1]

    return name2

def test():
    from vlib import db
    states = Attributes(db.getInstance(),
                            'usage_time_frames',
                            'id')
    print('List:', states.list)
    print('Code Map:', states.code_map)
    print('Name Map:',states.name_map)

if __name__ == '__main__':
    test()
