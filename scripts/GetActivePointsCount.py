# -----------------------------------------------------.
# 線形状で選択されたコントロールポイント数を取得.
#
# @title \en Get the number of selected control points \enden
# @title \ja 選択されたコントロールポイント数を取得 \endja
# -----------------------------------------------------.
scene = xshade.scene()

# 階層をたどる再帰.
def getSelectedControlPointsCount (shape):
  cou = 0

  if shape.type == 4:  # 線形状の場合.
    totalCou = shape.total_number_of_control_points
    for i in range(totalCou):
      if shape.get_active_control_point(i):
        cou += 1

  if shape.has_son:
    s = shape.son
    while s.has_bro:
      s = s.bro
      cou += getSelectedControlPointsCount(s)
  return cou

# shapeから階層構造をたどって出力.
aCou = 0
for shape in scene.active_shapes:
  aCou += getSelectedControlPointsCount(shape)

print '選択されたコントロールポイント数 : ' + str(aCou)

