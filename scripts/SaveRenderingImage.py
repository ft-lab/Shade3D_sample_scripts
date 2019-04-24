# -----------------------------------------------------.
# レンダリング画像をファイル保存.
#
# @title \en Save rendered image as file \enden
# @title \ja レンダリング画像をファイル保存 \endja
# -----------------------------------------------------.
scene = xshade.scene()

# レンダリング画像サイズを取得.
imageSize = scene.rendering.image_size
print "image size : " + str(imageSize[0]) + " x " + str(imageSize[1])

# レンダリング画像が存在する場合はファイルに保存.
if scene.rendering.image != None:
  dialog = xshade.create_dialog_with_uuid()
  file_path = dialog.ask_path(False, 'Jpeg|jpg;jpeg|png|png|OpenEXR|exr')
  if file_path != '':
    scene.rendering.image.save(file_path)

