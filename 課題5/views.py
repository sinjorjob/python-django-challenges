import eel
import desktop
from function import add_item_master
from function import Item, Order

app_name="html"
end_point="index.html"
size=(700,600)
CSV_PATH = "./csv/item_master.csv"

#EEL起動時に商品マスターとオーダインスタンスを1度だけ自動生成させる。
item_master = add_item_master(CSV_PATH) #csvから商品マスタを登録
order=Order(item_master) #商品マスタを元にオーダーインスタンスを生成


@eel.expose
def add_item(item_code, item_count):
    
    """
    inex.htmlの「オーダリストに追加する」ボタンを押すとCALLされる。
    input_orderメソッドで受けとった注文情報をorderインスタンスの下記変数へ格納する
    self.item_order_list:注文コード
    self.item_count_list:注文数

    第1引数：商品コード
    第2引数：商品の数量

    戻り値1: order_list:  注文リストに追加したオーダー情報
    戻り値2: total_amount:注文した商品の合計金額
    戻り値3: message: 処理タイプとメッセージ
    ※エラーが発生した場合は戻り値はmessageのみ。
    """

    message = order.input_order(item_code, item_count, order, item_master)  #注文の受付
    if message['type'] == 'error':
        print("errorメッセージを送信！")
        return message   #エラーtypeとメッセージ内容を返す
    else:
        #画面の「注文リスト」のTextareaにオーダーした情報を表示させるためのオーダ情報を取得
        order_list, total_amount = order.view_item_list() 
        return order_list, total_amount, message


@eel.expose
def get_item_info():
    """
    EEL画面の「商品追加はこちら」ボタンを押した際に発動する関数。
    入力フォームのTOPに購入可能な製品情報（商品コード、商品名、価格）を表示するために
    注文リストに格納されている製品情報を取得して画面に返す。

    引数：なし
    戻り値1: item_code： 製品マスターに登録されている商品コード
    戻り値2: item_name： 製品マスターに登録されている商品名
    戻り値3: item_price： 製品マスターに登録されている商品価格
    
    """

    item_name, item_code, item_price = order.get_item_info(item_master)
    return item_code, item_name, item_price


@eel.expose
def payment(payment):
    """
    お会計処理画面で「購入する」ボタンを押すと発動する関数。
    入力した支払金額と元におつりを計算する。

    引数：お会計処理画面で入力した支払金額
    戻り値: message: 処理タイプとメッセージ（エラー内容 or 支払金額とおつりの情報）
    
    """
    message = order.input_deposit_and_change_calc(payment)   #支払額を元におつりの金額を取得
    return message


@eel.expose
def chk_order_status():
    """
    「お会計はこちら」ボタンをクリックした際に、注文リストに1件も登録されていなかった場合に
    アラートを出すためにオーダー商品が存在しているかチェックする関数

    引数：なし
    戻り値: message: 処理タイプとメッセージ（エラー内容 or 支払金額とおつりの情報）
    
    """

    message = order.chk_order_status()   #製品がオーダーリストに存在するかチェック
    return message


@eel.expose
def init_order_list():
    """
    EEL画面の「注文をリセット」ボタンをクリックした際に、オーダー情報を初期化する。

    引数：なし
    戻り値: なし
    
    """
    #print("初期化前のitem_order_list=", order.item_order_list)
    #print("初期化前のitem_count_list=", order.item_count_list)
    order.item_order_list=[]   #注文コードをリセット
    order.item_count_list=[]   #注文数をリセット
    # total_all_items_amount変数を削除（合計金額をリセット）
    delattr(order,"total_all_items_amount")  
    #print("初期化後のitem_order_list=", order.item_order_list)
    #print("初期化後のitem_count_list=", order.item_count_list)
    return None


desktop.start(app_name,end_point,size)

