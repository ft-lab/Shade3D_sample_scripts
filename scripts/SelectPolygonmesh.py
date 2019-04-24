# -----------------------------------------------------.
# シーンのポリゴンメッシュをすべて選択.
#
# @title \en Select all polygon meshes \enden
# @title \ja ポリゴンメッシュをすべて選択 \endja
# -----------------------------------------------------.

scene = xshade.scene()

# 階層をたどってポリゴンメッシュを格納.
def getPolygonmeshes (shape, polygonmeshList):
    if shape.type == 7:
        polygonmeshList.append(shape)

    if shape.has_son:
        s = shape.son
        while s.has_bro:
           s = s.bro
           getPolygonmeshes(s, polygonmeshList)

# shapeから階層構造をたどってポリゴンメッシュのみ格納.
rootShape = scene.shape  # ルート形状.
polygonmeshList = []
getPolygonmeshes(rootShape, polygonmeshList)

# ポリゴンメッシュのみを選択.
if len(polygonmeshList) > 0:
    scene.active_shapes = polygonmeshList

