# -----------------------------------------------------.
# スキンが割り当てられているポリゴンメッシュを列挙する.
#
# @title \en Enumerate skin mesh \enden
# @title \ja スキンメッシュを列挙 \endja
# -----------------------------------------------------.
scene = xshade.scene()

# スキンを持つポリゴンメッシュを格納.
def getPolygonmeshesWithSkin (shape, polygonmeshList):
  if shape.type == 7:  # ポリゴンメッシュの場合.
    if shape.skin_type >= 0:  # スキンを持つ場合.
      polygonmeshList.append(shape)

  if shape.has_son:
    s = shape.son
    while s.has_bro:
      s = s.bro
      getPolygonmeshesWithSkin(s, polygonmeshList)

# 形状のブラウザ上のパスを取得.
def getShapePath (shape):
  pathStr = shape.name

  s = shape
  while s.has_dad:
    s = s.dad
    pathStr = s.name + "/" + pathStr

  return pathStr

# shapeから階層構造をたどってスキンを持つポリゴンメッシュのみ格納.
rootShape = scene.shape  # ルート形状.
polygonmeshList = []
getPolygonmeshesWithSkin(rootShape, polygonmeshList)

# 形状名を列挙.
for shape in polygonmeshList:
  shapeName = getShapePath(shape)
  print shapeName

