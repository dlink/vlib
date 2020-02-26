import unittest

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


