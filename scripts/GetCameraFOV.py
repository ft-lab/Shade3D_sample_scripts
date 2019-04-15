# -----------------------------------------------------.
# カメラの視野角度を取得.
# -----------------------------------------------------.
import math

scene = xshade.scene()

# レンダリング画像サイズを取得.
renderingImageSize = scene.rendering.image_size

# スクリーンの長辺は36mm固定.
screenDSize  = 36.0   
screenDSizeH = screenDSize * 0.5

# カメラの焦点距離値.
cameraZoom  = scene.camera.zoom

# アスペクト比.
aspect = float(renderingImageSize[0]) / float(renderingImageSize[1])
dH = 0.0
if renderingImageSize[0] > renderingImageSize[1]:
  dH = screenDSizeH / aspect
else :
  dH = screenDSizeH * aspect

# 短いほうの視野角度を計算.
cosV = cameraZoom / math.sqrt(dH * dH + cameraZoom * cameraZoom)
fovDegrees = 2.0 * math.acos(cosV) * 180.0 / math.pi

# 水平(fovH)、垂直(fovV)の視野角度を計算.
fovH = fovV = fovDegrees
if renderingImageSize[0] > renderingImageSize[1]:
  fovH = fovDegrees * aspect
else:
  fovV = fovDegrees / aspect

print "fovH : " + str(fovH)
print "fovV : " + str(fovV)
