# -----------------------------------------------------.
# 線形状をポリゴンメッシュのエッジに変換.
#
# @title \en Convert line shape to polygon mesh edges \enden
# @title \ja 線形状をポリゴンメッシュのエッジに変換 \endja
# -----------------------------------------------------.
import numpy
import math

scene = xshade.scene()

#---------------------------------------.
# ゼロチェック.
#---------------------------------------.
def isZero (v):
  minV = 1e-5
  if v > -minV and v < minV:
    return True
  return False

#---------------------------------------.
# ベジェ上の位置を計算.
#---------------------------------------.
def getBezierPoint (v1Pos, v1Out, v2In, v2Pos, fPos):
  fMin = 1e-6

  rPos = [0.0, 0.0, 0.0]
  cPos = []
  cPos.append([v1Pos[0], v1Pos[1], v1Pos[2]])
  cPos.append([v1Out[0], v1Out[1], v1Out[2]])
  cPos.append([v2In[0],  v2In[1],  v2In[2]])
  cPos.append([v2Pos[0], v2Pos[1], v2Pos[2]])

  fPos2 = float(fPos)
  fPos2 = max(0.0, fPos2)
  fPos2 = min(1.0, fPos2)
  
  if isZero(fPos2):
    rPos = cPos[0]
    return rPos

  if isZero(fPos2 - 1.0):
    rPos = cPos[3]
    return rPos

  # ベジェ曲線の計算.
  t   = fPos2
  t2  = 1.0 - t
  t2d = t2 * t2
  td  = t * t
  b1  = t2d * t2
  b2  = 3.0 * t * t2d
  b3  = 3.0 * td * t2
  b4  = t * td

  for i in range(3):
    rPos[i] = b1 * cPos[0][i] + b2 * cPos[1][i] + b3 * cPos[2][i] + b4 * cPos[3][i]

  return rPos

#---------------------------------------.
# 線形状を直線の集まりに分解.
# @param[in] shape       対象形状.
# @param[in] lineDivCou  ラインの全体の分割数.
# @return ポイントの配列.
#---------------------------------------.
def getLinePoints (shape, lineDivCou):
  vCou = shape.total_number_of_control_points
  vList = []
  if shape.type != 4 or vCou < 2:  # 線形状でない場合.
    return vList
  
  divCou = lineDivCou / vCou
  if divCou < 4:
    divCou = 4
  divD = 1.0 / float(divCou)

  # ベジェをポイントで保持.
  for i in range(vCou):
    if shape.closed == False and (i + 1 >= vCou):
      break
    p1 = shape.control_point(i)
    p2 = shape.control_point((i + 1) % vCou)

    dPos = 0.0
    for j in range(divCou + 1):
      p = getBezierPoint(p1.position, p1.out_handle, p2.in_handle, p2.position, dPos)
      if (i == 0) or (i != 0 and j > 0):
        vList.append(p)
      dPos += divD

  return vList

#---------------------------------------.
# ポイントのみで構成された配列情報から、等間隔になるように再計算.
# @param[in] vList   ポイントの配列.
# @param[in] divCou  新しいラインの分割数.
# @return ポイントの配列.
#---------------------------------------.
def recalcLinePoints (vList, divCou):
  # numpyの形式に配列に格納し直す.
  vListLen = len(vList)
  if vListLen < 2:
      return []

  posA = []
  for i in range(vListLen):
      posA.append(numpy.array([vList[i][0], vList[i][1], vList[i][2]]))

  # ラインの長さを計算.
  allLen = 0.0
  lenList = []
  for i in range(vListLen - 1):
    vLen = numpy.linalg.norm(posA[i + 1] - posA[i])
    lenList.append(vLen)
    allLen += vLen

  dLen = allLen / (divCou - 1.0)
  newPosA = []
  newPosA.append([posA[0][0], posA[0][1], posA[0][2]])
  dPos = 0.0
  for i in range(vListLen - 1):
    len1 = lenList[i]

    if dPos + len1 < dLen:
      dPos += len1
      continue

    dPos2 = 0.0
    while dPos2 < len1:
      dd = (dPos2 + (dLen - dPos)) / len1
      p = (posA[i + 1] - posA[i]) * dd + posA[i]
      newPosA.append([p[0], p[1], p[2]])
      if len(newPosA) >= divCou - 1:
        break
      dd2 = dLen - dPos
      if dPos2 + dd2 + dLen > len1:
        dPos = len1 - (dPos2 + dd2)
        break
      dPos2 += dd2
      dPos = 0.0

    if len(newPosA) >= divCou - 1:
      break

  newPosA.append([posA[-1][0], posA[-1][1], posA[-1][2]])
  return newPosA

# ---------------------------------------------.
shape = scene.active_shape()

if shape.type != 4 or shape.total_number_of_control_points < 2:
  xshade.show_message_box('ポイント数が2以上の線形状を選択してください。', False)

else:
  # ダイアログボックスの作成と表示.
  dlg = xshade.create_dialog_with_uuid('05783960-e90b-4a70-9488-daefa220447d')
  div_id = dlg.append_int('分割数')
  dlg.set_value(div_id, 10)
  dlg.set_default_value(div_id, 10)

  dlg.append_default_button()

  if dlg.ask("線形状をポリゴンメッシュのエッジに変換"):
    rDivCou = dlg.get_value(div_id) + 1
    if rDivCou < 2:
      rDivCou = 2

    # 線形状をポイントで分割.
    divCou = min(40, rDivCou * 4)
    vList = getLinePoints(shape, divCou)
    vList2 = recalcLinePoints(vList, rDivCou)
    if shape.closed:
      vList2.pop()

    # ポリゴンメッシュとして配置.
    scene.begin_creating()
    scene.begin_polygon_mesh(None)

    vCou = len(vList2)
    for p in vList2:
      scene.append_polygon_mesh_vertex(p)
    
    vCou2 = vCou
    if shape.closed == False:
      vCou2 = vCou2 - 1

    for i in range(vCou2):
      i0 = i
      i1 = (i + 1) % vCou
      scene.append_polygon_mesh_edge(i0, i1)

    scene.end_polygon_mesh()
    scene.end_creating()
