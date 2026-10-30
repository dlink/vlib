import unittest
from unittest.mock import Mock, patch

from vlib.datarecord import DataRecord, DataRecordNotFound

class Book(DataRecord):
    def __init__(self, key, language='en'):
        self.language = language
        DataRecord.__init__(self, None, 'books', key, primary_key='book_id')

class TestDataRecordFind(unittest.TestCase):
    '''Find records without using database connections.'''

    def setUp(self):
        table_patch = patch('vlib.datarecord.DataTable.__init__',
                            return_value=None)
        table_patch.start()
        self.addCleanup(table_patch.stop)
        load_patch = patch.object(DataRecord, '_loadData')
        self.load = load_patch.start()
        self.addCleanup(load_patch.stop)

    def test_find_returns_record_and_forwards_constructor_arguments(self):
        db = Mock()
        book = DataRecord.find(db, 'books', 1, primary_key='book_id')
        self.assertIsInstance(book, DataRecord)
        self.assertIs(book.db, db)
        self.assertEqual(book.table, 'books')
        self.assertEqual(book.id, 1)
        self.assertEqual(book.primary_key, 'book_id')
        self.load.assert_called_once_with()

    def test_subclass_inherits_find_and_returns_subclass(self):
        book = Book.find('book_name="Example"', language='fr')
        self.assertIsInstance(book, Book)
        self.assertEqual(book.id, 'book_name="Example"')
        self.assertEqual(book.language, 'fr')

    def test_find_returns_none_for_missing_record(self):
        self.load.side_effect = DataRecordNotFound('No matching book')
        self.assertIsNone(Book.find(1))

    def test_constructor_still_raises_for_missing_record(self):
        self.load.side_effect = DataRecordNotFound('No matching book')
        with self.assertRaises(DataRecordNotFound):
            Book(1)

    def test_find_does_not_hide_other_errors(self):
        error = RuntimeError('Database unavailable')
        self.load.side_effect = error
        with self.assertRaises(RuntimeError) as raised:
            Book.find(1)
        self.assertIs(raised.exception, error)
