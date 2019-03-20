import os
import unittest

import xmlrunner

import learn.learn_unit as t

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(t.Test))
    runner = unittest.TextTestRunner()
    runner.run(suite)

