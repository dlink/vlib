import unittest
import re

import vlib.sqlutils

class TestSqlUtils(unittest.TestCase):
    '''Given sql statements already in pretty format
       remove formating, reformat, and then compare.
    '''

    def test_sql_pretty1(self):
        self.do_test(1)

    def test_sql_pretty2(self):
        self.do_test(2)

    def do_test(self, test_num):
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
        
