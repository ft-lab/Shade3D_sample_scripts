# -----------------------------------------------------.
# マスターイメージとしてRGBA要素を指定し、合成(Pack).
# 選択されたマスターイメージが「R_xxxx」「G_xxxx」「B_xxxx」「A_xxxx」である場合、.
# Packし「xxxx」のイメージを作成.
#
# @title \en Pack texture image \enden
# @title \ja マスターイメージとしてRGBA要素を指定し、合成(Pack) \endja
# -----------------------------------------------------.
scene = xshade.scene()

# ----------------------------------------------------------.
# Pack : 指定のテクスチャ（マスターイメージ）をRGBAとして、1枚に結合.
# @param[in] imagesList  masterImageの配列(4要素分).
# ----------------------------------------------------------.
def packRGBAToImage (imagesList):
    if len(imagesList) != 4:
        return
    
    # 格納されている画像より、イメージサイズを最大のものを採用.
    name = ''
    width = 0
    height = 0
    for i in range(4):
        mImage = imagesList[i]
        if mImage == None:
            continue
        if mImage.image != None and mImage.image.has_image:
            pos = mImage.name.find('_')
            if pos >= 0:
                width = max(width, mImage.image.size[0])
                height = max(height, mImage.image.size[1])
                name = mImage.name[pos + 1:]

    if width == 0 or height == 0 or name == '':
        return
    
    # イメージを作成.
    scene.begin_creating()
    newMImage = scene.create_master_image(name)
    newMImage.image = xshade.create_image((width, height))
    scene.end_creating()

    imageBuff = [0.0, 0.0, 0.0, 0.0] * (width * height)

    # RGBAを格納.
    for i in range(4):
        mImage = imagesList[i]
        if mImage == None:
            continue
        if mImage.image != None and mImage.image.has_image:
            img = mImage.image.duplicate((width, height))

            iPos = 0
            for y in range(height):
                for x in range(width):
                    sCol = img.get_pixel_rgba(x, y)
                    imageBuff[iPos + i]= sCol[0]
                    iPos += 4

    # RGBAを格納.
    iPos = 0
    for y in range(height):
        for x in range(width):
            col = [imageBuff[iPos], imageBuff[iPos + 1], imageBuff[iPos + 2], imageBuff[iPos + 3]]
            newMImage.image.set_pixel_rgba(x, y, col)
            iPos += 4

# ----------------------------------------------------------.
# リストに指定の値valが存在するか.
# @param[in] listA  対象のリスト.
# @param[in] val    検索する値.
# @return 値が存在するインデックス.
# ----------------------------------------------------------.
def searchList (listA, val):
    indexV = -1
    for i in range(len(listA)):
        if listA[i] == val:
            indexV = i
            break
    return indexV

# ----------------------------------------------------------.
# 配列内のマスターイメージより、
# "R_xxx" "G_xxx" "B_xxx" "A_xxx"の組み合わせを格納.
# @param[in] masterImagesList  マスターイメージ配列.
# @return [][4]としてRGBAごとに整列した二次元配列を返す.
# ----------------------------------------------------------.
def checkImages (masterImagesList):
    cou = len(masterImagesList)
    if cou == 0:
        return []
    
    rgbaStr1 = ['r', 'g', 'b', 'a']
    rgbaStr2 = ['red', 'green', 'blue', 'alpha']

    # nameList[]に有効なマスターイメージ名を入れる.
    nameList = []
    for mImage in masterImagesList:
        name = mImage.name.lower()
        pos = name.find('_')
        if pos < 0:
            continue
        s = name[0:pos]
        if searchList(rgbaStr1, s) >= 0 or searchList(rgbaStr2, s) >= 0:
            name2 = mImage.name[pos + 1:]
            if searchList(nameList, name2) < 0:
                nameList.append(name2)

    # resList[][4]に、RGBAごとに整列.
    resList = []
    for i in range(len(nameList)):
        resList.append([None, None, None, None])

    for mImage in masterImagesList:
        name = mImage.name.lower()
        pos = name.find('_')
        if pos < 0:
            continue
        s = name[0:pos]
        name2 = mImage.name[pos + 1:]
        nIndex = searchList(nameList, name2)
        if nIndex < 0:
            continue

        p1 = searchList(rgbaStr1, s)
        p2 = searchList(rgbaStr2, s)
        if p1 >= 0 or p2 >= 0:
            p = max(p1, p2)
            resList[nIndex][p] = mImage

    return resList

# -------------------------------------------------.

activeShapesList = []
for shape in scene.active_shapes:
    if shape.type == 10:        # マスターイメージの場合.
        activeShapesList.append(shape)

if len(activeShapesList) == 0:
    print '"R_xxx" "G_xxx" "B_xxx" "A_xxx" の名前のマスターイメージを複数選択してください。'
else :
    # マスターイメージ名より、[][4]のRGBAごとの配列に分類.
    resList = checkImages(activeShapesList)

    # RGBAのマスターイメージより、1枚のイメージに合成.
    for imagesList in resList:
        packRGBAToImage(imagesList)
