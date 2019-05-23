# -----------------------------------------------------.
# ポリゴンメッシュのインポートした固定法線をクリア.
#
# @title \en Clear imported fixed normals of polygon mesh \enden
# @title \ja ポリゴンメッシュのインポートした固定法線をクリア \endja
# -----------------------------------------------------.

shape = xshade.scene().active_shape()

if shape.type == 7:  # ポリゴンメッシュの場合.
  shape.setup_normal()   # 法線を再計算.

  # 固定の法線をクリア.
  nFace = shape.number_of_faces
  for i in range(nFace):
    shape.face(i).normals = []
  shape.update()  # 形状を更新.
