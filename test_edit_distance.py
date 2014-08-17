#coding: utf-8

import unittest

import edit_distance

class Test(unittest.TestCase):
    def setUp(self):
        self.ed = edit_distance.EditDistance(is_test=True)

    def testEditdistance(self):
        pass


if __name__ == '__main__':
    unittest.main()

