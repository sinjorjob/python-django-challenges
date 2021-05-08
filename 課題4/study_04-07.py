import re
import pandas as pd
import datetime
import os


CSV_PATH = "./item_master.csv"
RECEIPT_FOLDER = "./receipt"


### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code   #商品コード
        self.item_name=item_name   #商品名
        self.price=price           #商品の値段
    
    def get_price(self):
        return self.price

    
### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]   #注文コード
        self.item_count_list=[]   #オーダー数を追加
        self.item_master=item_master   # item_masterにはItemクラスがリスト形式で格納される。
    
    def add_item_order(self,item_code, order_count):
        #注文数分オーダーを追加
        self.item_order_list.append(item_code)
        self.item_count_list.append(order_count)
        
    def view_item_list(self):
        self.total_all_items_amount=0   #全商品の合計金額
        self.total_item_amount = 0  #商品毎の合計金額

        for order, count in zip(self.item_order_list, self.item_count_list):   #注文コードと注文数を1レコードずつ取り出す
            for item in self.item_master:    #商品情報が格納されているitem_masterから1つずつ商品クラス情報を取り出し
                if order == item.item_code:    #オーダーされた商品コードと同じ商品コードのクラスかどうかをチェックし
                    #オーダーの合計金額を計算
                    self.total_item_amount = int(item.price) * int(count)   #商品全体の合計金額
                    self.total_all_items_amount += int(item.price) * int(count)   #商品毎の合計金額
                    print(f"商品名：{item.item_name}, 価格：{item.price}, 注文数：{count},合計金額：{self.total_item_amount}円") #一致していたらその商品の名前、価格を表示
                    self.write_receipt(f"商品名：{item.item_name}, 価格：{item.price}, 注文数：{count},合計金額：{self.total_item_amount}円")
                    break

    def input_order(self,order,item_master):
        """注文を受け付ける
        """
        print("ご注文を受け賜ります。")
        while True:
            
            # オーダー登録
            order_number =input("商品の注文番号を入力してください。 >>> ")
            #商品コードの入力値チェック（数字3桁）
            if not is_only_num(order_number, r'([0-9]{3})'):
                print("3桁数字の商品コードを入力してください。")
                continue
            #商品コードの存在チェック
            if not is_item_code_valid(order_number, item_master):
                print("商品コードが存在しません。\n存在する商品コードを入力してください。")
                continue
                
            order_count = input("商品の注文数を入力してください。>>>")
            
            #注文数のチェック(1以上の整数かどうか判定)
            if not is_only_num(order_count, r'([0-9]+)'):
                print("注文数は整数値を入力してください。")
                continue
            
            order.add_item_order(order_number, order_count)    #注文情報をオーダーに追加
            continue_input = input("引き続き注文する場合は「1」を、注文を終了する場合は「2」を入力してください。 ")
            if continue_input == "1":
                continue
            
            else:
                print("注文受付を終了します。")
                break
        

    def input_deposit_and_change_calc(self):
        """お客様からのお預かり金額を入力しお釣りを計算"""
        while True:
            self.deposit=input("お預かり金を入力してください >>> ")
            self.change_money=int(self.deposit) - self.total_all_items_amount #おつりの計算
            if self.change_money >= 0:
                print(f"お預り金は{self.deposit}円です。")
                print(f"おつりは{self.change_money}円です。")
                self.write_receipt(f"お預り金は{self.deposit}円です。")
                self.write_receipt(f"おつりは{self.change_money}円です。")
                break
            else:
                print("お金が不足しています。\n再度金額を入力してください。")
    
    def write_receipt(self,text):
        """
        注文結果をログに出力
        ファイル名:receipt_yyyymmdd.log
        """
        now = datetime.datetime.now()
        receipt_file = os.path.join(RECEIPT_FOLDER, 'receipt_' + now.strftime('%Y%m%d') + '.log')        
        with open(receipt_file, mode="a",encoding="utf-8_sig") as f:  #末尾に追記
            f.write(text+"\n")
            
            
            
        
#入力値の数値判定関数
def is_only_num(input, regex):
    return True if re.fullmatch(regex, input) else False


#商品マスターに存在する商品コードかどうかをチェックする関数
def is_item_code_valid(item_code, item_master):
    decision_flag  = False
    for item in item_master:  #商品マスターに入力した商品コードが存在するかチェック
        if item_code == item.item_code:
            decision_flag  = True
    return decision_flag
    
    
def add_item_master(csv_path):
    print("------- マスタ登録を開始します。 ---------")
    item_master=[]   #商品マスタの格納先リスト
    
    try:
        # pandasは文字列を格納するのに、objectというdtypeを用いる
        # item_codeが001->1のようになってしまうのでこれを回避
        item_master_df=pd.read_csv(csv_path,dtype={"item_code":object})
        #DataFrameを1行ずつ抽出しItemクラスを使って商品マスタのインスタンスを生成
        for index, row in item_master_df.iterrows():
            item_master.append(Item(row["item_code"], row["item_name"], row["price"]))
        print("{}件の商品データを登録しました。".format(index+1))
        print("------- マスタ登録が完了しました。 ---------")
        return item_master                    
    except Exception as e:
        print("マスタ登録処理が異常終了しました。")
        print(f"エラー内容:{e}")
        exit()
   
    
    

### メイン処理
def main():
    
    item_master = add_item_master(CSV_PATH) #csvから商品マスタを登録
    order=Order(item_master) #商品マスタを元にオーダーインスタンスを生成
    order.input_order(order, item_master)  #注文の受付
    order.view_item_list()   #注文の合計金額計算
    order.input_deposit_and_change_calc()  #預り金とおつりを計算


if __name__ == "__main__":
    main()


