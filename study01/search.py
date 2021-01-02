
### 検索ツールサンプル
### これをベースに課題の内容を追記してください
import os
import csv

# 検索ソース
source=["ねずこ","たんじろう","きょうじゅろう","ぎゆう","げんや","かなお","ぜんいつ"]

### 検索ツール
def search():
    #　追加の検索ソースファイル名
    filePath = "add.csv"
    # 書き込みモード
    writeMode = "w"
    
    word =input("鬼滅の登場人物の名前を入力してください >>> ")
    
    ### ここに検索ロジックを書く
    
    if os.path.exists(filePath):
        # ファイルがある場合、追記モード
        writeMode = "a"
        # 追加ファイルから取得・追加する
        with open(filePath, encoding='shift_jis') as f:
            reader = csv.reader(f)
            for row in reader:
                source.extend(row)
    
    # 検索ソースから検索
    if word in source:
        print("{}が見つかりました".format(word))
    else :
        print("{}は見つかりません".format(word))
        print("{}を追加します".format(word))
        # 見つからない場合、CSVファイルに追加
        with open(filePath, writeMode, newline = "", encoding='shift_jis') as f:
            writer = csv.writer(f)
            writer.writerow([word])
  

if __name__ == "__main__":
    search()