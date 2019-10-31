# -----------------------------------------------------.
# ポリゴンメッシュをワイヤーフレームに変換.
#
# @title \en Convert polygonmesh to wireframe \enden
# @title \ja ポリゴンメッシュをワイヤーフレームに変換 \endja
# -----------------------------------------------------.
import numpy
import math

scene = xshade.scene()

# -----------------------------------------------.
# 指定のポリゴンメッシュで、面に属さない頂点を削除.
# -----------------------------------------------.
def cleanupMeshVertices (shape):
    # 形状編集モードに入る.
    scene.enter_modify_mode()
    oldSelectionMode = scene.selection_mode

    # すべての面を選択.
    scene.selection_mode = 0
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

    # 元の選択モードに戻す.
    scene.selection_mode = oldSelectionMode

    # 形状編集モードから抜ける.
    scene.exit_modify_mode()

# -----------------------------------------------.
# ポリゴンメッシュをワイヤーフレームに変換.
# -----------------------------------------------.
def convMeshToWireframe (shape, lineWidth):
    if shape.type != 7:
        print 'ポリゴンメッシュを選択してください。'
        return
    
    shape.setup_plane_equation()

    zUpNormal = numpy.array([0.0, 0.0, 1.0])
    fMinDist = 1e-5

    faceVList = []
    faceOrgIndicesList = []
    tmpVersList = []
    facesCou = shape.number_of_faces
    versCou  = shape.total_number_of_control_points
    for fLoop in range(facesCou):
        faceD = shape.face(fLoop)
        fvCou = faceD.number_of_vertices
        if fvCou <= 2:
            continue

        # (x,y,z)が面法線相当.
        fNormal = shape.get_plane_equation(fLoop)

        # 法線座標系への変換行列。Z軸方向を法線とする.
        normalV = numpy.array([fNormal[0], fNormal[1], fNormal[2]])
        fnMatrix = numpy.matrix(numpy.identity(4))
        xV = numpy.array([0.0, 0.0, 0.0])
        yV = numpy.array([0.0, 0.0, 0.0])
        zV = normalV
        if math.fabs(fNormal[1]) > 0.1:
            xV = numpy.array([1.0, 0.0, 0.0])
            xV  = numpy.cross(normalV, xV)
            yV  = numpy.cross(normalV, xV)
        else :
            xV = numpy.array([0.0, 1.0, 0.0])
            xV  = numpy.cross(normalV, xV)
            yV  = numpy.cross(normalV, xV)

        lenV = numpy.linalg.norm(xV)
        if lenV == 0.0:
            continue
        xV /= lenV
        lenV = numpy.linalg.norm(yV)
        if lenV == 0.0:
            continue
        yV /= lenV

        fnMatrix[0, 0] = xV[0]
        fnMatrix[0, 1] = xV[1]
        fnMatrix[0, 2] = xV[2]
        fnMatrix[1, 0] = yV[0]
        fnMatrix[1, 1] = yV[1]
        fnMatrix[1, 2] = yV[2]
        fnMatrix[2, 0] = zV[0]
        fnMatrix[2, 1] = zV[1]
        fnMatrix[2, 2] = zV[2]

        fnMatrixInv = fnMatrix.I

        # 頂点座標を一時格納.
        vIndices = faceD.vertex_indices
        versIndices = []
        vers = []
        fCenterPos = numpy.array([0.0, 0.0, 0.0])
        for i in range(fvCou):
            p = shape.vertex(vIndices[i]).position
            p = numpy.array([p[0], p[1], p[2]])
            fCenterPos += p
            vers.append(p)
            versIndices.append(vIndices[i])
        fCenterPos /= float(fvCou)

        # 頂点間の距離がfMinDistよりも小さい場合はスキップ.
        removeI = []
        for i in range(fvCou):
            p0 = vers[i]
            p1 = vers[(i + 1) % fvCou]
            lenV = numpy.linalg.norm(p1 - p0)
            if lenV < fMinDist:
                if i + 1 < fvCou:
                    removeI.append(i)

        if len(removeI) > 0:
            for i in reversed(removeI):
                vers.pop(i)
                versIndices.pop(i)

        fvCou = len(vers)
        if fvCou <= 2:
            continue

        # 頂点座標をZ軸向きの座標系に変換.
        # この変換で、（平面上の面の場合は）Z値は0.0になる.
        for i in range(fvCou):
            p = vers[i]
            p2 = p - fCenterPos
            p2 = numpy.array([p2[0], p2[1], p2[2], 1.0])
            retM = numpy.dot(p2, fnMatrixInv)  # 法線座標系に変換.
            p2 = [retM[0,0], retM[0,1], retM[0,2]]
            vers[i] = numpy.array([p2[0], p2[1], p2[2]])

        # 面の法線座標での中心 ([0, 0, 0]になる).
        fCenter = numpy.array([0.0, 0.0, 0.0])
        for i in range(fvCou):
            fCenter += vers[i]
        fCenter /= float(fvCou)

        # エッジ間の最小距離を計算し、lineWidthの値を調整.
        lineWidth2 = lineWidth
        for i in range(fvCou):
            e0 = i
            e1 = (i + 1) % fvCou
            p0 = vers[e0]
            p1 = vers[e1]
            p0_2 = numpy.array([p0[0], p0[1], 0.0])
            p1_2 = numpy.array([p1[0], p1[1], 0.0])
            dirV = p1_2 - p0_2
            lenV = numpy.linalg.norm(dirV) * 0.2
            if lineWidth2 > lenV:
                lineWidth2 = lenV

        # TODO : エッジを内側にlineWidth2分シフト.
        tmpVers = []
        for i in range(fvCou):
            e0 = i
            e1 = (i + 1) % fvCou
            p0 = vers[e0] - fCenter
            p1 = vers[e1] - fCenter
            p0_2 = numpy.array([p0[0], p0[1], 0.0])
            p1_2 = numpy.array([p1[0], p1[1], 0.0])
            dirV = p1_2 - p0_2
            lenV = numpy.linalg.norm(dirV)
            if lenV < 1e-5:
                continue
            dirV /= lenV
            dirV2 = numpy.cross(dirV, -zUpNormal)
            lenV = numpy.linalg.norm(dirV2)
            if lenV < 1e-5:
                continue
            dirV2 /= lenV
            dirV3 = dirV2 * lineWidth2
            p0_3 = p0_2 + dirV3
            p1_3 = p1_2 + dirV3

            tmpVers.append(p0_3 + fCenter)
            tmpVers.append(p1_3 + fCenter)

        # test..tmpVersを元のローカル座標に戻す.
        for i in range(len(tmpVers)):
            p = tmpVers[i]
            p = numpy.array([p[0], p[1], p[2], 1.0])
            retM = numpy.dot(p, fnMatrix)
            p2 = numpy.array([retM[0,0], retM[0,1], retM[0,2]]) + fCenterPos
            tmpVers[i] = p2
        tmpVersList.append(tmpVers)

        #faceVList.append(vers)
        faceOrgIndicesList.append(versIndices)
    
    if len(tmpVersList) >= 1:
        nameStr = shape.name + '_wireframe'
        scene.begin_creating()
        pMesh = scene.begin_polygon_mesh(nameStr)

        # オリジナルの頂点を格納.
        for i in range(versCou):
            p = shape.vertex(i).position
            scene.append_polygon_mesh_vertex(p)
        vOffset = versCou

        # 新しいメッシュに頂点/面情報を格納.
        fIPos = 0
        fIndex = [0, 0, 0, 0]
        for fLoop in range(len(faceOrgIndicesList)):
            versOrgIndices = faceOrgIndicesList[fLoop]

            tmpVers = tmpVersList[fLoop]
            fvCou = len(tmpVers)
            for p in tmpVers:
                scene.append_polygon_mesh_vertex([p[0], p[1], p[2]])

            fvCouH = fvCou / 2
            iPos = 0
            for i in range(fvCouH):
                e0 = i
                e1 = (i + 1) % fvCouH
                fIndex[0] = versOrgIndices[e0]
                fIndex[1] = versOrgIndices[e1]

                e0_2 = iPos
                e1_2 = iPos + 1
                fIndex[2] = fIPos + e1_2 + vOffset
                fIndex[3] = fIPos + e0_2 + vOffset
                scene.append_polygon_mesh_face(fIndex)

                iPos += 2
            fIPos += fvCou

        vOffset = versCou

        scene.end_polygon_mesh()
        pMesh.make_edges()   # 稜線を生成.
        pMesh.cleanup_redundant_vertices()  # 重複頂点を削除.
        scene.end_creating()

        # 面に属さない頂点を削除.
        cleanupMeshVertices(pMesh)

        # 元の形状を隠す.
        shape.render_flag = 0
        shape.hide()

shape = scene.active_shape()

# -------------------------------------.
# ダイアログボックスの作成.
# -------------------------------------.
dlg = xshade.create_dialog_with_uuid('5C3E7C03-B4D6-40CC-B574-24F9C31206C0')

width_id = dlg.append_float('幅', 'mm')

# デフォルトボタンを追加.
dlg.append_default_button()

# 値を指定.
dlg.set_value(width_id, 10.0)

# デフォルト値を指定.
dlg.set_default_value(width_id, 10.0)

# ダイアログボックスを表示.
if dlg.ask("ポリゴンメッシュをワイヤーフレームに変換"):
  # ダイアログボックスでの値を取得.
  lineWidth = dlg.get_value(width_id)

  # ポリゴンメッシュをワイヤーフレームに変換.
  convMeshToWireframe(shape, lineWidth)


