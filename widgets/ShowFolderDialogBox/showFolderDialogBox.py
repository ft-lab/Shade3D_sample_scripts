# フォルダ選択ダイアログボックスを表示.
dialog = xshade.create_dialog()
folderPathStr = dialog.ask_folder()
if folderPathStr == None:
    folderPathStr = ""

# 戻り値はresultに入れる.
result = folderPathStr
