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

def output_receipt(order_item, deposit, change):
    """
     レシートを出力
    """
    # ■7.日付時刻をファイル名としたレシートファイル（テキスト）に出力できるようにしてください
    dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "receipt{}.txt".format(dt_now)
    with open(file_name, "w", newline = "", encoding='utf-8') as f:
        for item in order_item.get_item_order_list():
            f.write(item.get_write_info())
            f.write("\n")
                
        f.write("お預かり金額:{}".format(deposit))
        f.write("\n")
        f.write("お返し:{}".format(change))
        f.write("\n")
        f.write("ありがとうございました")

        
def input_code_amount(code, amount, item_master, order):
    """
     商品コードと個数を入力
     return : response, item
    """
    response = {}
    search_result = get_item_by_code(item_master, code)
    if not amount.isdecimal():
        response = {"result":"ng", 
                    "result_text":"個数に数値を入力してください"}
        return response, None
    
    if search_result is None:
        response = {"result":"ng", 
                    "result_text":"コードが間違っています"}
        return response, None
    
    search_result.set_amount(amount)
    order.add_item_order(search_result)
    response = {"result":"ok", 
                "product_info": search_result.get_subtotal(),
                "sum": order.sum_item_list()}
    
    return response, search_result

def input_deposit(order, deposit, item_master):
    """
     お預かり金額まで入力
    """
    response = {}
    
    if not deposit.isdecimal():
        response = {"result":"ng", 
                    "result_text":"お預かり金額に数値を入力してください"}
        return response
    
    sum_money = order.sum_item_list()
    
    change = int(deposit) - sum_money
    if change < 0:
        response = {"result":"ng", 
                    "result_text":"料金が足りません"}
        return response

    response = {"result":"ok", 
                "change": change}
    
    output_receipt(order, deposit, change)

    return response
    
def get_master_info_json():
    """
    item_master.csvからデータを取得して
    JSON形式で出力
    初期表示に使用
    """
    # マスタ
    item_master_json_list=[]
    
    item_master_csv = pd.read_csv("./item_master.csv", 
                                  dtype=str)
    # JSONに変換
    for i in range(len(item_master_csv)):
        item_master_df = item_master_csv.loc[i]
        item_master_json_list.append(item_master_df.to_json())
        
    return item_master_json_list
        
def get_master_info_list():
    """
    item_master.csvからデータを取得して
    List形式で出力
    初期表示に使用
    """
    # マスタ
    item_master_list=[]
    
    item_master_csv = pd.read_csv("./item_master.csv", 
                                  dtype=str)
    # JSONに変換
    for i in range(len(item_master_csv)):
        item_master_df = item_master_csv.loc[i]
        ## クラス変数のマスタに追加
        item_master_list.append(objc.Item(item_master_df["code"],
                             item_master_df["name"],
                             item_master_df["price"]))
        
    return item_master_list

if __name__ == "__main__":
    print("test")
   