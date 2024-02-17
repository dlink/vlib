import unittest

from vlib.odict import odict

# fixtures
COLOR = 'red'
DATA = odict(color=COLOR)

class TestOdict(unittest.TestCase):
    def test_odict(self):
        self.assertEqual(DATA.color, COLOR)
        with self.assertRaises(AttributeError):
            DATA.non_existent_field
