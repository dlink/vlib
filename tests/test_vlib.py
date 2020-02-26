#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import sys

from lib.test_attribute import TestAttribute
from lib.test_conf import TestConf
from lib.test_datarecord import TestDataRecord
from lib.test_datatable import TestDataTable
from lib.test_db import TestDb
from lib.test_odict import TestOdict
from lib.test_sqlutils import TestSqlUtils
from lib.test_shell import TestShell
from lib.test_utils import TestUtils

DEBUG = 0

TEST_NAMES = ('All', 'Attribute', 'Conf', 'DataTable', 'DataRecord', 'Db',
              'Odict', 'Shell', 'Utils', 'SqlUtils')

def syntax():
    progname = os.path.basename(sys.argv[0])
    print()
    print("  syntax: %s [%s]+" % (progname, ' | '.join(TEST_NAMES)))
    print()
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        syntax()

    # validate
    if any(t not in TEST_NAMES for t in sys.argv[1:]):
        print("Test name must be one (or more) of:", ", ".join(TEST_NAMES))
        sys.exit(1)

    # all or some
    if  sys.argv[1] == 'All':
        test_names = TEST_NAMES[1:]
    else:
        test_names = sys.argv[1:]

    # eval tests
    tests = []
    for test_name in test_names:
        tests.append(eval('Test%s' % test_name))

    # run suite of tests
    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    suite.addTests([loader(t) for t in tests])

    unittest.TextTestRunner(verbosity=2).run(suite)
