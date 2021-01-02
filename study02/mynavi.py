import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
import datetime

#エラー情報リスト
error_info_list=[]
# エラーメッセージ
ERROR_MESSAGE = "[{}]ERROR:{}{}"

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
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)


# |を含む会社情報から、会社名を取得する
def get_name(info):
    delimiter = "|"
    if delimiter in info:
        return info.split(delimiter)[0].strip()

    # |がない場合はそのまま返す
    return info

# 会社の情報を辞書型で取得
# webdriver：1社の情報  
def get_info_dict(webdriver, company_name, update_date):
    company_dist = {}
    # テーブルを指定
    table = webdriver.find_elements_by_class_name("tableCondition")[0]
    # 行単位のリスト
    tr_list = table.find_elements_by_tag_name("tr")
    for tr in tr_list:
        head = tr.find_element_by_class_name("tableCondition__head").text
        body = tr.find_element_by_class_name("tableCondition__body").text
        company_dist[head] = body

    company_dist["会社名"] = company_name
    company_dist["情報更新日"] = update_date

    return company_dist

# エラー情報を追加する (会社情報を表示してスキップする)
def add_error_info_skip(e, company_name):
    dt_now = datetime.datetime.now()
    company_name_info = "会社名：{} ".format(company_name) 
    str = ERROR_MESSAGE.format(dt_now, company_name_info, e)
    error_info_list.append(str.replace("\n", " "))
    
# エラー情報を追加する 
def add_error_info(e):
    dt_now = datetime.datetime.now()
    str = ERROR_MESSAGE.format(dt_now, "", e)
    error_info_list.append(str)

# エラーログ出力
def write_error_log():
    with open("error_log.log", "a", newline = "", encoding='utf-8') as f:
        for error in error_info_list:
            f.write(error)
            f.write("\n")

# ノーマルログ出力
def write_normal_log(str):
    dt_now = datetime.datetime.now()
    with open("normal.log", "a", newline = "", encoding='utf-8') as f:
        f.write("[{}] {}".format(dt_now, str))
        f.write("\n")

# 会社情報のリストを取得する
def get_company_info_list(driver):
    # ■課題２ for文を使って、１ページ内の３つ程度の項目（会社名、年収など）を取得できるように改造してみましょう
    page = driver.find_element_by_xpath("//li[@class='pager__item--active']/a").text
    # ■課題７　処理の経過が分かりやすいようにログファイルを出力してみましょう
    #  処理の開始と終了と検索結果の件数を表示するように対応しています
    write_normal_log("{}ページ目処理開始".format(page))

    company_info_list = []
    # 検索結果の会社情報を取得
    info_list = driver.find_elements_by_class_name("cassetteRecruit")
    for info in info_list :
        # 会社名
        company_name = get_name(info.find_element_by_class_name("cassetteRecruit__name").text)       
        # 更新日
        update_date = info.find_element_by_class_name("cassetteRecruit__updateDate").find_element_by_tag_name("span").text

        # ■課題６ エラーが発生した場合に、処理を停止させるのではなく、スキップして処理を継続できるようにしてみましょう
        try:
            # 各情報を辞書型で取得
            company_dist = get_info_dict(info, company_name, update_date)
        except Exception as e:
            # 例外発生時はエラーメッセージ追加して次の処理を行う
            add_error_info_skip(e, company_name)
            continue
        
        company_info_list.append(company_dist)


    # 検索結果の注目会社情報を取得
    recommend_info_list = driver.find_elements_by_class_name("cassetteRecruitRecommend")
    for info in recommend_info_list :
        # 会社名
        company_name = info.find_element_by_class_name("cassetteRecruitRecommend__name").text
        # 更新日
        update_date = info.find_element_by_class_name("cassetteRecruitRecommend__updateDate").find_element_by_tag_name("span").text
        try:
            # 各情報を辞書型で取得
            company_dist = get_info_dict(info, company_name, update_date)
        except Exception as e:
            # 例外発生時はエラーメッセージ追加して次の処理を行う
            add_error_info_skip(e, company_name)
            continue
            
        company_info_list.append(company_dist)
    
    write_normal_log("{}ページ目処理終了".format(page))

    return company_info_list
#

# main処理
def main():
    # ■課題４　任意のキーワードをコンソール（黒い画面）から指定して検索できるようにしてみましょう
    search_keyword =input("検索ワードを入力してください >>> ")
    EXPORT_FILE = "company_info.csv"
    LIMIT = 200
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", True)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)

    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    # ポップアップを閉じる
    popup_count = len(driver.find_elements_by_class_name("karte-close"))
    if popup_count > 0:
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        
    # ポップアップを閉じる
    popup_count = len(driver.find_elements_by_class_name("karte-close"))
    if popup_count > 0:
        driver.execute_script('document.querySelector(".karte-close").click()')

    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    write_normal_log("★★処理開始★★")

    search_count = driver.find_element_by_css_selector(".result__num .js__searchRecruit--count").text
    write_normal_log("{}件取得".format(search_count))

    # 会社情報のリスト
    company_info_list = []
    
    # ページ単位の会社情報のリスト
    page_company_info_list = get_company_info_list(driver)
    company_info_list.extend(page_company_info_list)

    # ■課題３ ２ページ目以降の情報も含めて取得できるようにしてみましょう
    next_count = len(driver.find_elements_by_class_name("iconFont--arrowLeft"))
    count = 0
    # 次へアイコンが表示されていたらtrue(200ページ、1万件超えるような場合は何らかのエラーの可能性があるため処理を抜ける)
    while next_count > 0 and count < LIMIT:
        # 次へボタン押下
        next_button = driver.find_element_by_class_name("iconFont--arrowLeft")
        next_button.location_once_scrolled_into_view
        next_button.click()
        # 次へボタンが表示されていたら１
        next_count = len(driver.find_elements_by_class_name("iconFont--arrowLeft"))
        # ページ内の情報を取得
        page_company_info_list = get_company_info_list(driver)
        # ページ内情報を会社情報に追加
        company_info_list.extend(page_company_info_list)
        count =+ 1

    print("数：{}".format(len(company_info_list)))
    
    if len(error_info_list) == 0:
        #エラーがなかった場合
        add_error_info("エラーはありませんでした")
        
    # エラーログ出力
    write_error_log()

    # ■課題５　取得した結果をpandasモジュールを使ってCSVファイルに出力してみましょう
    if len(company_info_list) > 0:
        # 検索結果1件以上
        if count == LIMIT:
            limit_message = {"会社名": "{}ページを超えるため、省略された会社情報があります".format(LIMIT + 1)}
            company_info_list.append(limit_message)

        df = pd.io.json.json_normalize(company_info_list)
        df = df[["会社名","仕事内容","勤務地","初年度年収","対象となる方","給与","情報更新日"]]
        df.to_csv(EXPORT_FILE, index=False)

    else:
        # 検索結果0件
        df = pd.DataFrame(["検索結果は0件でした"])
        df.to_csv(EXPORT_FILE, header=None, index=False)

    
    # ■課題１　会社名以外の項目を取得して画面にprint文で表示してみましょう。
    # 更新日が新しい順で会社名・情報更新日を表示しています
    output_info_list = sorted(company_info_list, key=lambda x: x["情報更新日"], reverse=True)
    for company_info in output_info_list:
        print("会社名：{}、情報更新日:{}".format(company_info["会社名"], company_info["情報更新日"]))


    #終了
    driver.close()
    
    write_normal_log("★★処理終了★★")

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
