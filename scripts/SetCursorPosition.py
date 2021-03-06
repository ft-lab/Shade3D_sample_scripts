# -----------------------------------------------------.
# 3次元カーソル位置を指定.
#     3次元カーソル位置を選択形状の中心にする.
#
# @title \en Specify 3D cursor position \enden
# @title \ja 3次元カーソル位置を指定 \endja
# -----------------------------------------------------.

scene = xshade.scene()

# 選択形状の中心位置.
shape = scene.active_shape()
centerPos = shape.center_position  # ワールド座標での中心.

# 3次元カーソル位置を変更.
scene.cursor_position = centerPos

