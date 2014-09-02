# coding: utf-8

from __future__ import print_function
import codecs
# for python 2.6
from contextlib import nested

import edit_distance

def remove_spaces(string):
    return string.strip().replace(u' ', '').replace(u'　', '')

def get_distance(co, ic):
    ed = edit_distance.EditDistance()
    with nested(codecs.open(co, 'r', 'utf-8'), codecs.open(ic, 'r', 'utf-8')) as (corrs, incors):
        for row, (corr, incor) in enumerate(zip(corrs, incors)):
            corr = remove_spaces(corr)
            incor = remove_spaces(incor)
            distance = ed.shortest_edit_script(incor, corr)
            print(row, distance)

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

    g_sub_list = []
    ed = edit_distance.EditDistance()

    with nested(codecs.open(co, 'r', 'utf-8'), codecs.open(ic, 'r', 'utf-8')) as (corrs, incors):
        for row, (corr, incor) in enumerate(zip(corrs, incors)):
            corr = remove_spaces(corr)
            incor = remove_spaces(incor)

            sub_list = ed.extract_word_sub(incor, corr)

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

