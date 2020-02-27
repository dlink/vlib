import unittest

from vlib import db
from vlib.datatable import DataTable

class TestDataTable(unittest.TestCase):
    '''Test DataTable'''

    def setUp(self):
        self.db = db.getInstance()
        self.datatable = DataTable(self.db, 'disciplines')

    def test_columnDefs(self):
        expected = [
            {'type': 'int(10) unsigned', 'name': 'discipline_id'},
            {'type': 'varchar(30)', 'name': 'code'},
            {'type': 'varchar(45)', 'name': 'name'},
            {'type': 'varchar(255)', 'name': 'description'},
            {'type': 'int(10) unsigned', 'name': 'active'},
            {'type': 'timestamp', 'name': 'last_updated'},
        ]
        sort = lambda r: sorted(r, key=lambda x: x['name'])
        results = sort(self.datatable.columnDefs())
        actual = sort(results)
        expected = sort(expected)
        for old, new in zip(expected, actual):
            self.assertDictEqual(old, new)

    def test_table_columns(self):
        expected = ['discipline_id', 'code', 'name', 'description',
                    'active', 'last_updated']
        results = self.datatable.table_columns
        self.assertEqual(expected, results)

    def test_describe(self):
        sort = lambda r: sorted(r, key=lambda x: x['Field'])
        expected = sort([
            {'Extra': '', 'Default': None, 'Field': 'discipline_id',
             'Key': 'PRI', 'Null': 'NO', 'Type': 'int(10) unsigned'},
            {'Extra': '', 'Default': None, 'Field': 'code',
             'Key': 'MUL', 'Null': 'NO', 'Type': 'varchar(30)'},
            {'Extra': '', 'Default': None, 'Field': 'name',
             'Key': '', 'Null': 'NO', 'Type': 'varchar(45)'},
            {'Extra': '', 'Default': None, 'Field': 'description',
             'Key': '', 'Null': 'YES', 'Type': 'varchar(255)'},
            {'Extra': '', 'Default': None, 'Field': 'active',
             'Key': '', 'Null': 'NO', 'Type': 'int(10) unsigned'},
            {'Extra': 'on update CURRENT_TIMESTAMP',
             'Default': 'CURRENT_TIMESTAMP', 'Field': 'last_updated',
             'Key': '', 'Null': 'NO', 'Type': 'timestamp'}
            ])
        results = sort(self.datatable.describe())
        for old, new in zip(expected, results):
            self.assertDictEqual(old, new)

    def test_getTableSelect(self):
        ID = 2
        DATA = ({'code': 'biology'},)
        self.datatable.setColumns(['code'])
        self.datatable.setOrderBy(1)
        self.datatable.setLimit(10)

        # string filter
        self.datatable.setFilters('discipline_id=%s' % ID)
        self.assertEqual(self.datatable.getTable(), DATA)

        # dict filter
        self.datatable.setFilters({'discipline_id': ID})
        self.assertEqual(self.datatable.getTable(), DATA)

        # is NULL filter
        self.datatable.setFilters({'discipline_id': None})
        self.assertNotEqual(self.datatable.getTable(), DATA)

        # list of filters
        CODE = 'biology'
        self.datatable.setFilters(['discipline_id=%s' % ID, 'code="%s"' %CODE])
        self.assertEqual(self.datatable.getTable(), DATA)

        # is in
        IDS = [2,4]
        DATA = ({'code': 'biology'},{'code': 'chemistry'})
        self.datatable.setFilters('discipline_id=%s' % ID)
        self.datatable.setFilters({'discipline_id': IDS})
        self.assertEqual(self.datatable.getTable(), DATA)

        # group by - int
        IDS = [2,4,5]
        DATA = ({'first': 'B', 'count': 1}, {'first': 'C', 'count': 2})
        self.datatable.setColumns(['left(name, 1) as first',
                                   'count(*) as count'])
        self.datatable.setFilters({'discipline_id': IDS})
        self.datatable.setGroupBy(1)
        self.assertEqual(self.datatable.getTable(), DATA)

        # group by - string
        self.datatable.setGroupBy('first')
        self.assertEqual(self.datatable.getTable(), DATA)

    def test_getTable_Insert_Delete(self):
        DATA = {'discipline_id': 100,
                'code': 'computers',
                'name': 'Computers',
                'active': 0}
        # insert
        self.datatable.insertRow(DATA)
        self.datatable.setColumns(DATA.keys())
        self.datatable.setFilters('code = "%s"' % DATA['code'])
        self.assertEqual(self.datatable.getTable(), (DATA,))

        # delete
        self.datatable.deleteRows()
        self.assertEqual(self.datatable.getTable(), ())
