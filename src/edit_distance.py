# -*- coding: utf-8 -*-
from __future__ import print_function

# 編集タグ
EQ_TAG =  '.'
ADD_TAG = '+'
del_tag = '-'
SUB_TAG = '/'

class EditDistance(object):

    def __init__(self, is_test=False):
        """
        is_test    -- True を指定すると、途中経過を表示する。
        """

        self.is_test = is_test

    def build_edit_graph(self, src, dst):
        """[FUNCTIONS] 二つの文字列間のエディットグラフを作る。
        置換の距離は2。

        Keyword argument:
        src -- 1つ目の文。例：学習者の文  :: unicode
        dst -- 2つ目の文。例：添削文      :: unicode

        Return value:
        edit_graph  :: [[int]]
        """
        # DPで使うエディットグラフ用の2次元配列の初期化。
        # サイズは系列src,dstの文字数+1(("","")があるため)
        m = [[0] * (len(dst)+1) for i in range(len(src) +1)]

        # LD(i,0)となる自明な箇所の初期化
        for i in xrange(len(src) + 1):
            m[i][0] = i

        # LD(0,j)となる自明な箇所の初期化
        for j in xrange(len(dst)+1):
            m[0][j] = j

        # エディットグラフの値を埋める。
        for i in xrange(1, len(src) + 1):
            for j in xrange(1, len(dst) + 1):
                if src[i - 1] == dst[j - 1]:
                    x = 0
                else:
                    x = 2
                m[i][j] = min(m[i-1][j] + 1, m[i][j - 1] + 1, m[i - 1][j - 1] + x)

        if self.is_test:
            print(', '.join(' ' + dst))
            for s, l in zip(' ' + src, m):
                print(s, l)
            print("")

            print('len(src) = ' + str(len(src)))
            print('i = ' + str(i))# i, jは最後の値になっていることを確認
            print('len(dst) = ' + str(len(dst)))
            print('j = ' + str(j))
            print('[i][j] = ' + str(m[i][j]))

            print('len(m) = ' + str(len(m)))
            print('len(m[0]) = ' + str(len(m[0])))

        return m


    def build_edit_trail(self, src, dst):
        """[FUNCTIONS] エディットグラフを終端（最も右下）から左上にたどり、
        二つの文の編集履歴を得る。編集履歴は'add', 'del', 'eq'のリスト。

        Keyword arguments:
        src        -- 1つ目の文。例：学習者の文  :: unicode
        dst        -- 2つ目の文。例：添削文      :: unicode
        """
        m = self.build_edit_graph(src, dst)

        #最後からたどるために、最も右下のインデックスを得る
        now_i = len(m) - 1
        now_j = len(m[0]) - 1
        now = m[now_i][now_j]

        edit_trail = [] # 逆からたどった経路
        while(now_i > 0 or now_j > 0):
            up_num = m[now_i - 1][now_j]
            diagonal_num = m[now_i -1][now_j - 1]
            left_num = m[now_i][now_j - 1]

            # 優先順位は eq(diagonal), del(up), add(left)の順
            min_list = [ diagonal_num, up_num, left_num]
            min_num = min(min_list)
            min_index = min_list.index(min_num)
            # これで、左・斜め・上のどのスコアが最も小さいか分かった。

            # エディットグラフの上端に到達しているときはそのまま左に進む
            if now_i == 0:
                now_j -= 1
                edit_trail.append('add')
            # 左端に到達しているときはそのまま上に進む
            elif now_j == 0:
                now_i -= 1
                edit_trail.append('del')
            # 斜めはeqの時だけたどる（置換は考えない）
            elif min_index == 0 and min_num == now:
                now_i -= 1
                now_j -= 1
                edit_trail.append('eq')
            else:
                #if left_num <= up_num:
                if min_index == 2:
                    now_j -= 1
                    edit_trail.append('add')
                else:
                    now_i -= 1
                    edit_trail.append('del')
            now = m[now_i][now_j]

        # 左上からの編集履歴を得るために、reverseする。
        return list(reversed(edit_trail))


    def build_edit_rev(self, src, dst):
        """[FUNCTIONS] 編集タグ、変更前文字列、変更後文字列の三つ組を作る。

        Keyword arguments:
        src        -- 1つ目の文。例：学習者の文  :: unicode
        dst        -- 2つ目の文。例：添削文      :: unicode

        Return value:
        (tag_str, src_str, dst_str)

        例： "いあいあ", "ああえ"の場合
        tag_str = -.-.+
        src_ist = いあいあ＿
        dst_str = ＿あ＿あえ
        """

        edit_trail = self.build_edit_trail(src, dst)

        src_index = 0
        dst_index = 0
        tag_str = u''
        src_str = u''
        dst_str = u''
        for i, e in enumerate(edit_trail):
            if e == 'eq':
                tag_str += EQ_TAG
                src_str += src[src_index]
                dst_str += dst[dst_index]
                if self.is_test:
                    print('eq  :' + src[src_index] + '->' \
                          + dst[dst_index] + '(' + str(dst_index) + ')')
                src_index += 1
                dst_index += 1
            elif e == 'add':
                tag_str += ADD_TAG
                src_str += u'＿'
                dst_str += dst[dst_index]
                if self.is_test:
                    print('add :' + u'＿' + '->' + dst[dst_index] \
                          + '(' + str(dst_index) + ')')
                dst_index += 1
            elif e == 'del':
                tag_str += del_tag
                src_str+= src[src_index]
                dst_str += u'＿'
                if self.is_test:
                    print('del :' + src[src_index] + '->' \
                          + u'＿' + '(' + str(dst_index) + ')')
                src_index += 1
            elif e == 'sub':
                tag_str += SUB_TAG
                src_str += src[src_index]
                dst_str += dst[dst_index]
                if self.is_test:
                    print('sub :' + src[src_index] + '->' \
                          + dst[dst_index] + '(' + str(dst_index) + ')')
                src_index += 1
                dst_index += 1
            else:
                print('this tag is not defiened')

        if self.is_test:
             print(tag_str)
             print(src_str)
             print(dst_str)
        
        return (tag_str, src_str, dst_str)


    def blank_insert(self, dst_str, morphed_chars):
        """[FUNCTIONS] morphed_charsにdst_strと同じ位置に＿を挿入する。 
        dst_strはbuild_edit_rev関数で処理された形式とする。

        """
        import morph_char 

        for i, d in enumerate(dst_str):
            if d == u'＿':
                morphed_chars.insert(i, morph_char.MorphedChar(u'＿', u'X', u'X'))


    def extract_word_sub(self, src, dst):
        """[FUNCTIONS] 二つの文の置換された箇所のペアのリストを作る。
        そのとき、挿入された側を単語単位で抜き出すよう整形する。

        Keyword arguments:
        src        -- 1つ目の文。例：学習者の文  :: unicode
        dst        -- 2つ目の文。例：添削文      :: unicode

        Return value:
        [(src_strでの表現, dst_strでの表現)]  :: [(unicode, [MorphedChar])]
        """

        from morph_char import str_to_morphed_chars

        edit_rev_triple = self.build_edit_rev(src, dst)
        dst_morphed_chars = str_to_morphed_chars(dst)

        sub_list = []

        # 2つ目の文をMorphedCharのリストに置き換える。
        # その時、添削による＿を反映させる。
        tag_str, src_str, dst_str = edit_rev_triple
        self.blank_insert(dst_str, dst_morphed_chars)

        word_begin = 0
        word_end   = 0
        in_word    = False
        for i, (t, s, d) in enumerate(zip(tag_str,src_str,
                                          dst_morphed_chars)):
            if in_word:
                if d.position == u'B':
                    if t == ADD_TAG and tag_str[i-1] != EQ_TAG:
                        pass
                    else:
                        word_end   = i
                        sub_list.append([src_str[word_begin:word_end], 
                            dst_morphed_chars[word_begin:word_end]])
                        word_begin = i
            else:
                if d.position == u'B':
                    in_word = True
                    word_begin = i

        sub_list.append([src_str[word_begin:], 
            dst_morphed_chars[word_begin:]])

        sub_list = self.blank_delete(sub_list)

        return sub_list

    def blank_delete(self, sub_list):
        """trim u'＿' from sub_list"""
        clear_sub_list = []
        for sub in sub_list:
            before = sub[0].replace(u'＿', u'')
            after = []
            for morphedchar in sub[1]:
                if morphedchar.surface == u'＿':
                    pass
                else:
                    after.append(morphedchar)
            clear_sub_list.append(tuple([before, after]))
        return clear_sub_list


    def shortest_edit_script(self, src, dst):
        """[FUNCTIONS] 二つの文字列の編集距離を返す。
        置換は編集距離2と考える。
        Keyword argument:
        src    -- 文字列その1。例えば、学習者の文。 :: unicode
        dst    -- 文字列その2。例えば、添削文。     :: unicode

        Return value:
        edit_distance :: int
        """

        edit_graph = self.build_edit_graph(src, dst)
        return edit_graph[-1][-1]

