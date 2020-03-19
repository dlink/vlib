import sys
from io import StringIO

import unittest

from vlib.cli import CLI, CLI_Error

class TestCli(unittest.TestCase):
    '''Test Cli'''

    def setUp(self):
        commands = ['say <greeting>',
                    'add <n> <m>',
                    'list <n>',
                    'matrix <n> <m>',
                    'dict',
                    'time']
        self.cli = CLI(self.process, commands)

        # redirect stdout to a string
        self.old_stdout = sys.stdout
        sys.stdout = self.mystdout = StringIO()

    def tearDown(self):
        sys.stdout = self.old_stdout

    def process(self, *args):
        '''Process incoming requests'''
        args = list(args)
        if len(args) < 1:
            self.cli.syntax('missing args', return_no_exit=1)

        cmd = args.pop(0)
        if cmd == 'say':
            opt = args[0]
            return opt
        elif cmd == 'add':
            n = args[0]
            m = args[1]
            return int(n) + int(m)
        elif cmd == 'list':
            n = int(args.pop(0))
            return list(range(0, n))
        elif cmd == 'matrix':
            n = int(args.pop(0))
            m = int(args.pop(0))
            matrix = []
            for i in range(0, n):
                row = list(range(0, m))
                matrix.append(row)
            return matrix
        elif cmd == 'dict':
            return {'r': 'red', 'b': 'blue'}
        elif cmd == 'time':
            import datetime
            return datetime.datetime.now()
        else:
            raise CLI_Error('Unrecognized Command: %s' % cmd)

    def test_syntax(self):
        sys.argv = ['test_cli.py']
        retcode = self.cli.process(return_not_exit=1)
        self.assertEqual(retcode, 100)

    def test_syntax_with_emsg(self):
        sys.argv = ['test_cli.py']
        retcode = self.cli.syntax(emsg='some e-message', return_not_exit=1)
        self.assertEqual(retcode, 1)

    def test_badcmd_raise(self):
        sys.argv = ['test_cli.py', 'badcmd', '-v']
        retcode = None
        with self.assertRaises(CLI_Error):
            retcode = self.cli.process(return_not_exit=1)

    def test_badcmd_retcode(self):
        sys.argv = ['test_cli.py', 'badcmd']
        retcode = self.cli.process(return_not_exit=1)
        self.assertEqual(retcode, 100)


    def test_args_mssing(self):
        sys.argv = ['test_cli.py', 'say', '-v']
        with self.assertRaises(IndexError):
            self.cli.process(return_not_exit=1)

    def test_two_args(self):
        sys.argv = ['test_cli.py', 'say', 'hi']
        retcode = self.cli.process(return_not_exit=1)
        self.assertEqual(retcode, 0)

    def test_return_list(self):
        sys.argv = ['test_cli.py', 'list', '5']
        retcode = self.cli.process(return_not_exit=1)
        self.assertEqual(retcode, 0)

    def test_return_list_of_list(self):
        sys.argv = ['test_cli.py', 'matrix', '2', '3']
        retcode = self.cli.process(return_not_exit=1)
        self.assertEqual(retcode, 0)

    def test_return_dict(self):
        sys.argv = ['test_cli.py', 'dict']
        retcode = self.cli.process(return_not_exit=1)
        self.assertEqual(retcode, 0)

    def test_quiet(self):
        sys.argv = ['test_cli.py', 'say', 'hi' '-q']
        retcode = self.cli.process(return_not_exit=1)
        self.assertEqual(retcode, 0)
