# -----------------------------------------------------.
# 選択された2つの頂点(コントロールポイント)の長さを計算.
#
# @title \en Calculate the length of two selected vertices \enden
# @title \ja 選択された2つの頂点(コントロールポイント)の長さを計算 \endja
# -----------------------------------------------------.
import math

scene = xshade.scene()

#---------------------------------------.
# 指定の形状で選択された2頂点の長さを計算.
# @param[in] shape       対象形状.
#---------------------------------------.
def getTwoPointsLength (shape):
    # ポリゴンメッシュでも線形状でもない場合はスキップ.
    if shape.type != 7 and shape.type != 4:
        print 'ポリゴンメッシュまたは線形状を選択してください。'
        return

    # 選択されている頂点（コントロールポイント）のインデックスと選択数を取得.    
    vCou = shape.total_number_of_control_points
    selectVIndices = []
    selectVCou = 0
    if shape.type == 4:     # 線形状の場合.
        for i in range(vCou):
            if shape.get_active_control_point(i):
                selectVIndices.append(i)
                selectVCou += 1
                if selectVCou > 2:
                    break

    else:       # ポリゴンメッシュの場合.
        for i in range(vCou):
            vertexD = shape.vertex(i)
            if vertexD.active:
                selectVIndices.append(i)
                selectVCou += 1
                if selectVCou > 2:
                    break
    if selectVCou > 2:
        print '頂点またはコントロールポイントが2つ以上選択されています。'
        return
    if selectVCou < 2:
        print '頂点またはコントロールポイントを2つ選択してください。'
        return

    # 2つの頂点（コントロールポイント）を取得.
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    if shape.type == 4:     # 線形状の場合.
        p0 = shape.control_point(selectVIndices[0]).position
        p1 = shape.control_point(selectVIndices[1]).position
    else:       # ポリゴンメッシュの場合.
        p0 = shape.vertex(selectVIndices[0]).position
        p1 = shape.vertex(selectVIndices[1]).position

    # 距離を計算.
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    dz = p1[2] - p0[2]
    distV = math.sqrt(dx * dx + dy * dy + dz * dz)
    print 'point(' + str(selectVIndices[0]) + ') - point(' + str(selectVIndices[1]) + ') : ' + str(distV) + ' mm'

shape = scene.active_shape()
getTwoPointsLength(shape)



