import requests
from error_exception import HttpStatusRakutenException
import sys

ICHIBA_ITEM_URL =  "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?format=json&keyword={}&page={}&applicationId=1019079537947262807"
PRODUCT_URL =      "https://app.rakuten.co.jp/services/api/Product/Search/20170426?format=json&keyword={}&page={}&applicationId=1019079537947262807"
ICHIBA_GENRE_URL = "https://app.rakuten.co.jp/services/api/IchibaGenre/Search/20140222?format=json&genreId={}&applicationId=1019079537947262807"
RANK_URL =         "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?format=json&genreId={}&applicationId=1019079537947262807"

def get_api(url):
    result = requests.get(url)
    print(result.status_code)
    print(result.json())
    
    if result.status_code != 200 :
        error = HttpStatusRakutenException()
        error.set_param(result.status_code, result.json())
        raise error
    
    return result.json()


def get_ichiba_item_json_first(keyword):
    """"
    楽天商品検索API (初回検索)
    商品名と価格の一覧
    """
    return get_ichiba_item_json(keyword, 1)

def get_ichiba_item_json(keyword, start_page):
    """"
    楽天商品検索API 
    商品名と価格の一覧
    """
    print("call:{}".format(sys._getframe().f_code.co_name))

    url = ICHIBA_ITEM_URL.format(keyword, start_page)
        
    return get_api(url)

def get_product_json_first(keyword):
    """"
    商品価格ナビ製品検索API (初回検索)
    商品名と価格の一覧
    """
    return get_product_json(keyword, 1)

def get_product_json(keyword, start_page):
    """"
    商品価格ナビ製品検索API 
    商品名と価格の一覧
    """
    print("call:{}".format(sys._getframe().f_code.co_name))

    url = PRODUCT_URL.format(keyword, start_page)
        
    return get_api(url)


def get_genre_json(keyword):
    """"
    ジャンル検索API
    """
    print("call:{}".format(sys._getframe().f_code.co_name))
    
    url = ICHIBA_GENRE_URL.format(keyword)
        
    return get_api(url)


def get_rank_json(keyword):
    """"
    ランキング検索API
    """
    print("call:{}".format(sys._getframe().f_code.co_name))

    url = RANK_URL.format(keyword)
        
    return get_api(url)

