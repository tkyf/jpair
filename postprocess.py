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

def make_all_sub_list(co, ic, all=False):
    """[FUNCTIONS]ファイルオープン、差分作成を行う。

    Return value:
    g_sub_list [[元の表現, [後の表現], 出現行番号]]  :: [unicode, [MorphedChar], unicode]
    """

    def is_revised(sub):
        """ペアに添削が行われているかどうかを判定する。
        ペアが等しい場合、false。異なっている場合、true
        """
        after = u''
        if sub[1]:
            for morphedchar in sub[1]:
                after += morphedchar.surface
        if sub[0] or after:
            return sub[0] != after
        return False

    def is_insertion(sub):
        """ペアが挿入操作かどうかを判定する。
        学習者の表現が存在しない場合、挿入だと判定される。
        """
        return not bool(sub[0])

    import sys

    g_sub_list = []
    ed = edit_distance.EditDistance()

    with nested(codecs.open(co, 'r', 'utf-8'), codecs.open(ic, 'r', 'utf-8')) as (corrs, incors):
        for row, (corr, incor) in enumerate(zip(corrs, incors)):
            corr = corr.strip().replace(u' ', '').replace(u'　', '')
            incor = incor.strip().replace(u' ', '').replace(u'　', '')

            sub_list = ed.word_sub_extract(incor, corr)

            if sub_list is None:
                continue

            if all:
                pass
            else:
                # 変化のないペアを取り除く
                sub_list = filter(is_revised, sub_list)

                # 挿入操作のペアを取り除く
                sub_list = filter(lambda x:not is_insertion(x), sub_list)


            sub_list.append(unicode(row + 1))
            g_sub_list.append(sub_list)

            if row != 0 and row % 10000 == 0:
                print('row:' + str(row), file=sys.stderr)

    return g_sub_list

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


