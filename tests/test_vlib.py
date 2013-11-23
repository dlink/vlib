#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import sys
import datetime

DEBUG = 0

TEST_NAMES = ('All', 'Conf', 'DataTable', 'Db', 'Shell', 'Utils')


# Fixtures
DATABASE_ENGINE='mysql'
SHELL='/bin/bash'
SECRET='toyboat$'

class TestConf(unittest.TestCase):
    '''Test Conf'''
    
    def setUp(self):
        import conf
        self.conf = conf.getInstance()
        
    def test_getvar(self):
        self.assertEqual(self.conf.database.engine, DATABASE_ENGINE)
        
    def test_getvar_withenvvar(self):
        self.assertEqual(self.conf.shell, SHELL)

    def test_getvar_withescaping(self):
        self.assertEqual(self.conf.secret, SECRET)
        
class TestDataTable(unittest.TestCase):
    '''Test DataTable'''

    def setUp(self):
        import db
        from datatable import DataTable
        
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

class TestDb(unittest.TestCase):
    '''Test Db'''

    def setUp(self):
        import db

        self.db = db.getInstance()

    def test_query(self):
        sql = 'select book_name from books where book_id = 1'
        results = self.db.query(sql)
        self.assertEqual(results[0]['book_name'], 'baranoff')

    def test_timezone(self):
        import conf
        sql = 'select @@session.time_zone as time_zone'
        db_timezone = self.db.query(sql)[0]['time_zone']
        self.assertEqual(conf.getInstance().database.timezone, db_timezone)
        
    def test_timezone_same_as_localhost(self):
        sql = 'SELECT date_format(now(), "%Y-%m-%d %H:%i") as now;'
        db_datetime = self.db.query(sql)[0]['now']
        localhost_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M").lower()
        self.assertEqual(localhost_datetime, db_datetime)
        
class TestShell(unittest.TestCase):
    def setUp(self):
        from shell import Shell
        self.shell = Shell()
        
    def test_ls(self):
        output = self.shell.cmd('ls')

class TestUtils(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_pretty_str(self):
        import utils
        str = 'This is a string'
        self.assertEqual(str, utils.pretty(str))
        
    def test_pretty_list(self):
        import utils
        Astr = '''ennie
meanie
mightie
'''
        A = ['ennie', 'meanie', 'mightie']
        self.assertEqual(Astr, utils.pretty(A))
        
    def test_pretty_dict(self):
        import utils
        Dstr = '''color: blue
shape: square
texture: groovy
'''
        D = {'shape': 'square', 'texture': 'groovy', 'color': 'blue'}
        self.assertEqual(Dstr, utils.pretty(D))

    def test_pretty_list_of_lists(self):
        import utils
        AAstr = '''a,b,c
d,e,f
g,h,i
'''
        AA = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g','h', 'i']]
        self.assertEqual(AAstr, utils.pretty(AA))

    def test_format_datetime(self):
        import utils
        d = datetime.datetime(2013,11,22,10,9,8)
        self.assertEqual(utils.format_datetime(d),
                         '11/22/2013 10:09 am')

    def test_format_datetime_with_sections(self):
        import utils
        d = datetime.datetime(2013,11,22,10,9,8)
        self.assertEqual(utils.format_datetime(d, with_seconds=1),
                         '11/22/2013 10:09:08 am')

    def test_format_datetime_ISO8601(self):
        import utils
        d = datetime.datetime(2013,11,22,10,9,8)
        self.assertEqual(utils.format_datetime(d, format='ISO8601'),
                         '2013-11-22T10:09:08Z')

def syntax():
    progname = os.path.basename(sys.argv[0])
    print
    print "  syntax: %s [%s]+" % (progname, ' | '.join(TEST_NAMES))
    print
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        syntax()

    if any(t not in TEST_NAMES for t in sys.argv[1:]):
        print "Test name must be one (or more) of:", ", ".join(TEST_NAMES)
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


