# coding: utf-8

import codecs
import glob
import os
import os.path
import copy

# for python 2.6
from contextlib import nested

import edit_distance


def main():
    """[FUNCTIONS]
    品詞情報ありの差分ペアを作る。
    差分ペアは単語単位で取れる。
    """
    import sys
    try: 
        import argparse
        parser = argparse.ArgumentParser(description="Extract revision pairs from Japanese text pair.")
        parser.add_argument("-c", "--co", dest="co", help="Correction File")
        parser.add_argument("-i", "--ic", dest="ic", help="Learner File")
        parser.add_argument("-l", "--all", dest="all", action="store_true", help="Output includes ALL word pairs.(includes Insertion, Subusutitution, Deletion and No Revision)")
        parser.add_argument("-d", "--distance", dest="distance", action="store_true", help="Get edit distacne")
        parser.add_argument("-n", "--nopos", dest="nopos", action="store_true", help="Without pos")
        parser.add_argument("-a", "--addtag", dest="add_tag", action="store_true", help="add tag to replaced word")

        (args, options) = parser.parse_args()

    # for python 2.6
    except ImportError:
        import optparse
        parser = optparse.OptionParser(description="Extract revision pairs from Japanese text pair.")
        parser.add_option("-c", "--co", dest="co", help="Correction File")
        parser.add_option("-i", "--ic", dest="ic", help="Learner File")
        parser.add_option("-l", "--all", dest="all", action="store_true", help="Output includes ALL word pairs.(includes Insertion, Subusutitution, Deletion and No Revision)")
        parser.add_option("-d", "--distance", dest="distance", action="store_true", help="Get edit distacne")
        parser.add_option("-n", "--nopos", dest="nopos", action="store_true", help="Without pos")
        parser.add_option("-a", "--addtag", dest="add_tag", action="store_true", help="add tag to replaced word")

        (args, options) = parser.parse_args()

    if not args or args.co is None or args.ic is None:
        parser.print_help()
        exit(-1)

    if args.distance:
        get_distance(args.co, args.ic)
    else:

        g_sub_list = make_all_sub_list(args.co, args.ic, args.all)

        to_write_list = make_to_write(g_sub_list, args.nopos, args.add_tag)

        for to_write in to_write_list:
            print to_write.encode('utf-8')


def get_distance(co, ic):
    ed = edit_distance.EditDistance(is_test=True)
    with nested(codecs.open(co, 'r', 'utf-8'), codecs.open(ic, 'r', 'utf-8')) as (corrs, incors):
        for row, (corr, incor) in enumerate(zip(corrs, incors)):
            corr = corr.strip().replace(u' ', '').replace(u'　', '')
            incor = incor.strip().replace(u' ', '').replace(u'　', '')   
            distance = ed.shortest_edit_script(incor, corr)
            print row, distance

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
                print >>sys.stderr, 'row:' + str(row)

    return g_sub_list


def make_to_write(g_sub_list, nopos, add_tag):

    def morphed_char_joining(morphed_char_list):
        """[FUNCTIONS] MorphedCharとして別の文字にわかれてる単語をくっつける。
        ここでの返り値の MorphedChar には、単語を返す場合、複数の文字が入る。

        Return value:
        morphed_word_list :: [MorphedChar]
        """
        # 削除操作の場合
        if morphed_char_list == []:
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

    splitter = u'\t'

    to_write_list = []

    for sub_list in g_sub_list:
        dup_sub_list = copy.deepcopy(sub_list)
        row = dup_sub_list[-1]

        to_write_local = []
        for sub in dup_sub_list[:-1]:

            morphed_char_list = sub[1]
            morphed_word_list = morphed_char_joining(morphed_char_list)

            after_word = u' '.join(morphed_word_list)
            before_word = sub[0]

            if add_tag and before_word != after_word:
                before_word = "<goyo crr=\"%s\">%s</goyo>" % (after_word, before_word)

            to_write = splitter.join([row, before_word , after_word])
            to_write_local.append(to_write)

        to_write_list += to_write_local

    return to_write_list

if __name__ == "__main__":
    main()
