# -----------------------------------------------------.
# 検索パスの一覧と追加.
#   importでファイルを分けて管理する際に使用.
# -----------------------------------------------------.
import sys
import pprint

# 新たに検索パスを追加。同一のパスを追加しないようにしている.
def appendSysPath(newPath):
    existF = False
    for path in sys.path:
      if path == newPath:
        existF = True
        break

    if existF:
      return

    sys.path.append(newPath)

# Pythonファイルの検索パスを表示.
pprint.pprint(sys.path)

# 新しくパスを追加.
# appendSysPath("C:/Users/ログインユーザ名/Documents/Shade3D/Shade3D ver.17/scripts_sub")
#
# import xxxx のようにしてxxxx.pyをインポートし、xxxx.foo() のように関数を実行.

