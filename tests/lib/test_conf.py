import unittest

# Fixtures
DATABASE_ENGINE='mysql'
SHELL='/bin/bash'
SECRET='toyboat$'

class TestConf(unittest.TestCase):
    '''Test Conf'''

    def setUp(self):
        from vlib import conf
        self.conf = conf.getInstance()

    def test_getvar(self):
        self.assertEqual(self.conf.database.engine, DATABASE_ENGINE)

    def test_getvar_withenvvar(self):
        self.assertEqual(self.conf.shell, SHELL)

    def test_getvar_withescaping(self):
        self.assertEqual(self.conf.secret, SECRET)
