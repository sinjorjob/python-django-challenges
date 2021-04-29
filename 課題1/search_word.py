"""
簡単な検索ツールの作成
１．入力したキーワードで、キャラクターリスト(source)を検索して、存在すれば存在する旨を、存在しなければ存在しない旨をPrint文で表示してみましょう
２．１に追加して結果が存在しなかった場合に、キャラクターリスト(source)に追加できるようにしてみましょう
３．２に追加してキャラクターリスト(source)をCSVから読み込んで登録できるようにしてみましょう
４．３に追加してキャラクターリスト(source)をCSVに書き込めるようにしてみましょう
"""


# 検索ソース
import pandas as pd
import sys

source_file = "<ファイルパスを指定>\source.csv"

### 検索ツール
def search(file):
    word =input("鬼滅の登場人物の名前を入力してください >>> ")
    # csvの読み込み
    df = pd.read_csv(file, encoding='utf-8_sig')
    # DataFrame -> リストデータに変換
    source = [row['キャラクタ名'] for index, row in df.iterrows()]
    
    if word in source:
        print(f"{word}が見つかりした")
    else:
        print(f"検索ワード{word}が見つかりませんでした")
        print(f"検索ワード{word}を追加します。")
        # 検索ワードをSeries形式に変換
        add_word = pd.Series( [word], index=df.columns)
        # df(DataFrame )に検索ワードを追加
        df = df.append( add_word, ignore_index=True)
 
        print(f"検索ワード{word}を追加しました")
        # csv書き込み
        df.to_csv(source_file,index=False,encoding='utf-8_sig')


if __name__ == "__main__":
    
    search(source_file)