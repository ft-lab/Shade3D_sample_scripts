# -----------------------------------------------------.
# レンダリングイメージのZ値(ZDepth)を取得し、
# マスターイメージとして出力.
#
# @title \en Get the ZDepth of the rendered image \enden
# @title \ja レンダリングイメージのZ値(ZDepth)を取得 \endja
# -----------------------------------------------------.
scene = xshade.scene()

depthLayer = scene.rendering.image_layer('ZDepth')
if depthLayer != None and scene.rendering.image != None:
  # Depth値の最小と最大.
  minDist = depthLayer.minimum_value
  maxDist = depthLayer.maximum_value

  srcImage = depthLayer.image
  width  = srcImage.size[0]
  height = srcImage.size[1]

  # マスターイメージを作成.
  scene.begin_creating()
  masterImage = scene.create_master_image('depth_image')
  masterImage.image = scene.rendering.image.duplicate()
  dstImage = masterImage.image
  scene.end_creating()

  # ピクセルごとに色をコピー.
  for y in range(height):
    for x in range(width):
      # Z値を0.0 - 1.0に変換.
      col = srcImage.get_pixel_rgba(x, y)
      zDist = col[0]
      zVal = (zDist - minDist[0]) / (maxDist[0] - minDist[0])
      col = [zVal, zVal, zVal, 1.0]
      dstImage.set_pixel_rgba(x, y, col)
  dstImage.update()
