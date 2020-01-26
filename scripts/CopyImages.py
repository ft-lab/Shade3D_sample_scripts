# -----------------------------------------------------.
# イメージを複製.
#
# @title \en Copy image \enden
# @title \ja イメージを複製 \endja
# -----------------------------------------------------.
scene = xshade.scene()

# ----------------------------------------------------------.
# 指定のマスターイメージを複製.
# @param[in] masterImage  masterImageクラス.
# ----------------------------------------------------------.
def copyImage (masterImage):
    # マスターイメージではない場合.
    if masterImage == None or masterImage.type != 10:
        return
    
    if masterImage.image == None or masterImage.image.has_image == False:
        return

    scene.begin_creating()
    newMImage = scene.create_master_image(masterImage.name)
    newMImage.image = masterImage.image.duplicate()
    scene.end_creating()

# -------------------------------------------------.
activeShapesList = []
for shape in scene.active_shapes:
    if shape.type == 10:        # マスターイメージの場合.
        activeShapesList.append(shape)

for shape in activeShapesList:
    copyImage(shape)
