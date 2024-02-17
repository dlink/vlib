import unittest

from vlib import db
from vlib.datatable import DataTable
from vlib.datarecord import DataRecord
from vlib.odict import odict

class TestDataTable(unittest.TestCase):
    '''Test DataTable'''

    def setUp(self):
        self.db = db.getInstance()
        self.datatable = DataTable(self.db, 'disciplines')

    def test_columnDefs(self):
        expected = [
            {'type': 'int(10) unsigned', 'name': 'id'},
            {'type': 'varchar(30)', 'name': 'code'},
            {'type': 'varchar(45)', 'name': 'name'},
            {'type': 'varchar(255)', 'name': 'description'},
            {'type': 'tinyint(1)', 'name': 'active'},
            {'type': 'timestamp', 'name': 'last_updated'},
        ]
        sort = lambda r: sorted(r, key=lambda x: x['name'])
        results = sort(self.datatable.columnDefs())
        actual = sort(results)
        expected = sort(expected)
        for old, new in zip(expected, actual):
            self.assertDictEqual(old, new)

    def test_table_columns(self):
        expected = ['id', 'code', 'name', 'description',
                    'active', 'last_updated']
        results = self.datatable.table_columns
        self.assertEqual(expected, results)

    def test_describe(self):
        sort = lambda r: sorted(r, key=lambda x: x['Field'])
        expected = sort([
            {'Extra': '', 'Default': None, 'Field': 'id',
             'Key': 'PRI', 'Null': 'NO', 'Type': 'int(10) unsigned'},
            {'Extra': '', 'Default': None, 'Field': 'code',
             'Key': 'MUL', 'Null': 'NO', 'Type': 'varchar(30)'},
            {'Extra': '', 'Default': None, 'Field': 'name',
             'Key': '', 'Null': 'NO', 'Type': 'varchar(45)'},
            {'Extra': '', 'Default': None, 'Field': 'description',
             'Key': '', 'Null': 'YES', 'Type': 'varchar(255)'},
            {'Extra': '', 'Default': '1', 'Field': 'active',
             'Key': '', 'Null': 'YES', 'Type': 'tinyint(1)'},
            {'Extra': 'on update CURRENT_TIMESTAMP',
             'Default': 'CURRENT_TIMESTAMP', 'Field': 'last_updated',
             'Key': '', 'Null': 'NO', 'Type': 'timestamp'}
            ])
        results = sort(self.datatable.describe())
        for old, new in zip(expected, results):
            self.assertDictEqual(old, new)

    def test_getTable(self):
        ID = 2
        CODE = 'biology'
        DATA = [{'code': 'biology'}]
        self.datatable.setColumns(['code'])
        self.datatable.setOrderBy(1)
        self.datatable.setLimit(10)

        # string filter
        self.datatable.setFilters('id=%s' % ID)
        self.assertEqual(self.datatable.getTable(), DATA)

        # dict filter
        self.datatable.setFilters({'id': ID})
        self.assertEqual(self.datatable.getTable(), DATA)

        # dict fitler with string value
        self.datatable.setFilters({'code': CODE})
        self.assertEqual(self.datatable.getTable(), DATA)

        # is NULL filter
        self.datatable.setFilters({'id': None})
        self.assertNotEqual(self.datatable.getTable(), DATA)

        # list of filters
        self.datatable.setFilters(['id=%s' % ID, 'code="%s"' %CODE])
        self.assertEqual(self.datatable.getTable(), DATA)

        # is in
        IDS = [2,4]
        DATA = [{'code': 'biology'},{'code': 'chemistry'}]
        self.datatable.setFilters({'id': IDS})
        self.assertEqual(self.datatable.getTable(), DATA)

        # group by - int
        IDS = [2,4,5]
        DATA = [{'first': 'B', 'count': 1}, {'first': 'C', 'count': 2}]
        self.datatable.setColumns(['left(name, 1) as first',
                                   'count(*) as count'])
        self.datatable.setFilters({'id': IDS})
        self.datatable.setGroupBy(1)
        self.assertEqual(self.datatable.getTable(), DATA)

        # group by - string
        self.datatable.setGroupBy('first')
        self.assertEqual(self.datatable.getTable(), DATA)

    # test_get
    def test_get_simple(self):
        ID = 2
        results = self.datatable.get('id=%s' % ID)
        self.assertEqual(results[0]['id'], ID)
        self.assertEqual(type(odict()), type(results[0]))

    def test_get_none_filter(self):
        NUM_ROWS = 20
        results = self.datatable.get(show_inactives=1)
        self.assertEqual(len(results), NUM_ROWS)

    def test_get_none_filter_with_inactives(self):
        NUM_ROWS = 20
        results = self.datatable.get()
        self.assertEqual(len(results), NUM_ROWS-1)

    def test_get_none_filter_no_active_field(self):
        # Books table has no active flag
        books = DataTable(self.db, 'books')
        NUM_ROWS = 85
        results = books.get()
        self.assertEqual(len(results), NUM_ROWS)

    def test_get_str_filter(self):
        NUM_ROWS = 2
        results = self.datatable.get('code like "a%"')
        self.assertEqual(len(results), NUM_ROWS-1)

    def test_get_str_filter_with_inactives(self):
        NUM_ROWS = 2
        results = self.datatable.get('code like "a%"', show_inactives=1)
        self.assertEqual(len(results), NUM_ROWS)

    def test_get_list_filter(self):
        NUM_ROWS = 2
        results = self.datatable.get(['code like "a%"'])
        self.assertEqual(len(results), NUM_ROWS-1)

    def test_get_list_filter_with_inactives(self):
        NUM_ROWS = 2
        results = self.datatable.get(['code like "a%"'], show_inactives=1)
        self.assertEqual(len(results), NUM_ROWS)

    def test_get_dict_filter(self):
        NUM_ROWS = 1
        results = self.datatable.get({'code': 'alchemy'})
        self.assertEqual(len(results), NUM_ROWS-1)

    def test_get_dict_filter_with_inactives(self):
        NUM_ROWS = 1
        results = self.datatable.get({'code': 'alchemy'}, show_inactives=1)
        self.assertEqual(len(results), NUM_ROWS)

    def test_get_with_recordObj(self):
        db = self.db
        class Discipline(DataRecord):
            def __init__(self, id):
                super().__init__(db, 'disciplines', id)

        disciplines = DataTable(self.db, 'disciplines', Discipline)
        results = disciplines.get({'id': 1})
        self.assertEqual(type(Discipline(1)), type(results[0]))

    def test_iter(self):
        NUM_ROWS = 20
        all_recs = []
        for rec in self.datatable:
            all_recs.append(rec)
        self.assertEqual(len(all_recs), NUM_ROWS)

    def test_insertRow_deleteRows(self):
        DATA = {'id': 100,
                'code': 'computers',
                'name': 'Computers',
                'active': 0}
        # insert
        self.datatable.insertRow(DATA)
        self.datatable.setColumns(DATA.keys())
        self.datatable.setFilters('code = "%s"' % DATA['code'])
        self.assertEqual(self.datatable.getTable(), [DATA])

        # delete
        self.datatable.deleteRows()
        self.assertEqual(self.datatable.getTable(), ())

    def test_updateRows(self):
        CODE = 'biology'
        DATA = {'active': 0}
        DATA2 = {'active': 1}

        # update
        self.datatable.setFilters('code = "%s"' % CODE)
        self.datatable.updateRows(DATA)
        self.datatable.setColumns('active')
        self.assertEqual(self.datatable.getTable(), [DATA])

        # update it back
        self.datatable.updateRows(DATA2)
        self.assertEqual(self.datatable.getTable(), [DATA2])
