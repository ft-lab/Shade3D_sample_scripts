# -----------------------------------------------------.
# テクスチャイメージのRGBA要素を分解(Unpack).
#
# @title \en Unpack texture images \enden
# @title \ja テクスチャイメージのRGBA要素を分解(Unpack) \endja
# -----------------------------------------------------.
scene = xshade.scene()

# ----------------------------------------------------------.
# Unpack : 指定のテクスチャ（マスターイメージ）をRGBAに分解.
# @param[in] masterImage  masterImageクラス.
# ----------------------------------------------------------.
def unpackImageToRGBA (masterImage):
    # マスターイメージではない場合.
    if masterImage == None or masterImage.type != 10:
        return
    
    if masterImage.image == None or masterImage.image.has_image == False:
        return

    width  = masterImage.image.size[0]
    height = masterImage.image.size[1]

    scene.begin_creating()

    nameV = ['R', 'G', 'B', 'A']
    for loop in range(4):
        name = nameV[loop] + '_' + masterImage.name
        newMImage = scene.create_master_image(name)
        newMImage.image = xshade.create_image((width, height))

        for y in range(height):
            for x in range(width):
                col  = masterImage.image.get_pixel_rgba(x, y)
                fV   = col[loop]
                col2 = [fV, fV, fV, 1.0]
                newMImage.image.set_pixel_rgba(x, y, col2)

    scene.end_creating()


# -------------------------------------------------.

# 選択形状がマスターイメージの場合にUnpackする.
activeShapesList = []
for shape in scene.active_shapes:
    activeShapesList.append(shape)

for shape in activeShapesList:
    if shape.type == 10:        # マスターイメージの場合.
        unpackImageToRGBA(shape)

