# -----------------------------------------------------.
# ポリゴンメッシュの不要な頂点/稜線を削除.
#     選択されたポリゴンメッシュの面を構成しない頂点や稜線を削除.
#
# @title \en Remove unnecessary vertices/edges of polygon mesh \enden
# @title \ja ポリゴンメッシュの不要な頂点/稜線を削除 \endja
# -----------------------------------------------------.

scene = xshade.scene()

# ポリゴンメッシュの面を構成しない頂点や稜線を削除.
def CleanupPolygonmesh (shape):
    # 面で参照される頂点を取得.
    versCou  = shape.total_number_of_control_points
    facesCou = shape.number_of_faces
    vUsedList = [0] * versCou
    for fLoop in range(facesCou):
        f = shape.face(fLoop)
        vCou = f.number_of_vertices
        for i in range(vCou):
            vUsedList[ f.vertex_indices[i] ] = 1

    # 参照されない頂点を削除.
    shape.begin_removing_control_points()

    for i in range(versCou):
        if vUsedList[i] == 0:
            shape.remove_control_point(i)

    shape.end_removing_control_points()

for shape in scene.active_shapes:
    if shape.type == 7:   # ポリゴンメッシュの場合.
        CleanupPolygonmesh(shape)

