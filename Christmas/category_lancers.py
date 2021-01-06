from selenium.webdriver import Chrome, ChromeOptions
import time
import os
import sys
import sqlite3
from urllib.parse import urlparse

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
        print(base_path)
    except Exception:
        base_path = os.path.dirname(__file__)
        print(base_path)
    return os.path.join(base_path, relative_path)

# Chromeを起動する関数
def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    
    return Chrome(executable_path=resource_path("./" + driver_path), options=options)


# driverを起動
if os.name == 'nt': #Windows
    driver = set_driver("chromedriver.exe", False)
elif os.name == 'posix': #Mac
    driver = set_driver("chromedriver", False)

# Webサイトを開く
BASE_URL = "https://www.lancers.jp"
driver.get("https://www.lancers.jp/work/search?ref=search_topic&show_description=1&sort=client&work_rank%5B%5D=0&work_rank%5B%5D=2&work_rank%5B%5D=3")
time.sleep(5)
# ポップアップを閉じる
popup_count = len(driver.find_elements_by_class_name("karte-close"))
if popup_count > 0:
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(5)
    
    
#***********************  カテゴリ取得部分  ********************************

# カテゴリから探す
search_categoly = driver.find_element_by_css_selector("nav.p-search-categories")
categolies = search_categoly.find_elements_by_css_selector("dl")
count = 1
lancers_array = []
child_array = []
for categoly in categolies:
    # 親項目　例:システム開発・運用
    parent_text = categoly.find_element_by_css_selector("dt").get_attribute("textContent").strip()
    parent_url = categoly.find_element_by_css_selector("a").get_attribute("href")
    parent_id = count * 100 * 100
    parent = (parent_id, 0, parent_text, parent_url)
    lancers_array.append(parent)

    count = count + 1
    count_child = 1
    # 子項目　例:Web・システム開発
    child_webdrivers = categoly.find_elements_by_css_selector("dd")
    for child_webdriver in child_webdrivers:
        # 子項目のテキスト
        child_text = child_webdriver.find_element_by_css_selector("a").get_attribute("textContent").strip()
        # 子項目のURL
        child_url = child_webdriver.find_element_by_css_selector("a").get_attribute("href")
        # 子項目のID
        child_id = parent_id + count_child * 100
        child = (child_id, parent_id, child_text, child_url)
        lancers_array.append(child)
        child_array.append(child)
        count_child = count_child + 1
        

# 孫項目　例:Webシステム開発・プログラミング
for child in child_array:
    # URLへ移動
    driver.get(child[3])
    time.sleep(3)
    # 選択したカテゴリ
    #driver.find_elements_by_class_name(".p-search-sidenav__list-item--active")
    # 孫カテゴリ
    grandchild_webdrivers = driver.find_elements_by_css_selector("dd.p-search-sidenav__list-item--child")

    count_grand_child = 1
    for grandchild_webdriver in grandchild_webdrivers:
        # 孫項目のテキスト
        grand_child_text = grandchild_webdriver.find_element_by_css_selector("a").get_attribute("textContent").strip()
        # 孫項目のURL リクエストパラメータを削除する
        grand_child_url = grandchild_webdriver.find_element_by_css_selector("a").get_attribute("href")
        o = urlparse(grand_child_url)
        grand_child_url = BASE_URL + o.path
        # 孫項目のID
        grand_child_id = child[0] + count_grand_child
        grand_child = (grand_child_id, child[0], grand_child_text, grand_child_url)
        lancers_array.append(grand_child)
        count_grand_child = count_grand_child + 1
    
#***********************  DB部分  ********************************
dbname = resource_path("./db/INFO.db")
conn = sqlite3.connect(dbname)
# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()


cur.execute("DROP TABLE IF EXISTS lancers")
# lancersというtableを作成してみる
# 大文字部はSQL文。小文字でも問題ない。
cur.execute(
    'CREATE TABLE lancers(id INTEGER PRIMARY KEY, parent INTEGER, name STRING, url STRING)')

# データベースへコミット。これで変更が反映される。
conn.commit()

cur.executemany("insert into lancers values (?,?,?,?)", lancers_array)
conn.commit()

for row in cur.execute('select * from lancers'):
    print(row)

cur.close()
conn.close()