import eel
import sys
import socket
import control 
import datetime
import traceback

# エラーメッセージ
ERROR_MESSAGE = "[{}]ERROR:{}{}"
item_master = []
# ブラウザ引数
CHROME_ARGS = [
    '--incognit',  # シークレットモード
    '--disable-http-cache',  # キャッシュ無効
    '--disable-plugins',  # プラグイン無効
    '--disable-extensions',  # 拡張機能無効
    '--disable-dev-tools',  # デベロッパーツールを無効にする
]

def write_error_log(e):
    """
    エラーログ書き込み
    """
    print("call:{}".format(sys._getframe().f_code.co_name))

    dt_now = datetime.datetime.now()
    message = ERROR_MESSAGE.format(dt_now, "", traceback.format_exc())

    with open("error_log.log", "a", newline = "", encoding='utf-8') as f:
        f.write(message)
        f.write("\n")
        
    print(traceback.format_exc())


def exit(arg1, arg2):  # 終了時の処理
    """
    終了処理
    """
    print("call:{}".format(sys._getframe().f_code.co_name))

    sys.exit(0)

@eel.expose
def search_lancers(url, param):
    """
     ランサーズの案件検索
    """
    print("call:{}".format(sys._getframe().f_code.co_name))
    result_disp = ""
    print(param)
    try:
        result_disp = control.search_lancers(url, param)
        
    except Exception as e:
        write_error_log(e)
        result = {"result":"ng", "message":"エラー情報：{}".format(e)}
        return result

    return result_disp

@eel.expose
def search_crowdworks(url, param):
    """
     クラウドワークスの案件検索
    """
    print("call:{}".format(sys._getframe().f_code.co_name))
    result_disp = ""
    try:
        result_disp = control.search_crowdworks(url, param)
        
    except Exception as e:
        write_error_log(e)
        result = {"result":"ng", "message":"エラー情報：{}".format(e)}
        return result

    return result_disp


##  初期処理 
eel.init("web")

##　マスタ情報を設定
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 0))
port = s.getsockname()[1]
s.close()
print("port:{}".format(port))

start_options = {
    'mode': "chrome",
    'port': port,
    'size': (1000,900),
    'close_callback' : exit,
    'default_path': "main.html",
    'cmdline_args': CHROME_ARGS
}
# _start_args = {
#     'mode':             "chrome",                   # What browser is used
#     'host':             'localhost',                # Hostname use for Bottle server
#     'port':             8000,                       # Port used for Bottle server (use 0 for auto)
#     'block':            True,                       # Whether start() blocks calling thread
#     'jinja_templates':  None,                       # Folder for jinja2 templates
#     'cmdline_args':     ['--disable-http-cache'],   # Extra cmdline flags to pass to browser start
#     'size':             None,                       # (width, height) of main window
#     'position':         None,                       # (left, top) of main window
#     'geometry':         {},                         # Dictionary of size/position for all windows
#     'close_callback':   None,                       # Callback for when all windows have closed
#     'app_mode':  True,                              # (Chrome specific option)
#     'all_interfaces': False,                        # Allow bottle server to listen for connections on all interfaces
#     'disable_cache': True,                          # Sets the no-store response header when serving assets
#    'default_path': 'index.html',                   # The default file to retrieve for the root URL
#    'app': btl.default_app(),                       # Allows passing in a custom Bottle instance, e.g. with middleware
# }

condition = control.select_search_info()
eel.js_function(condition) # JSON serializableでないとダメ
eel.start("main.html", options=start_options, suppress_error=True)
