import eel
import sys
import socket
import pos_system 
import object_class as objc

item_master = []
order = objc.Order()
CHROME_ARGS = [
    '--incognit',  # シークレットモード
    '--disable-http-cache',  # キャッシュ無効
    '--disable-plugins',  # プラグイン無効
    '--disable-extensions',  # 拡張機能無効
    '--disable-dev-tools',  # デベロッパーツールを無効にする
]
@eel.expose
def input_code_amount(code, amount):
    """
     商品コードと個数を入力
    """
    global order
    result = pos_system.input_code_amount(code, amount, item_master, order)
    response = result[0]
    
#    if "ok" == response.get("result"):
#        order.add_item_order(result[1])
    
    return response

@eel.expose
def input_deposit(code, amount, deposit):
    """
     お預かり金額まで入力
    """
    global order
    response = pos_system.input_deposit(order, deposit, item_master)
    
    if "ok" == response.get("result"):
        order = objc.Order()
    
    return response
    
@eel.expose
def get_master_init_info():
    """
    item_master.csvからデータを取得して
    JSON形式で出力
    初期表示に使用
    """
    return pos_system.get_master_info_json()


def exit(arg1, arg2):  # 終了時の処理
    """
    終了処理
    """
    sys.exit(0)

##  初期処理 
eel.init("web")

##　マスタ情報を設定
item_master = pos_system.get_master_info_list() 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 0))
port = s.getsockname()[1]
s.close()
print("port:{}".format(port))

start_options = {
    'mode': "chrome",
    'port': port,
    'size': (700,900),
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
eel.start("main.html", options=start_options, suppress_error=True)
