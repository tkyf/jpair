#encoding: utf-8
from __future__ import print_function

import MeCab

pos_index = 0
try:
    tagger = MeCab.Tagger('-Ochasen')
    pos_index = 3
except RuntimeError:
    tagger = MeCab.Tagger('-Ounidic')
    pos_index = 4

class MorphedChar:
    """[CLASSES] 形態素解析された一つの文字を表す．
    この文字は品詞と単語中での位置を持つ
    """
    def __init__(self, surface, pos, position):
        """[FUNCTIONS] 文字の表層、品詞、単語内での位置を受け取り格納する

        Keyword arguments:
        sruface -- surface of charactor : unicode
        pos     -- surface of word      : unicode
        position -- position of charactor in word. :unicode 
                    B: begin of word. I: inter of word.

        例： surface  : 人
             pos      : 名詞
             position : B 
        """

        self.surface = surface
        self.pos = pos
        self.position = position  # B:先頭，I:文中

def str_to_morphed_chars(src):
    """[FUNCTIONS]文字列を受け取り，MeCabで形態素解析して、
    MorphedCharのリストにして返す

    Keyword arguments:
    src       -- 文字列

    Return value:
    [MorphedChar]
 
    """
    if isinstance(src, unicode):
        morphed = tagger.parse(src.encode('utf_8'))
    elif isinstance(src, str):
        morphed = tagger.parse(src)

    morphed = unicode(morphed, 'utf_8')

    splited = morphed.split(u'\n')

    cs = []
    for l in splited:
        if l.startswith(u'EOS'):
            break
        feature = l.split(u'\t')
        cs.append(MorphedChar(feature[0][0], feature[pos_index], u'B'))

        n = len(feature[0])
        if n > 1: #2文字以上からなる単語の場合
            for i in xrange(0, n - 1):
                cs.append(MorphedChar(feature[0][i+1], feature[pos_index], u'I'))
    return cs

def main():
    src = u'庭には二羽にわとりがいる'
    print(src)
    morphed_chars = str_to_morphed_chars(src)
    for morphed_char in morphed_chars:
        print(morphed_char.surface.encode('cp932') , morphed_char.pos.encode('cp932') , morphed_char.position.encode('cp932'))


if __name__ == "__main__":
    main()


