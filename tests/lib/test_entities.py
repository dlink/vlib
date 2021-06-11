import unittest

from vlib import entities

class TestEntities(unittest.TestCase):

    def test_toEntity(self):
        TESTS = (('Text', 'Text'),
                 ('<', '&lt;'),
                 ('>', '&gt;'),
                 ('&', '&amp;'),
                 ('\u00a9', '&#169;'), # copyright symbol
                 )
        for s, d in TESTS:
            self.assertEqual(entities.toEntity(s), d)
