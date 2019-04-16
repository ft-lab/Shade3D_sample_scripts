# -----------------------------------------------------.
# シーンの各要素数を取得.
#   カメラ数/光源数/ポリゴンメッシュ数/マスターイメージ数/マスターサーフェス数を取得.
# -----------------------------------------------------.

scene = xshade.scene()

# 階層をたどる再帰.
def traceHierarchy (shape, counterA):
  if shape.type == 2 and shape.part_type == 11:  # カメラ.
    counterA[0] += 1
  if shape.type == 3:  # 光源.
    counterA[1] += 1
  if shape.type == 7:  # ポリゴンメッシュ.
    counterA[2] += 1
  if shape.type == 10:  # マスターイメージ.
    counterA[3] += 1
  if shape.type == 8:  # マスターサーフェス.
    counterA[4] += 1

  if shape.has_son:
    s = shape.son
    while s.has_bro:
      s = s.bro
      traceHierarchy(s, counterA)

# shapeから階層構造をたどって出力.
rootShape = scene.shape  # ルート形状.

counterA = [0, 0, 0, 0, 0]
traceHierarchy(rootShape, counterA)

print "カメラ数 : " + str(counterA[0])
print "光源数 : " + str(counterA[1])
print "ポリゴンメッシュ数 : " + str(counterA[2])
print "マスターイメージ数 : " + str(counterA[3])
print "マスターサーフェス数 : " + str(counterA[4])

