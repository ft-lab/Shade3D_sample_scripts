# -----------------------------------------------------.
# 未参照のイメージを一覧.
#
# @title \en List unreferenced images \enden
# @title \ja 未参照のイメージを一覧 \endja
# -----------------------------------------------------.
scene = xshade.scene()

# 未参照のイメージを格納.
def getUnreferencedMasterImages (shape, masterImageA):
  if shape.type == 10:  # マスターイメージ.
    if shape.is_master_image_being_used() == 0:  # 未参照の場合.
      masterImageA.append(shape)

  if shape.has_son:
    s = shape.son
    while s.has_bro:
      s = s.bro
      getUnreferencedMasterImages(s, masterImageA)

# 未参照のマスターイメージを取得.
rootShape = scene.shape  # ルート形状.
masterImageList = []
getUnreferencedMasterImages(rootShape, masterImageList)

# マスターイメージ名を表示.
if len(masterImageList) > 0:
  print "-- Unreferenced images --------"
  for masterImage in masterImageList:
     print masterImage.name
