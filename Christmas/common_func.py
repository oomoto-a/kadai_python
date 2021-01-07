# -*- coding: utf-8 -*-
import sys 
import os 
import sqlite3 

def resource_path(relative_path):
    """"
    パス検索
    """
    try:
        base_path = sys._MEIPASS
        print(base_path)
    except Exception:
        base_path = os.path.dirname(__file__)
        print(base_path)
    return os.path.join(base_path, relative_path)

def get_dbname():
    dbname = "INFO.db"
    
    return dbname


def exists_db():
    """
    dbファイルがあるかどうかチェックする

    Returns true：dbファイルがある
    -------
    None.

    """
    
    dbname = get_dbname()
    return os.path.exists(dbname)
    
def init_db():
    """
    DBの初期化を行う
    lancers_search_conditionの

    Returns  None.

    """
    dbname = get_dbname()
    print(dbname)
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS lancers_search_condition")
    # lancers_search_conditionというtableを作成してみる
    # 大文字部はSQL文。小文字でも問題ない。
    cur.execute(
        'CREATE TABLE lancers_search_condition(id INTEGER PRIMARY KEY, '
        + 'email STRING, password STRING,'
        + 'search_name STRING, search_url STRING, sort STRING)')
    
    conn.commit()
    
    cur.close()
    conn.close()