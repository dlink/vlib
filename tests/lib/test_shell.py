import unittest

from vlib.shell import Shell

class TestShell(unittest.TestCase):
    def setUp(self):
        self.shell = Shell()

    def test_ls(self):
        output = self.shell.cmd('ls')
