import unittest

class TestShell(unittest.TestCase):
    def setUp(self):
        from vlib.shell import Shell
        self.shell = Shell()

    def test_ls(self):
        output = self.shell.cmd('ls')
