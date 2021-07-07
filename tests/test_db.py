#!/bin/env python

from vlib import conf
from vlib import db

class TestError(Exception): pass

class Test():
    '''Test Db'''

    def __init__(self):
        print('test.__init__()')
        self.db = db.getInstance()

    def run(self):
        print('test.run()')
        print()
        print(1)
        self.test_query()
        print()
        print(2)
        self.test_query()
        
    def test_query(self):
        sql = 'select book_name from books where book_id = 1'
        results = self.db.query(sql)
        print('results:',results)
        
if __name__ == '__main__':
    test = Test()
    test.run()
