import unittest

from vlib import db
from vlib.datarecord import DataRecord

class TestDataRecord(unittest.TestCase):
    '''Test DataRecord'''

    def setUp(self):
        self.db = db.getInstance()

    def testLoad(self):
        book = DataRecord(self.db, 'books', 1, primary_key='book_id')
        self.assertEqual(book.book_name, 'baranoff')

