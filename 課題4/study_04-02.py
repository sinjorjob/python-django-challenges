import re


### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_master=item_master   # item_masterにはItemクラスがリスト形式で格納される。
    
    def add_item_order(self,item_code):
        self.item_order_list.append(item_code)
        
    def view_item_list(self):
        #
        for order in self.item_order_list:   #オーダー情報（商品コード）を1つずつ取り出し
            for item in self.item_master:    #商品情報が格納されているitem_masterから1つずつ商品クラス情報を取り出し
                if order == item.item_code:    #オーダーされた商品コードと同じ商品コードのクラスかどうかをチェックし
                    print(f"商品コード{order}, 商品名：{item.item_name}, 価格：{item.price}") #一致していたらその商品の名前、価格を表示
                    break
                    
                    

#入力値が3桁数字かどうかを判定する関数
def is_only_num(input):
    regex = r'([0-9]{3})'
    return True if re.fullmatch(regex, input) else False
    

#商品マスターに存在する商品コードかどうかをチェックする関数
def is_valid(item_code, item_master):
    decision_flag  = False
    for item in item_master:  #商品マスターに入力した商品コードが存在するかチェック
        if item_code == item.item_code:
            decision_flag  = True
    return decision_flag
    
    
### メイン処理
def main():
    # マスタ登録
    item_master=[]
    item_master.append(Item("001","りんご",100))
    item_master.append(Item("002","なし",120))
    item_master.append(Item("003","みかん",150))
    
    # オーダー登録
    order_number =input("商品の注文番号を入力してください。 >>> ")
    #入力値のチェック3桁の数字
    if not is_only_num(order_number):
        print("3桁数字の商品コードを入力してください。")
        exit()
    #商品コードの存在チェック
    if not is_valid(order_number, item_master):
        print("商品コードが存在しません。\n存在する商品コードを入力してください。")
        exit()
    
    else:
        order=Order(item_master)
        order.add_item_order(order_number)
        order.view_item_list()

if __name__ == "__main__":
    main()
