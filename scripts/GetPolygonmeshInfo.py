# -----------------------------------------------------.
# ポリゴンメッシュ情報を取得.
#   ブラウザで選択したポリゴンメッシュの情報を取得.
# -----------------------------------------------------.
scene = xshade.scene()

# ポリゴンメッシュ情報を表示.
def PrintPolygonmeshInfo (shape):
    print "[ " + shape.name + " ]"

    print "  頂点数 : " + str(shape.total_number_of_control_points)
    print "  稜線数 : " + str(shape.number_of_edges)
    print "  面数 : " + str(shape.number_of_faces)
    print "  UVレイヤ数 : " + str(shape.get_number_of_uv_layers())
    print "  フェイスグループ数 : " + str(shape.get_number_of_face_groups())
    print ""

for shape in scene.active_shapes:
    if shape.type == 7:   # ポリゴンメッシュの場合.
        PrintPolygonmeshInfo(shape)

