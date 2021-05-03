import pandas as pd
import sys
import os
import datetime


### 検索ツール
def search_word(word, file_path, save_dir):
    #処理結果の格納先辞書を定義
    message = {"type":"", "message":""}

    #指定した保存先ディレクトリのチェック
    if not os.path.exists(save_dir):    
        message["type"] = "error"
        message["message"] = "保存先ディレクトリが指定されていないか、指定したディレクトリが存在しません。\n存在するディレクトリを指定してください。"
        return message

    #カレントパスの取得
    current_dir = os.getcwd()
    #ファイル名を取得(C:\fakepath\filename.csv -> filename.csvのみ抽出)
    file_name = file_path.split("\\")[-1]
    #検索対象のcsvファイルの絶対パスを生成
    csv_file = os.path.join(current_dir, file_name)
    # csvの読み込み
    if not os.path.exists(csv_file):    
        message["type"] = "error"
        message["message"] = "ファイルが存在しませんでした。\ncsvが正しいパスにあることを確認してください。"
        return message
    try:
        #検索対象のcsvを読み込む
        df = pd.read_csv(csv_file, encoding='utf-8_sig')
    except:
        message["type"] = "error"
        message["message"] = "CSVファイルの読み込みが失敗しました。"
        return message

    # DataFrame -> リストデータに変換
    source = [row['キャラクタ名'] for index, row in df.iterrows()]
    
    if word in source:
        message["type"] = "success"
        message["message"] = "検索ワード【" + word + "】が見つかりました\n"
        return message
    else:
        message["message"] = "検索ワード【" + word + "】が見つかりませんでした。\n新規にワードを追加します。\n"
  
        # 検索ワードをSeries形式に変換
        add_word = pd.Series( [word], index=df.columns)
        # df(DataFrame )に検索ワードを追加
        df = df.append( add_word, ignore_index=True) 
        # 指定のパスへcsv書き込み
        try:
            now = datetime.datetime.now()
            #保存するファイル名を生成（yyyymmdd-hhmmss_ファイル名.csv）
            file_name_date = now.strftime('%Y%m%d_%H%M%S') + '_' + file_name
            #保存するcsvファイルの絶対パスを生成
            save_file = os.path.join(save_dir, file_name_date)
            df.to_csv(save_file,index=False,encoding='utf-8_sig')
            #マスターのCSVファイルも更新
            df.to_csv(file_name,index=False,encoding='utf-8_sig')
        except:
            message["type"] = "error"
            message["message"] = "CSVファイルの書き込みが失敗しました。\n"
            return message        

        message["message"] = message["message"] + "検索ワードの追加が完了しました。\n"
        message["type"] = "success"
        return message


if __name__ == "__main__":
    
    search_word()