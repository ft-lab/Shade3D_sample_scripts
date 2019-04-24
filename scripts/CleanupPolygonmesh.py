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
    # 形状編集モードに入る.
    scene.enter_modify_mode()

    # 面選択モード.
    scene.selection_mode = 0

    # すべての面を選択.
    for i in range(shape.number_of_faces):
        shape.face(i).active = True
    shape.update()

    # 頂点選択モード。これで、面を構成する頂点のみ選択される.
    scene.selection_mode = 2

    # 頂点の選択を反転.
    tCou = shape.total_number_of_control_points
    for i in range(tCou):
        if shape.vertex(i).active:
            shape.vertex(i).active = False
        else:
            shape.vertex(i).active = True
    
    # 選択頂点を削除.
    shape.begin_removing_control_points()

    for i in range(tCou):
        if shape.vertex(tCou - i - 1).active:
            shape.remove_control_point(tCou - i - 1)

    shape.end_removing_control_points()

    # 形状編集モードから抜ける.
    scene.exit_modify_mode()

for shape in scene.active_shapes:
    if shape.type == 7:   # ポリゴンメッシュの場合.
        CleanupPolygonmesh(shape)

