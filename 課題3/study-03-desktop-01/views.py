import eel
import desktop
import search

app_name="html"
end_point="index.html"
size=(700,600)

#ワード検索用関数
@eel.expose
def serach_word(word, filepath, save_dir):
    """
    第1引数：検索ワード
    第2引数：検索対象のCSV情報
    第3引数：新規ワードを追加した県債対象データの保存先ディレクトリ
    戻り値：処理結果（エラー種別、メッセージ）
    """
    result = search.search_word(word, filepath, save_dir)
    return result


desktop.start(app_name,end_point,size)

