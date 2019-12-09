# -----------------------------------------------------.
# ポリゴンメッシュ内の直方体要素を選択.
#
# @title \en Select multiple boxes of polygon mesh \enden
# @title \ja ポリゴンメッシュ内の直方体要素を選択 \endja
# -----------------------------------------------------.
import numpy
import math

scene = xshade.scene()

# ----------------------------------------------------------.
# ポリゴンメッシュの隣接する面をたどり、面ごとのシェル番号を割り当て.
# @param[in] shape  対象ポリゴンメッシュ.
# @return  面ごとのシェル番号(0-)の配列.
# ----------------------------------------------------------.
def getMeshShellIndex (shape):
    if shape.type != 7:     # ポリゴンメッシュでない場合.
        return None

    facesCou = shape.number_of_faces
    versCou  = shape.total_number_of_control_points

    faceGIndexList = [-1] * facesCou

    # 頂点が共有する4頂点を持つ面のリストを作成.
    vFacesList = []
    for i in range(versCou):
        vFacesList.append([])
    
    for i in range(facesCou):
        f = shape.face(i)
        vCou = f.number_of_vertices
        if vCou < 3:
            continue
        for j in range(vCou):
            vIndex = f.vertex_indices[j]
            vFacesList[vIndex].append(i)

    # 隣接する面をたどり、インデックスを割り当てていく.
    fNewIndex = 0
    for fLoop in range(facesCou):
        if faceGIndexList[fLoop] >= 0:
            continue

        f = shape.face(fLoop)
        vCou = f.number_of_vertices
        if vCou < 3:
            continue

        faceIList = [fLoop]

        while len(faceIList):
            fCurIndex = faceIList[0]

            if faceGIndexList[fCurIndex] >= 0:
                faceIList.pop(0)
                continue

            f = shape.face(fCurIndex)
            vCou = f.number_of_vertices
            if vCou < 3:
                faceIList.pop(0)
                continue

            faceGIndexList[fCurIndex] = fNewIndex

            for i in range(vCou):
                i1 = f.vertex_indices[i]
                i2 = f.vertex_indices[(i + 1) % vCou]

                fList1 = vFacesList[i1]
                for j in range(len(fList1)):
                    fI = fList1[j]
                    if fI == fLoop or faceGIndexList[fI] >= 0:
                        continue

                    iCou = 0
                    f2 = shape.face(fI)
                    vCou2 = f2.number_of_vertices
                    if vCou2 < 3:
                        continue
                    
                    for k in range(vCou2):
                        vI = f2.vertex_indices[k]
                        if vI == i1 or vI == i2:
                            iCou += 1
                    
                    if iCou == 2:
                        faceIList.append(fI)

            faceIList.pop(0)
        fNewIndex += 1

    return faceGIndexList

# ----------------------------------------------------------.
# ポリゴンメッシュの6つの四角形面が直方体を構成しているかチェック.
# @param[in]  shape     対象形状.
# @param[in]  faceList  直方体の6面のインデックス.
# @return 直方体の場合はTrue, その後に6面の対面の番号を0-2で入れる配列.
# ----------------------------------------------------------.
def checkBox (shape, faceList):
    if len(faceList) != 6:
        return False, None

    # 向かい合う面の組み合わせが3つあれば直方体と判断.
    fDList = [-1] * 6
    index = 0
    for i in range(6):
        if fDList[i] >= 0:
            continue

        # 面法線.
        fNormal1 = shape.get_plane_equation(faceList[i])
        fNormal1 = numpy.array([fNormal1[0], fNormal1[1], fNormal1[2]])

        for j in range(i + 1, 6):
            if fDList[j] >= 0:
                continue
        
            # 面法線.
            fNormal2 = shape.get_plane_equation(faceList[j])
            fNormal2 = numpy.array([fNormal2[0], fNormal2[1], fNormal2[2]])

            # fNormal1とfNormal2が対面になっているか.
            v = numpy.dot(fNormal1, fNormal2)
            if math.fabs(v) > 0.999:
                fDList[i] = index
                fDList[j] = index
                index += 1
                break

    if index != 3:
        return False, None

    return True, fDList

# ----------------------------------------------------------.
# ポリゴンメッシュから直方体を構成する面番号の配列を返す.
# @param[in]  shape  対象形状.
# @return 直方体を構成する面の配列を [][6]で返す.
# ----------------------------------------------------------.
def getBoxFaces (shape):
    if shape.type != 7:     # ポリゴンメッシュでない場合.
        return None

    shape.setup_plane_equation()

    facesCou = shape.number_of_faces
    versCou  = shape.total_number_of_control_points
    if facesCou < 6 or versCou < 8:
        return None

    # 面ごとのシェル番号を取得.
    faceShellIndex = getMeshShellIndex(shape)

    maxShellIndex = -1
    for shellIndex in range(facesCou):
        if faceShellIndex[shellIndex] > maxShellIndex:
            maxShellIndex = faceShellIndex[shellIndex]
    if maxShellIndex < 0:
        return None

    # 直方体を構成する四角形面の面番号の配列を取得.
    retBoxList = []
    for shellIndex in range(maxShellIndex + 1):
        fList = []
        for i in range(len(faceShellIndex)):
            if faceShellIndex[i] == shellIndex:
                fList.append(i)

        # 6面で構成されるか.
        fCou = len(fList)
        if fCou != 6:
            continue

        # すべての面が四角形で構成されるか.
        fCou2 = 0
        for i in range(fCou):
            f = shape.face(fList[i])
            if f.number_of_vertices == 4:
                fCou2 += 1
        
        if fCou2 != 6:
            continue

        # fListに格納された面が直方体を構成するかチェック.
        retV = checkBox(shape, fList)
        if retV[0]:
            retBoxList.append(fList)

    return retBoxList

# -------------------------------------.

# 形状編集モード + 面選択モードに移行.
scene.enter_modify_mode()
scene.selection_mode = 0

for shape in scene.active_shapes:
    # すべての選択を解除.
    shape.select_all_control_points(False)

    # ポリゴンメッシュで直方体を構成する面番号を取得.
    boxList = getBoxFaces(shape)
    if len(boxList) > 0:
        print "[" + shape.name + "] : 直方体の数 " + str(len(boxList))

        # 直方体を構成する面を選択.
        for faceList in boxList:
            for faceIndex in faceList:
                shape.face(faceIndex).active = True

scene.update_figure_window()

