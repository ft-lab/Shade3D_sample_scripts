# -----------------------------------------------------.
# 独立した表面材質を持つ形状を検索.
#
# @title \en Search for independent materials \enden
# @title \ja 独立した表面材質を検索 \endja
# -----------------------------------------------------.

scene = xshade.scene()

# 階層をたどり、独立した材質を持つ形状を検索
# @param[in]  shape         対象形状.
# @param[out] searchShapes  独立した材質を持つ形状を格納.
def searchMaterials (shape, searchShapes):
  if shape.type == 2 and shape.part_type == 11:  # カメラ.
    return
  if shape.type == 3:  # 光源.
    return
  if shape.type == 10:  # マスターイメージ.
    return
  if shape.type == 8:  # マスターサーフェス.
    return

  # マスターサーフェスを持たない場合.
  if shape.master_surface == None:
    # 表面材質を持つ場合.
    if shape.has_surface_attributes:
      searchShapes.append(shape)

  if shape.has_son:
    s = shape.son
    while s.has_bro:
      s = s.bro
      searchMaterials(s, searchShapes)

# 形状のブラウザ上のパスを取得.
def getShapePath (shape):
  pathStr = shape.name

  s = shape
  while s.has_dad:
    s = s.dad
    pathStr = s.name + "/" + pathStr

  return pathStr

# shapeから階層構造をたどって出力.
rootShape = scene.shape  # ルート形状.

searchShapesA = []
searchMaterials(rootShape, searchShapesA)

print "独立した表面材質数 : " + str(len(searchShapesA))
print ""

for shape in searchShapesA:
  print "  " + getShapePath(shape)


