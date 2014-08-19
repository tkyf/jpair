#coding: utf-8

import unittest

import edit_distance

class Test(unittest.TestCase):
    def setUp(self):
        self.ed = edit_distance.EditDistance(is_test=True)
        self.corr = []
        self.incor = []
        self.corr.append(u"こんにちは。わたしはげんきです。")
        self.incor.append(u"こにちわ。わちしはげんきでした。")

    def test_sub(self):
        expects = [("こんにちは", "こにちわ", "感動詞"),("わたし","わちし", "名詞-代名詞-一般"),
                ("です", "でした", "助動詞")]

    def test_editdistance(self):
        d = self.ed.shortest_edit_script(self.incor[0], self.corr[0])  
        self.assertEqual(d, 8)
        


if __name__ == '__main__':
    unittest.main()

