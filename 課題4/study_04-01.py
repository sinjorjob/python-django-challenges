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
                    print(f"商品コード{order}, 商品名：{item.item_name}, 価格：{item.price}")   #一致していたらその商品の名前、価格を表示
                    break
    
   
    
### メイン処理
def main():
    # マスタ登録
    item_master=[]
    item_master.append(Item("001","りんご",100))
    item_master.append(Item("002","なし",120))
    item_master.append(Item("003","みかん",150))
    
    # オーダー登録
    order=Order(item_master)
    order.add_item_order("001")
    order.add_item_order("002")
    order.add_item_order("003")
    
    # オーダー表示
    order.view_item_list()


if __name__ == "__main__":
    main()
