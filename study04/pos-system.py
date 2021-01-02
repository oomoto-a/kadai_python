import object_class as objc
import pandas as pd
import datetime

def get_item_by_code(item_list, code):
    """
     item_listからcodeをキーに検索
     無い場合はNoneを返す
    """
    for item in item_list:
        if code == item.get_code():
            return item
        else:
            continue

    return None

def output_receipt(order_item):
    """
     レシートを出力
    """
    # ■7.日付時刻をファイル名としたレシートファイル（テキスト）に出力できるようにしてください
    dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "receipt{}.txt".format(dt_now)
    with open(file_name, "w", newline = "", encoding='utf-8') as f:
        f.write(order_item.get_display_info())
        f.write("\n")
        f.write(order_item.get_display_sum())
        f.write("\n")
        f.write("お預かり金額:{}".format(order_item.get_deposit()))
        f.write("\n")
        f.write("お返し:{}".format(order_item.get_change()))
        f.write("\n")
        f.write("ありがとうございました")


### メイン処理
def main():
    # マスタ登録
    item_master=[]
    item_master_csv = pd.read_csv("item_master.csv", 
                                  dtype=str)
        
    # オーダー登録
    for i in range(len(item_master_csv)):
        item_master_df = item_master_csv.loc[i]
        item_master.append(objc.Item(item_master_df["code"],
                                     item_master_df["name"],
                                     item_master_df["price"]))
    
    # マスタ一覧表示
    infos = []
    for info in item_master:
        infos.append(info.get_display_info())
    print("\n".join(infos))
    
    # ■2.オーダーをコンソール（ターミナル）から登録できるようにしてください 登録時は商品コードをキーとする
    print("オーダーを入力してください")
    code =input(" コード入力 >>> ")
    
    order_item = get_item_by_code(item_master, code)
    
    if order_item is None:
        print("コードが間違っています")
        return 

    # ■1.オーダー登録した商品の一覧（商品名、価格）を表示できるようにしてください
    print(order_item.get_display_info())

    print("個数を入力してください")
    amount =input(" 個数入力 >>> ")
    
    if not amount.isdecimal():
        print("数値を入力してください")
        return 
        
    order_item.set_amount(amount)

    # ■5.オーダー登録した商品の一覧（商品名、価格）を表示し、かつ合計金額、個数を表示できるようにしてください
    print(order_item.get_display_info())
    print(order_item.get_display_sum())
    
    # ■6.お客様からのお預かり金額を入力しお釣りを計算できるようにしてください
    print("お預かり金額を入力してください")
    deposit =input(" お預かり金額 >>> ")
    
    if not deposit.isdecimal():
        print("数値を入力してください")
        return 
    
    order_item.set_deposit(deposit)
    if order_item.get_change() < 0:
        print("料金が足りません")
        return

    print(order_item.get_display_change())
    
    # レシート出力
    output_receipt(order_item)
    
if __name__ == "__main__":
    main()