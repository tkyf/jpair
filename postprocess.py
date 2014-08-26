# coding: utf-8

from __future__ import print_function

import codecs
import glob
import os
import os.path
import copy


# for python 2.6
from contextlib import nested

import edit_distance

def morphed_char_joining(morphed_char_list, nopos):
    """[FUNCTIONS] 文字単位のMorphedCharのリストを単語単位に結合する。
    結合の基準として、MorphedCharのpositionアトリビュートを使用する。

    Return value:
    morphed_word_list :: [MorphedChar]
    """

    if not morphed_char_list:
        return []

    morphed_word_list = []

    # 下のfor文内で、一つ前までに出てきた文字列(MorphedChar)を表す。
    # 次に出てきた文字のpositionがIだったらくっつける。という操作の判定に使う
    latest_word = None

    for mc in morphed_char_list:
        if latest_word is None:
            latest_word = mc
        else:
            if mc.position == 'B':
                if nopos:
                    s = u"%s" % (latest_word.surface)
                else:
                    s = u"%s %s" % (latest_word.surface,
                            latest_word.pos)
                morphed_word_list.append(s)
                latest_word = mc
            elif mc.position == 'I':
                latest_word.surface += mc.surface
    if nopos:
        s = u"%s" % (latest_word.surface)
    else:
        s = u"%s %s" % (latest_word.surface,
                latest_word.pos)
    morphed_word_list.append(s)
    return morphed_word_list



def make_to_write(g_sub_list, nopos, add_tag):

    splitter = u'\t'

    to_write_list = []

    for sub_list in g_sub_list:
        dup_sub_list = copy.deepcopy(sub_list)
        row = dup_sub_list[-1]

        to_write_local = []
        for sub in dup_sub_list[:-1]:

            morphed_char_list = sub[1]
            morphed_word_list = morphed_char_joining(morphed_char_list, nopos)

            after_word = u' '.join(morphed_word_list)
            before_word = sub[0]

            if add_tag and before_word != after_word:
                before_word = "<goyo crr=\"%s\">%s</goyo>" % (after_word, before_word)

            to_write = splitter.join([row, before_word , after_word])
            to_write_local.append(to_write)

        to_write_list += to_write_local

    return to_write_list


