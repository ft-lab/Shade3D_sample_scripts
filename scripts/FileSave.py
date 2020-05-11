# -----------------------------------------------------.
# テキストファイルの内容をファイル保存.
# 
# @title \en Save the contents of a text file as a file \enden
# @title \ja テキストファイルの内容をファイル保存 \endja
# -----------------------------------------------------.

# 保存する文字列.
textStr = "item1\nテストデータ\n"

# ファイルダイアログボックスを表示し、保存するフルパスを取得.
dialog = xshade.create_dialog()
filePath = dialog.ask_path(False, "TEXT(.txt)|txt")

if filePath != "":
    # ファイルパスをPythonで理解できるようにUTF-8から変換.
    filePath = filePath.decode('utf-8')

    try:
        # ファイルを出力用に開く.
        f = open(filePath, mode='w')

        # テキストを出力.
        f.write(textStr)

        # ファイルを閉じる
        f.close()
    except Exception as e:
        print "出力に失敗 : " + str(e)
      
