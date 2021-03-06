jpair
=====

正しい文と、誤りを含む文を入力し、
相違点を単語単位で出力するツールです。

### 例

正しい文：　　　こんにちは。わたしはげんきです。

誤りを含む文：　*こにちわ*。*わちし*はげんき*でした*。

出力：　

    1　こにちわ　こんにちは　感動詞-一般
    1　わちし　　わたし　　　代名詞
    1　でした  　です　　　　助動詞

## 動作環境
Python の以下のバージョンで動作確認済

+ 2.7.4
+ 2.7.3
+ 2.6.6


## 必要要件
[MeCab](http://mecab.googlecode.com/svn/trunk/mecab/doc/index.html) の [Python バインディング](http://mecab.googlecode.com/svn/trunk/mecab/doc/bindings.html)が動いている環境が必要です。

MeCabの辞書は、[IPAdic](http://mecab.googlecode.com/svn/trunk/mecab/doc/index.html)および、[UniDic](http://download.unidic.org/)のUTF-8版に対応しています。

参考： [Windowsにmecab-pythonを導入](http://w.livedoor.jp/spz/d/Windows%A4%CBmecab-python%A4%F2%C6%B3%C6%FE)

## インストール
``git clone https://github.com/tkyf/jpair.git``

## 実行例

main.pyに2つの文のファイルを指定して実行します。

    $ python main.py -i incorrection.txt -c correction.txt
    1       こにちわ        こんにちは 感動詞-一般
    1       わちし  わたし 代名詞
    1       でした  です 助動詞

出力は左から、

そのペアが出現した回数、-iで指定されたファイル内での表現、

-cで指定されたファイル内での表現、-cで指定されたファイル内での品詞です。

※ 出力の文字コードはUTF-8です。

## LICENSE

MIT

