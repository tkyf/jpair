#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

# for python 2.6
from contextlib import nested

import preprocess
import postprocess


def main():
    """[FUNCTIONS]
    品詞情報ありの差分ペアを作る。
    差分ペアは単語単位で取れる。
    """
    import sys
    # for python 2.6
    import optparse

    parser = optparse.OptionParser(description="Extract revision pairs from Japanese text pair.")
    parser.add_option("-c", "--co", dest="co", help="Correction File")
    parser.add_option("-i", "--ic", dest="ic", help="Learner File")
    parser.add_option("-l", "--all", dest="all", action="store_true", help="Output includes ALL word pairs.(includes Insertion, Subusutitution, Deletion and No Revision)")
    parser.add_option("-d", "--distance", dest="distance", action="store_true", help="Get edit distacne")
    parser.add_option("-n", "--nopos", dest="nopos", action="store_true", help="Without pos")
    parser.add_option("-a", "--addtag", dest="add_tag", action="store_true", help="add tag to replaced word")

    (opts, args) = parser.parse_args()

    if not opts:
        parser.print_help()
        exit(-1)

    if  opts.co is None or opts.ic is None:
        parser.print_help()
        exit(-1)

    # 処理が編集距離の場合 
    if opts.distance:
        preprocess.get_distance(opts.co, opts.ic)
    else:
        g_sub_list = preprocess.make_all_sub_list(opts.co, opts.ic, opts.all)
        to_write_list = postprocess.make_to_write(g_sub_list, opts.nopos, opts.add_tag)

        for to_write in to_write_list:
            print(to_write.encode('utf-8'))

if __name__ == "__main__":
    main()

