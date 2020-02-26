import unittest

class TestDataTable(unittest.TestCase):
    '''Test DataTable'''

    def setUp(self):
        from vlib import db
        from vlib.datatable import DataTable

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

