# -----------------------------------------------------.
# 線形状の長さを計算.
#   ブラウザで選択された線形状の長さを表示。曲線の場合は近似になる.
#
# @title \en Calculate length of line shape \enden
# @title \ja 線形状の長さを計算 \endja
# -----------------------------------------------------.
import numpy
import math

#---------------------------------------.
# ゼロチェック.
#---------------------------------------.
def isZero (v):
	minV = 1e-5
	if v > -minV and v < minV:
		return True
	return False

#---------------------------------------.
# ベクトルの減算.
# @param[in] v1  (x, y, z)の3要素.
# @param[in] v2  (x, y, z)の3要素.
#---------------------------------------.
def subVec3Vec3 (v1, v2):
	vec3_1 = numpy.array(v1)
	vec3_2 = numpy.array(v2)
	
	return vec3_1 - vec3_2

#---------------------------------------.
# ベクトルの長さを計算.
#---------------------------------------.
def lengthVec3 (v):
	vec3 = numpy.array(v)
	return numpy.linalg.norm(vec3)

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
# 指定の形状が線形状の場合に、長さを計算.
# @param[in] shape       対象形状.
# @param[in] lineDivCou  ラインの全体の分割数.
#---------------------------------------.
def getLineLength (shape, lineDivCou):
    if shape.type != 4:  # 線形状でない場合.
        return 0.0
    
    vCou = shape.total_number_of_control_points
    vList = []

    divCou = lineDivCou / vCou
    if divCou < 4:
        divCou = 4
    divD   = 1.0 / float(divCou)

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

    # ラインの全体長を計算.
    vLineLenList = []
    allLen = 0.0
    for i in range(len(vList) - 1):
        lenV = lengthVec3(subVec3Vec3(vList[i + 1] , vList[i]))
        vLineLenList.append(lenV)
        allLen += lenV

    return allLen

# ----------------------------------.
# 選択された形状の長さを取得.
# ----------------------------------.
scene = xshade.scene()
shape = scene.active_shape()

# shapeの長さを計算.
lineLenV = getLineLength(shape, 100)

print "[" + shape.name + "] length = " + str(lineLenV) + " mm"
