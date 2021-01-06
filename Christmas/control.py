# -*- coding: utf-8 -*-
import pandas as pd
import datetime
import sys
import os
import selenium_logic
import common_func
import sqlite3

LANCERS_FILE_NAME = "./data/lancers_{}_{}.csv"
CROWDWORKS_FILE_NAME = "./data/crowdworks_{}_{}.csv"

def write_csv(df, file_name, header):
    """"
    ファイル出力
    """
    df.to_csv(file_name, index=False, encoding="utf-8_sig", mode="a", header=header)
    
def write_info(info_array, file_name, header):
    """"
    情報出力
    """
    new_dir_path_recursive = './data'
    # dataフォルダがなかったら作成
    if not os.path.exists(new_dir_path_recursive):
        os.makedirs(new_dir_path_recursive)

    keys = []    
    for key in info_array[0].keys():
        keys.append(key)
    df = pd.json_normalize(info_array)
    df = df[keys]
    write_csv(df, file_name, header)

def save_search_info(url, param):
    #***********************  DB部分  ********************************
    dbname = common_func.resource_path("./db/INFO.db")
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()
    cur.execute("delete from lancers_search_condition")
    insert_info = []
    # id
    insert_info.append(0)
    # email
    insert_info.append(param["email"])
    # password
    insert_info.append(param["password"])
    # search_name
    insert_info.append(param["name"])
    # search_url
    insert_info.append(url)
    # sort
    insert_info.append(param["sort"])
    
    cur.execute("insert into lancers_search_condition values (?,?,?,?,?,?)", insert_info)
    conn.commit()
    
    cur.close()
    conn.close()

def select_search_info():
    result = {"email": "", "password": "", "name": "", "url": "", "sort":""}
    #***********************  DB部分  ********************************
    dbname = common_func.resource_path("./db/INFO.db")
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()
    
    cur.execute("select * from lancers_search_condition")
    selecct = cur.fetchone()
    
    if selecct is not None:
        result = {"email": selecct[1], "password": selecct[2], "name": selecct[3], "url": selecct[4], "sort": selecct[5]}

    cur.close()
    conn.close()

    return result

def search_lancers(url, param):
    """"
    ランサーズの案件検索
    """
    print("call:{}".format(sys._getframe().f_code.co_name))
    
    save_search_info(url, param)
    detail = ""
    lancers_info = selenium_logic.get_lancers(url, param)
    lancers_array = lancers_info[0]
    if lancers_info[1]:
        detail = "ログインに失敗しました。ログインしていない状態で検索しています。"
    dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = LANCERS_FILE_NAME.format(param["name"], dt_now)
    header = True
    if len(lancers_array) == 0:
        return {"result":"ok", "message":"0件でした", "detail":""}
    write_info(lancers_array, file_name, header)
    
    count = len(lancers_array)
    
    return {"result": "ok", "message": "{}件取得しました".format(count), "detail": detail}

def search_crowdworks(url, param):
    """"
    クラウドワークスの案件検索
    """
    print("call:{}".format(sys._getframe().f_code.co_name))

    info_array = selenium_logic.get_crowdworks(url)
    dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = CROWDWORKS_FILE_NAME.format(param["name"], dt_now)
    header = True
    
    if len(info_array) == 0:
        return {"result":"ok", "message":"0件でした", "detail":""}
    write_info(info_array, file_name, header)
    
    count = len(info_array)
    return {"result":"ok", "message":"{}件取得しました".format(count), "detail":""}


