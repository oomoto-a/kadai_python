# -*- coding: utf-8 -*-
import common_func
import sqlite3


dbname = common_func.resource_path("./db/INFO.db")
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