# -----------------------------------------------------.
# ポリゴンメッシュの重複頂点で、1つの頂点のみを選択.
#
# @title \en Select single vertex of polygon mesh \enden
# @title \ja ポリゴンメッシュの重複頂点の選択を単一に \endja
# -----------------------------------------------------.
import math

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

# 2つの頂点座標が同一位置か判定.
def isSamePosition (p1, p2):
    fMin = 0.0001
    return (math.fabs(p1[0] - p2[0]) < fMin and math.fabs(p1[1] - p2[1]) < fMin and math.fabs(p1[2] - p2[2]) < fMin)

#-------------------------------------------------.

# 階層構造をたどってポリゴンメッシュのみ格納.
polygonmeshList = []
for shape in scene.active_shapes:
    getPolygonmeshes(shape, polygonmeshList)

if len(polygonmeshList) == 0:
    xshade.show_message_box('ポリゴンメッシュを選択してください。', False)

chkF = False
for shape in polygonmeshList:
    if shape.number_of_active_control_points == 0:
        continue

    # 選択されている頂点番号の配列.
    aVers = shape.active_vertex_indices
    aVersCou = len(aVers)

    # 同一頂点位置の場合、片側の選択を解除.
    for i in range(aVersCou):
        index0 = aVers[i]
        if shape.vertex(index0).active == False: continue
        v0 = shape.vertex(index0).position
            
        for j in range(i + 1, aVersCou):
            index1 = aVers[j]
            if shape.vertex(index1).active == False: continue

            v1 = shape.vertex(index1).position
            if isSamePosition(v0, v1):
                # index1の頂点の選択を解除.
                shape.vertex(index1).active = False
                chkF = True

if chkF == False:
    xshade.show_message_box('選択された頂点で、重複が存在しませんでした。', False)

