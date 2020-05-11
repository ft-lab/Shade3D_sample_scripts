# -----------------------------------------------------.
# ファイルダイアログボックスを表示し、テキストファイルの内容をメッセージウィンドウに表示.
# 
# @title \en View file contents \enden
# @title \ja ファイル内容を表示 \endja
# -----------------------------------------------------.

# ファイルダイアログボックスを表示し、フルパスを取得.
dialog = xshade.create_dialog()
filePath = dialog.ask_path(True, "TEXT(.txt)|txt")

if filePath != "":
    # ファイルパスをPythonで理解できるようにUTF-8から変換.
    filePath = filePath.decode('utf-8')

    try:
        # ファイルを開く(テキストファイルとして開く).
        f = open(filePath)

        # 1行ずつ取り出し.
        for lineStr in f:
            # 1行の改行コードを取り除く.
            lineStr = lineStr.rstrip('\n')

            # 1行を表示.
            print lineStr

        # ファイルを閉じる
        f.close()
    except Exception as e:
        print "読み込みに失敗 : " + str(e)


