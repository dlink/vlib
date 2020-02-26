import unittest

class TestOdict(unittest.TestCase):
    def test_odict(self):
        from vlib.odict import odict, OdictError
        COLOR = 'red'
        d = odict(color=COLOR)
        self.assertEqual(d.color, COLOR)
        with self.assertRaises(OdictError):
            d.non_existent_field

