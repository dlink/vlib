import unittest

class TestDataRecord(unittest.TestCase):
    '''Test DataRecord'''

    def setUp(self):
        from vlib import db
        self.db = db.getInstance()

    def testLoad(self):
        from vlib.datarecord import DataRecord
        book = DataRecord(self.db, 'books', 1, primary_key='book_id')
        self.assertEqual(book.book_name, 'baranoff')

