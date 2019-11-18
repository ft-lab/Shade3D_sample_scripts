# -----------------------------------------------------.
# ポリゴンメッシュの頂点カラーレイヤをまとめて削除.
# ※ただしUNDO/REDOには対応していない.
# 
# @title \en Remove vertex color layers of polygon mesh at once \enden
# @title \ja ポリゴンメッシュの頂点カラーレイヤをまとめて削除 \endja
# -----------------------------------------------------.
scene = xshade.scene()

# ---------------------------------------------.
# ポリゴンメッシュの頂点カラーを削除.
# ---------------------------------------------.
def clearMeshVertexColorLayers(shape):
    if shape.type != 7:
        return False
    
    shape.clear_vertex_color_layers()
    shape.update()

    return True

# -------------------------------------------------.
chkF = False
for shape in scene.active_shapes:
    if clearMeshVertexColorLayers(shape):
        chkF = True

if chkF == False:
    print 'ポリゴンメッシュを選択してください。'

