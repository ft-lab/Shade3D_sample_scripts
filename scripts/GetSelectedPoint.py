# -----------------------------------------------------.
# 選択頂点の座標値を取得.
#    形状編集モードで頂点が選択されている場合、.
#    ブラウザで選択された形状の選択頂点の座標値を一覧.
#
# @title \en Get coordinate value of selected vertices \enden
# @title \ja 選択頂点の座標値を取得 \endja
# -----------------------------------------------------.

scene = xshade.scene()

# 指定形状の選択頂点の座標値(ローカル座標値)を表示.
def PrintPointsPosition (shape):
    if len(shape.active_vertex_indices) == 0 or (shape.type != 7 and shape.type != 4):
        return

    print "[ " + shape.name + " ]"

    if shape.type == 7:  # ポリゴンメッシュの場合.
        for pIndex in shape.active_vertex_indices:
            print shape.vertex(pIndex).position

    if shape.type == 4:  # 線形状の場合.
        for pIndex in shape.active_vertex_indices:
            print shape.control_point(pIndex).position

    print ""

for shape in scene.active_shapes:
    PrintPointsPosition(shape)

