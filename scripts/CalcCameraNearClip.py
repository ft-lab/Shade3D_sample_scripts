# -----------------------------------------------------.
# 透視投影カメラの近クリップ面までの距離を計算.
#
# @title \en Calculate near clip plane of perspective projection camera \enden
# @title \ja 透視投影カメラの近クリップ面までの距離を計算 \endja
# -----------------------------------------------------.
import numpy
import math

scene = xshade.scene()

# 近クリップ面までの距離を計算.
def m_calcNearClip (zDist):
  wvMat = numpy.matrix(scene.world_to_view_matrix)
  wdMat = numpy.matrix(scene.world_to_device_matrix)
  nearDist = 0.0

  # ビュー座標でのzDist距離をワールド座標に変換.
  vDir = numpy.array([0.0, 0.0, zDist, 1.0])
  wDir = numpy.dot(vDir, wvMat.I)
  wDir = numpy.array([wDir[0,0], wDir[0,1], wDir[0,2],wDir[0,3]])

  # ワールド座標でのwDirベクトルをデバイス座標に変換.
  v4 = numpy.dot(wDir, wdMat)
  v4 = [v4[0,0], v4[0,1], v4[0,2], v4[0,3]]
  z = v4[2]
  w = v4[3]
  if w > z:
    nearDist = w - z

  return nearDist

def calcNearClip ():
  nearDist = m_calcNearClip(-5000.0)
  if math.fabs(nearDist) < 1e-7:
    nearDist = m_calcNearClip(5000.0)

  return nearDist

nearPlane = calcNearClip()
print "近クリップ面までの距離 : " + str(nearPlane)
