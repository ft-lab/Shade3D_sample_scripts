# ファイルダイアログボックスを表示.
dialog = xshade.create_dialog()
pathStr = dialog.ask_path(True, "JSON/TEXT(.json .txt)|json;txt|JSON(.json)|json|TEXT(.txt)|txt")
if pathStr == None:
    pathStr = ""

# 戻り値はresultに入れる.
result = pathStr
