# -*- coding: utf-8 -*-
import rakuten_api
import pandas as pd
import datetime
import sys
import time

ICHIBA_ITEM_FILE_NAME = "./ichiba/ichiba_item{}_{}.csv"
PRODUCT_FILE_NAME = "./product/product{}_{}.csv"
RANK_FILE_NAME = "./rank/rank{}_{}.csv"
MAX_PAGE = 100
LIMIT_NUM = MAX_PAGE*30
#リクエスト過多 (各ユーザ制限値超過)対策の待機時間（秒）
WAIT_TIME = 1

def write_csv(df, file_name, header):
    """"
    ファイル出力
    """
    df.to_csv(file_name, index=False, encoding="utf-8_sig", mode="a", header=header)
    
def write_ichiba_item(result_json, file_name, header):
    """"
    楽天商品検索API 
    商品名と価格の一覧
    """
    items = []
    for item_info in result_json.get("Items"):
        item = item_info.get("Item")
        items.append({"商品名" : item.get("itemName"), "価格" : item.get("itemPrice")})
        print({"商品名" : item.get("itemName"), "価格" : item.get("itemPrice")})

        
    df = pd.json_normalize(items)
    df = df[["商品名","価格"]]
    write_csv(df, file_name, header)

def get_ichiba_item(keyword):
    print("call:{}".format(sys._getframe().f_code.co_name))

    result_json = rakuten_api.get_ichiba_item_json_first(keyword)
    result_disp = ""
    result_detail = ""
    # 件数チェック
    if result_json.get("count") > 0:
        dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = ICHIBA_ITEM_FILE_NAME.format(keyword, dt_now)

        header = True
        # ヒットした場合
        write_ichiba_item(result_json, file_name, header)
        result_disp = "{}件取得しました".format(result_json.get("count"))
        ## ページ処理がある場合
        if result_json.get("pageCount")>1:
            header = False
            for i in range(2, result_json.get("pageCount")+1):
                if MAX_PAGE+1 == i:
                    break
                
                # リクエスト過多 (各ユーザ制限値超過)対策のため、待機
                time.sleep(WAIT_TIME)
                result_json = rakuten_api.get_ichiba_item_json(keyword, i)
                write_ichiba_item(result_json, file_name, header)

        if result_json.get("count") > LIMIT_NUM:
            result_detail =  "最大取得件数{}件を超えたの分は出力されません".format(LIMIT_NUM)
    else:
        # ヒットしなかった場合
        result_disp = "対象商品はありません"
        
    return {"result":"ok", "message":result_disp, "detail":result_detail}


def write_product(result_json, file_name, header):
    """"
    楽天商品検索API 
    商品名と価格の一覧
    """
    items = []
    for item_info in result_json.get("Products"):
        item = item_info.get("Product")
        items.append({"商品名" : item.get("productName"), "最安値" : item.get("minPrice"), "最高値" : item.get("maxPrice")})
        print({"商品名" : item.get("productName"), "最安値" : item.get("minPrice"), "最高値" : item.get("maxPrice")})

        
    df = pd.json_normalize(items)
    df = df[["商品名","最安値", "最高値"]]
    write_csv(df, file_name, header)


def get_product(keyword):
    """"
    商品価格ナビ製品検索API
    最安値と最高値
    """
    print("call:{}".format(sys._getframe().f_code.co_name))
    
    result_json = rakuten_api.get_product_json_first(keyword)
    result_disp = ""
    result_detail = ""
    # 件数チェック
    if result_json.get("count") > 0:
        dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = PRODUCT_FILE_NAME.format(keyword, dt_now)

        header = True
        # ヒットした場合
        write_product(result_json, file_name, header)
        result_disp = "{}件取得しました".format(result_json.get("count"))
        ## ページ処理がある場合
        if result_json.get("pageCount")>1:
            header = False
            for i in range(2, result_json.get("pageCount")+1):
                if MAX_PAGE+1 == i:
                    break
                
                # リクエスト過多 (各ユーザ制限値超過)対策のため、待機
                time.sleep(WAIT_TIME)
                result_json = rakuten_api.get_product_json(keyword, i)
                write_product(result_json, file_name, header)

        if result_json.get("count") > LIMIT_NUM:
            result_detail =  "最大取得件数{}件を超えたの分は出力されません".format(LIMIT_NUM)
    else:
        # ヒットしなかった場合
        result_disp = "対象商品はありません"
        
    return {"result":"ok", "message":result_disp, "detail":result_detail}

def get_genre(keyword):
    """"
    ジャンル検索API
    """
    print("call:{}".format(sys._getframe().f_code.co_name))
    genres = []
    result_json = rakuten_api.get_genre_json(keyword)
    # ジャンルがない場合はあり得ないのでチェックしない
    children = result_json.get("children")
    for child_dict in children:
        child = child_dict.get("child")
        genres.append({"genreName": child.get("genreName"),
                       "genreId": child.get("genreId"),
                       "genreLevel": child.get("genreLevel")})
    
    return genres
    
def write_rank(result_json, file_name, header):
    """"
    ランキングAPI 
    商品名とランクの一覧
    """
    items = []
    for item_info in result_json.get("Items"):
        item = item_info.get("Item")
        items.append({"順位" : item.get("rank"), 
                      "商品名" : item.get("itemName"), 
                      "商品価格" : item.get("itemPrice")})

        
    df = pd.json_normalize(items)
    df = df[["順位","商品名", "商品価格"]]
    write_csv(df, file_name, header)

def get_rank(keyword):
    """"
    ランキング検索API
    """
    print("call:{}".format(sys._getframe().f_code.co_name))
    print(keyword)
    result_json = rakuten_api.get_rank_json(keyword[0])
    # ランキングがない場合はあり得ないのでチェックしない
    dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = RANK_FILE_NAME.format(keyword[1], dt_now)
    write_rank(result_json, file_name, True)
    result_disp = "{}ランキングを取得しました".format(keyword[1])
    
            
    return {"result":"ok", "message":result_disp, "detail":""}