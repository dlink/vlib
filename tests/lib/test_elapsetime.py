import unittest

from vlib.elapsetime import ElapseTime

class TestElapseTime(unittest.TestCase):

    def test_elapsetime(self):
        e = ElapseTime()
        self.assertTrue(e.seconds>0)
        self.assertTrue(e.ms>0)

        # reset
        e.reset()
        self.assertTrue(e.seconds>0)
