#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import sys
import datetime

DEBUG = 0

TEST_NAMES = ('All', 'Attribute', 'Conf', 'DataTable', 'DataRecord', 'Db',
              'Shell', 'Utils', 'SqlUtils')


# Fixtures
DATABASE_ENGINE='mysql'
SHELL='/bin/bash'
SECRET='toyboat$'

class TestConf(unittest.TestCase):
    '''Test Conf'''

    def setUp(self):
        from vlib import conf
        self.conf = conf.getInstance()

    def test_getvar(self):
        self.assertEqual(self.conf.database.engine, DATABASE_ENGINE)

    def test_getvar_withenvvar(self):
        self.assertEqual(self.conf.shell, SHELL)

    def test_getvar_withescaping(self):
        self.assertEqual(self.conf.secret, SECRET)

class TestAttribute(unittest.TestCase):

    def setUp(self):
        from vlib import db
        from vlib.attributes import Attributes
        self.disciplines = Attributes(db.getInstance(), 'disciplines')

    def test_getIdFromCode(self):
        from vlib.attributes import AttributesDataNotFoundError
        ID, CODE = 2, 'biology'
        BAD_CODE = 'mud'
        self.assertEqual(self.disciplines.getIdFromCode(CODE), ID)
        with self.assertRaises(AttributesDataNotFoundError):
            self.disciplines.getIdFromCode(BAD_CODE)

    def test_list(self):
        FIRST_D = 'Unknown'
        self.assertEqual(self.disciplines.list[0], FIRST_D)

    def test_getColumnValue(self):
        from vlib.attributes import AttributesDataNotFoundError
        ID, COLUMN, VALUE = 2, 'name', 'Biology'
        BAD_COLUMN = 'mud'
        self.assertEqual(self.disciplines.getColumnValue(ID, COLUMN), VALUE)
        with self.assertRaises(AttributesDataNotFoundError):
            self.disciplines.getColumnValue(ID, BAD_COLUMN)

    def test_getId(self):
        from vlib.attributes import AttributesError,AttributesDataNotFoundError
        ID, CODE, NAME = 2, 'biology', 'Biology'
        BAD_CODE, BAD_NAME = 'mud', 'MUD'
        self.assertEqual(self.disciplines.getId(CODE), ID)
        self.assertEqual(self.disciplines.getId(name=NAME), ID)
        with self.assertRaises(AttributesDataNotFoundError):
            self.disciplines.getId(BAD_CODE)
        with self.assertRaises(AttributesDataNotFoundError):
            self.disciplines.getId(name=BAD_NAME)
        with self.assertRaises(AttributesError):
            self.disciplines.getId()

    def test_getCode(self):
        ID, CODE = 2, 'biology'
        self.assertEqual(self.disciplines.getCode(ID), CODE)

    def test_getName(self):
        ID, NAME = 2, 'Biology'
        self.assertEqual(self.disciplines.getName(ID), NAME)

    def test_getDescription(self):
        ID, DESCRIPTION = 2, ''
        self.assertEqual(self.disciplines.getDescription(ID), DESCRIPTION)


    def test_plural2singular(self):
        from vlib.attributes import plural2singular
        for S, P in (('book', 'books'),
                     ('country', 'countries'),
                     ('status', 'statuses'),
                     ('discipline', 'disciplines')):
            self.assertEqual(plural2singular(P), S)


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

class TestDataRecord(unittest.TestCase):
    '''Test DataRecord'''

    def setUp(self):
        from vlib import db
        self.db = db.getInstance()

    def testLoad(self):
        from vlib.datarecord import DataRecord
        book = DataRecord(self.db, 'books', 1, primary_key='book_id')
        self.assertEqual(book.book_name, 'baranoff')

class TestDb(unittest.TestCase):
    '''Test Db'''

    def setUp(self):
        from vlib import db

        self.db = db.getInstance()

    def test_query(self):
        sql = 'select book_name from books where book_id = 1'
        results = self.db.query(sql)
        self.assertEqual(results[0]['book_name'], 'baranoff')

    def test_timezone(self):
        from vlib import conf
        sql = 'select @@session.time_zone as time_zone'
        db_timezone = self.db.query(sql)[0]['time_zone']
        self.assertEqual(conf.getInstance().database.timezone, db_timezone)

    def test_timezone_same_as_localhost(self):
        sql = 'SELECT date_format(now(), "%Y-%m-%d %H:%i") as now;'
        db_datetime = self.db.query(sql)[0]['now']
        localhost_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M").lower()
        self.assertEqual(localhost_datetime, db_datetime)

    def test_rollback(self):
        max_book_id = self._getMaxBookId()
        self.db.startTransaction()
        try:
            sql = 'insert into books (book_name) value ("Unit Test Book")'
            self.db.execute(sql)
            raise Exception('Test Error')
        except Exception as e:
            self.db.rollback()
        max_book_id2 = self._getMaxBookId()
        self.assertEqual(max_book_id, max_book_id2)
        self._resetBooksAutoInc()

    def test_commit(self):
        max_book_id = self._getMaxBookId()
        self.db.startTransaction()
        try:
            sql = 'insert into books (book_name) value ("Unit Test Book")'
            self.db.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
        max_book_id2 = self._getMaxBookId()
        self.assertEqual(max_book_id+1, max_book_id2)
        self._removeBook(max_book_id2)
        self._resetBooksAutoInc()

    def _getMaxBookId(self):
        sql = 'select max(book_id) as max_book_id from books'
        return self.db.query(sql)[0]['max_book_id']

    def _removeBook(self, book_id):
        sql = 'delete from books where book_id = %s' % book_id
        self.db.execute(sql)

    def _resetBooksAutoInc(self):
        sql = 'alter table books auto_increment = 1'
        self.db.execute(sql)

class TestShell(unittest.TestCase):
    def setUp(self):
        from vlib.shell import Shell
        self.shell = Shell()

    def test_ls(self):
        output = self.shell.cmd('ls')

class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def test_pretty_str(self):
        import vlib.utils
        str = 'This is a string'
        self.assertEqual(str, vlib.utils.pretty(str))

    def test_pretty_list(self):
        import vlib.utils
        Astr = '''ennie
meanie
mightie'''
        A = ['ennie', 'meanie', 'mightie']
        self.assertEqual(Astr, vlib.utils.pretty(A))

    def test_pretty_dict(self):
        import vlib.utils
        Dstr = '''color: blue
shape: square
texture: groovy'''
        D = {'shape': 'square', 'texture': 'groovy', 'color': 'blue'}
        self.assertEqual(Dstr, vlib.utils.pretty(D))

    def test_pretty_list_of_lists(self):
        import vlib.utils
        AAstr = '''a,b,c
d,e,f
g,h,i'''
        AA = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g','h', 'i']]
        self.assertEqual(AAstr, vlib.utils.pretty(AA))

    def test_format_datetime(self):
        import vlib.utils
        d = datetime.datetime(2013,11,22,10,9,8)
        self.assertEqual(vlib.utils.format_datetime(d),
                         '11/22/2013 10:09 am')

    def test_format_datetime_with_sections(self):
        import vlib.utils
        d = datetime.datetime(2013,11,22,10,9,8)
        self.assertEqual(vlib.utils.format_datetime(d, with_seconds=1),
                         '11/22/2013 10:09:08 am')

    def test_format_datetime_ISO8601(self):
        import vlib.utils
        d = datetime.datetime(2013,11,22,10,9,8)
        self.assertEqual(vlib.utils.format_datetime(d, format='ISO8601'),
                         '2013-11-22T10:09:08-05:00')

    def test_format_datetime_ISO8601_without_time(self):
        import vlib.utils
        d = datetime.datetime(2013,11,22)
        self.assertEqual(vlib.utils.format_datetime(d, format='ISO8601'),
                         '2013-11-22T00:00:00-05:00')

class TestSqlUtils(unittest.TestCase):
    '''Given sql statements already in pretty format
       remove formating, reformat, and then compare.
    '''

    def xtest_sql_pretty1(self):
        self.do_test(1)

    def test_sql_pretty2(self):
        self.do_test(2)

    def do_test(self, test_num):
        import re
        import vlib.sqlutils
        sql = open('testsqlpretty%s.sql' % test_num).read()
        rawsql = re.sub(r'\s+', ' ', sql)
        prettysql = vlib.sqlutils.pretty_sql(rawsql)

        #self.show_before_and_after(sql, prettysql)
        self.assertEqual(sql, prettysql)

    def show_before_and_after(self, sql1, sql2):
        '''For testing the test'''
        print()
        print('"%s"' % sql1.replace(' ', '_'))
        print()
        print('"%s"' % sql2.replace(' ', '_'))
        
def syntax():
    progname = os.path.basename(sys.argv[0])
    print()
    print("  syntax: %s [%s]+" % (progname, ' | '.join(TEST_NAMES)))
    print()
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        syntax()

    if any(t not in TEST_NAMES for t in sys.argv[1:]):
        print("Test name must be one (or more) of:", ", ".join(TEST_NAMES))
        sys.exit(1)

    if  sys.argv[1] == 'All':
        tests = []
        for test_name in TEST_NAMES[1:]:
            tests.append(eval('Test%s' % test_name))
    else:
        tests = [eval('Test%s' % t) for t in sys.argv[1:]]

    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    suite.addTests([loader(t) for t in tests])

    unittest.TextTestRunner(verbosity=2).run(suite)
