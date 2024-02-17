import unittest
from datetime import datetime

import vlib.utils

class TestUtils(unittest.TestCase):

    def test_validate_num_args(self):
        S, NUM_ARGS, ARGS = 'test cmd', 1, ('a')
        BAD_ARGS = ()
        self.assertIsNone(vlib.utils.validate_num_args(S, NUM_ARGS, ARGS))
        with self.assertRaises(vlib.utils.MissingArguments):
            vlib.utils.validate_num_args(S, NUM_ARGS, BAD_ARGS)

        S, NUM_ARGS, ARGS = 'test cmd', 2, ('a', 'b')
        BAD_ARGS = ('a')
        self.assertIsNone(vlib.utils.validate_num_args(S, NUM_ARGS, ARGS))
        with self.assertRaises(vlib.utils.MissingArguments):
            vlib.utils.validate_num_args(S, NUM_ARGS, BAD_ARGS)

    def test_uniqueId(self):
        self.assertIsNotNone(vlib.utils.uniqueId())
        self.assertIsNotNone(vlib.utils.uniqueId(with_millisec=True))

    def test_str2datetime(self):
        S = '2010-11-11 17:39:52'
        D = datetime(2010, 11, 11, 17, 39, 52)
        self.assertEqual(vlib.utils.str2datetime(S), D)

        S = '2010-11-11'
        D = datetime(2010, 11, 11)
        self.assertEqual(vlib.utils.str2datetime(S), D)
        
        S = 'mud'
        D = datetime(2010, 11, 11)
        with self.assertRaises(vlib.utils.Str2DateError):
            vlib.utils.str2datetime(S)

    def test_pretty_str(self):
        str = 'This is a string'
        self.assertEqual(str, vlib.utils.pretty(str))

    def test_pretty_list(self):
        Astr = '''ennie
meanie
mightie'''
        A = ['ennie', 'meanie', 'mightie']
        self.assertEqual(Astr, vlib.utils.pretty(A))

    def test_pretty_dict(self):
        Dstr = '''color: blue
shape: square
texture: groovy'''
        D = {'shape': 'square', 'texture': 'groovy', 'color': 'blue'}
        self.assertEqual(Dstr, vlib.utils.pretty(D))

    def test_pretty_list_of_lists(self):
        AAstr = '''a,b,c
d,e,f
g,h,i'''
        AA = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g','h', 'i']]
        self.assertEqual(AAstr, vlib.utils.pretty(AA))

    def test_format_datetime(self):
        d = datetime(2013,11,22,10,9,8)
        self.assertEqual(vlib.utils.format_datetime(d),
                         '11/22/13 10:09 am')

    def test_format_datetime_with_sections(self):
        d = datetime(2013,11,22,10,9,8)
        self.assertEqual(vlib.utils.format_datetime(d, with_seconds=1),
                         '11/22/13 10:09:08 am')

    def test_format_datetime_ISO8601(self):
        d = datetime(2013,11,22,10,9,8)
        self.assertEqual(vlib.utils.format_datetime(d, format='ISO8601'),
                         '2013-11-22T10:09:08-05:00')

    def test_format_datetime_ISO8601_without_time(self):
        d = datetime(2013,11,22)
        self.assertEqual(vlib.utils.format_datetime(d, format='ISO8601'),
                         '2013-11-22T00:00:00-05:00')

