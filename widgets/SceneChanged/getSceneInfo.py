# ---------------------------------------.
# シーン情報を取得.
# ---------------------------------------.
import os.path

scene = xshade.scene()

# シーンファイル名を取得.
sceneFileName = scene.file_path

fName = ''
if sceneFileName != '':
    fName = os.path.basename(sceneFileName)

# 結果を文字列で返す.
result = fName



