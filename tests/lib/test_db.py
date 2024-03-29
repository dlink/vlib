import unittest
import datetime

from vlib import conf
from vlib import db

class TestError(Exception): pass

class TestDb(unittest.TestCase):
    '''Test Db'''

    def setUp(self):
        self.db = db.getInstance()

    def test__repr__(self):
        A='vlib.db.Db:vlibtests'
        B=str(self.db)
        self.assertEqual(A, B)

    def test_query(self):
        sql = 'select book_name from books where book_id = 1'
        results = self.db.query(sql)
        self.assertEqual(results[0]['book_name'], 'baranoff')

    def test_rowcount(self):
        sql = "update books set subtitle = 'test' where book_id <= 2"
        results = self.db.query(sql)
        rowcount = self.db.rowcount
        self.assertEqual(rowcount, 2)
        sql = "update books set subtitle = null where book_id <= 2"
        results = self.db.query(sql)

    def test_timezone(self):
        sql = 'select @@session.time_zone as time_zone'
        db_timezone = self.db.query(sql)[0]['time_zone']
        self.assertEqual(conf.getInstance().database.timezone, db_timezone)

    def test_timezone_same_as_localhost(self):
        sql = 'SELECT date_format(now(), "%Y-%m-%d %H:%i") as now;'
        db_datetime = self.db.query(sql)[0]['now']
        localhost_datetime = \
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M").lower()
        self.assertEqual(localhost_datetime, db_datetime)

    def test_rollback(self):
        max_book_id = self._getMaxBookId()
        self.db.startTransaction()
        try:
            sql = 'insert into books (book_name) value ("Unit Test Book")'
            self.db.execute(sql)
            raise TestError('Test Error')
        except TestError as e:
            self.db.rollback()
        except Exception as e:
            raise
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

