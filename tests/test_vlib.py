#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import sys

DEBUG = 0

TEST_NAMES = ('All', 'Conf', 'DataTable', 'Db', 'Shell')


# Fixtures
COLUMNDEF_FILENAME='fixtures/datatable_columndefs'
 
class TestConf(unittest.TestCase):
    '''Test Conf'''
    
    def setUp(self):
        import conf
        self.conf = conf.Factory.create().data
        
    def test_getvar(self):
        self.assertEqual(self.conf['database']['engine'], 'mysql')
        
    def test_getvar_withenvvar(self):
        self.assertEqual(self.conf['shell'], '/bin/bash')
        
class TestDataTable(unittest.TestCase):
    '''Test DataTable'''

    def setUp(self):
        import db
        from datatable import DataTable
        
        self.db = db.Factory().create()
        self.datatable = DataTable(self.db, 'disciplines')

    def test_columnDefs(self):
        results = self.datatable.columnDefs()
        new = '\n'.join(map(str, results))
        old = open(COLUMNDEF_FILENAME, 'r').read()
        self.assertEqual(new, old)

class TestDb(unittest.TestCase):
    '''Test Db'''

    def setUp(self):
        import db

        self.db = db.Factory().create()

    def test_query(self):
        sql = 'select book_name from books where book_id = 1'
        results = self.db.query(sql)
        self.assertEqual(results[0]['book_name'], 'baranoff')

class TestShell(unittest.TestCase):
    def setUp(self):
        from shell import Shell
        self.shell = Shell()
        
    def test_ls(self):
        output = self.shell.cmd('ls')

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


