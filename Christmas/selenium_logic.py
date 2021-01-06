from selenium.webdriver import Chrome, ChromeOptions
import time
import os
import sys
import requests
from bs4 import BeautifulSoup

# Chromeを起動する関数
def set_driver(headless_flg):
    
    # driverを起動
    if os.name == 'nt': #Windows
        driver_path = "./chromedriver.exe"
    elif os.name == 'posix': #Mac
        driver_path = "./chromedriver"

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
#    return Chrome(executable_path=common_func.resource_path(driver_path), options=options)
    return Chrome(executable_path=driver_path, options=options)

def __get_text_by_css(driver, css_str):
    """
    cssを指定して、textを取得する
    """
    flg = len(driver.find_elements_by_css_selector(css_str))
    result = ""
    if flg != 0:
        result = driver.find_element_by_css_selector(css_str).get_attribute("textContent")
    
    return result

def get_lancers_info(driver):
    """
    現在開いているランサーズの情報を取得する
    """

    # カテゴリから探す
    lancers_array = []
    main_div = driver.find_elements_by_css_selector("div.c-media__content")
    
    for div in main_div:
        # 案件名 c-media__title-inner
        name = div.find_element_by_css_selector(".c-media__title-inner").text
        name = name.replace("\n", " ")
        # 価格情報（プロジェクト等） c-badge__text
        price_info = div.find_element_by_css_selector(".c-badge__text").text
        # 価格 c-media__job-price
        price = div.find_element_by_css_selector(".c-media__job-price").text
        # 提案数 c-media__job-number
        suggestion = __get_text_by_css(div, ".c-media__job-propose span.c-media__job-number")
        # URL c-media__title
        url = div.find_element_by_css_selector("a").get_attribute("href")
        # 残り時間（もしくは締め切り）
        remaining = __get_text_by_css(div,".c-media__job-time__remaining")
        
        lancers_info={"案件名":name,
                     "仕事スタイル":price_info,
                     "価格":price,
                     "URL":url,
                      "残り時間":remaining,
                     "提案数":suggestion,
                     }
        lancers_array.append(lancers_info)
        
    return lancers_array

        
def get_lancers(url, param):
    """"
    ランサーズから情報を取得する
    0:案件情報（リスト）
    1:ログイン失敗フラグ
    """
    print("call:{}".format(sys._getframe().f_code.co_name))
    lancers_array = []
    driver = set_driver(True)
    #　ログイン失敗フラグ
    login_fail_flg = False
    
    if len(param["email"]) > 0 and len(param["password"]) > 0:
        driver.get("https://www.lancers.jp/user/login?ref=header_menu")
        driver.find_element_by_id("UserEmail").clear()
        driver.find_element_by_id("UserEmail").send_keys(param["email"])
        
        driver.find_element_by_id("UserPassword").clear()
        driver.find_element_by_id("UserPassword").send_keys(param["password"])
        
        driver.find_element_by_id("form_submit").click()
        login_fail_flg = "login" in driver.current_url
        time.sleep(2)
    
    sort = "started"
    if len(param["sort"]) > 0:
        sort = param["sort"]
        
    option = "?open=1&show_description=1&" + "sort=" + sort + "&work_rank%5B%5D=0&work_rank%5B%5D=1&work_rank%5B%5D=2&work_rank%5B%5D=3"
    BASE_URL = url
    # Webサイトを開く
    driver.get(BASE_URL + option)
    time.sleep(5)
    # 1page目
    lancers_array.extend(get_lancers_info(driver))

    while True:
        if len(driver.find_elements_by_css_selector(".pager__item--next > a.pager__item__anchor")) != 1:
            #次へがなくなったら終了
            break
        
        driver.find_element_by_css_selector(".pager__item--next > a.pager__item__anchor").click()
        time.sleep(3)
        lancers_array.extend(get_lancers_info(driver))

    driver.close()
    driver.quit()

    return lancers_array, login_fail_flg

def get_crowdworks_info(driver):
    """
    現在開いているクラウドワークスの情報を取得する
    """
    # カテゴリから探す
    info_array = []
    main_div = driver.find_elements_by_css_selector("div.item.job_item")
    
    for div in main_div:
        # 案件名
        name = div.find_element_by_css_selector("a").text
        name = name.replace("\n", " ")
        # 価格情報（プロジェクト等） cw-label
        price_info = div.find_element_by_css_selector("span.cw-label").text
        # 価格 
        price = div.find_element_by_css_selector("div.inner_cell b").text
        # URL c-media__title
        url = div.find_element_by_css_selector("a").get_attribute("href")
        # 残り時間（もしくは締め切り）
        remaining = __get_text_by_css(div,"div.entry_data.expires .inner_cell b")
        
        crowdworks_info={"案件名":name,
                     "仕事スタイル":price_info.replace("\n", " ").strip(" "),
                     "価格":price.replace("\n", " ").strip(" "),
#                     "契約数":suggestion.replace("\n", " ").strip(" "),
                     "URL":url,
                      "残り時間":remaining.replace("\n", " ").strip(" "),
#                      "残り時間2":remaining2.replace("\n", " ").strip(" "),
                     }

        
        
#        '応募した人': '17 人', '契約した人': '1 人', '募集人数': '2 人', '気になる！リスト': '13 人'
        try:
            html = requests.get(url)
            soup = BeautifulSoup(html.content, "html.parser")
            number_array = soup.select("table.application_status_table td")
            crowdworks_info["応募した人"] = number_array[0].string.replace("\n","").strip(" ")
            crowdworks_info["契約した人"] = number_array[1].string.replace("\n","").strip(" ")
            crowdworks_info["募集人数"] = number_array[2].string.replace("\n","").strip(" ")
            crowdworks_info["気になる！リスト"] = number_array[3].string.replace("\n","").strip(" ")
        except Exception as e:
            #　タスクの場合、表示内容が異なるため
            print(e)
            crowdworks_info["応募した人"] = ""
            crowdworks_info["契約した人"] = ""
            crowdworks_info["募集人数"] = ""
            crowdworks_info["気になる！リスト"] = ""
            
        info_array.append(crowdworks_info)
        
    
    return info_array

        
        
def get_crowdworks(url):
    """"
    クラウドワークスから情報を取得する
    """
    print("call:{}".format(sys._getframe().f_code.co_name))
    info_array = []
    driver = set_driver(True)
#    BASE_URL = "https://www.lancers.jp/work/search?ref=search_topic&show_description=1&sort=client&work_rank%5B%5D=0&work_rank%5B%5D=2&work_rank%5B%5D=3"
    # Webサイトを開く
    driver.get(url)
    time.sleep(2)
    # 
    driver.find_element_by_css_selector("label.cw-checkbox_inline input").click()
    
    time.sleep(2)

    print(driver.find_element_by_css_selector(".result_count span").text)

    # 1page目
    info_array.extend(get_crowdworks_info(driver))
    
    while True:
        if len(driver.find_elements_by_css_selector(".to_next_page")) != 1:
            #次へがなくなったら終了
            break
        
        driver.find_element_by_css_selector(".to_next_page").click()
        time.sleep(3)
        info_array.extend(get_crowdworks_info(driver))
        
    driver.close()
    driver.quit()
    
    return info_array



