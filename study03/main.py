import eel
import os
import csv
import sys

ENCODING = "utf-8"

@eel.expose
def python_function2(source_flie ,word):
    if search(source_flie, word):
        print("『{}』はあります".format(word))
        return "『{}』はあります".format(word)
    else:
        # 追加
        add_word(source_flie, word)

        print("『{}』はありません".format(word))
        return "『{}』はありません\n『{}』を追加します".format(word, word)



### 検索ツール
def search(source_flie, word):
    # 検索ソース
    source=[]
        
    if os.path.exists(source_flie):
        # 追加ファイルから取得・追加する
        with open(source_flie, encoding=ENCODING) as f:
            reader = csv.reader(f)
            for row in reader:
                source.extend(row)
    
    # 検索ソースから検索
    if word in source:
        return True
    else :
        return False

## 書き込み処理
def add_word(source_flie, word):
    # 書き込みモード
    writeMode = "w" if os.path.exists(source_flie) else "a"
    # 見つからない場合、CSVファイルに追加
    with open(source_flie, writeMode, newline = "", encoding=ENCODING) as f:
        writer = csv.writer(f)
        writer.writerow([word])


eel.init("web")

web_app_options = {
    "mode": "chrome-app",  # chromeのアプリケーションモードで起動
                           # "chrome" とすると、通常のchromeで起動
    "port": 8080,
    "chromeFlags": [
            "--start-fullscreen",  
            # "--window-size=800,600",
            # "--window-position=0,0",
    ]
}

eel.start("main.html")

def exit(arg1, arg2):  # 終了時の処理
    sys.exit(0)