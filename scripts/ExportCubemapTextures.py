# -----------------------------------------------------.
# キューブマップテクスチャを生成して出力.
# WebGL(three.js)で使用する場合は、出力されたZ面(pz,nz)は入れ替える必要があります。.
# 
# @title \en Generate and export cube map textures \enden
# @title \ja キューブマップテクスチャを生成して出力 \endja
# -----------------------------------------------------.
scene = xshade.scene()

# ------------------------------------------------------------.
# レンダリングを行う.
# 左右上下1ピクセルごとのマージンを設けてレンダリング.
# @param[in] cubeSize  キューブマップのサイズ (512, 1024 など).
# ------------------------------------------------------------.
def doRendering (cubeSize):
    # レンダリングサイズ.
    renderWidth  = (cubeSize + 2) * 3
    renderHeight = (cubeSize + 2) * 4
    scene.rendering.image_size = [renderWidth, renderHeight]

    # バーティカルクロスのパノラマ投影.
    scene.rendering.panorama_projection = 5

    # レンダリング.
    # レンダリングが完了するまで待つ.
    scene.rendering.render()

# ------------------------------------------------------------.
# 指定の名前のマスターイメージを取得.
# ------------------------------------------------------------.
def findMasterImageByName (nameStr):
    # マスターイメージパートを取得.
    shape = scene.shape
    masterImagePart = None
    if shape.has_son:
        s = shape.son
        while s.has_bro:
            s = s.bro
            if s.type == 2 and s.part_type == 102:  # マスターイメージパート.
                masterImagePart = s
                break

    if masterImagePart == None or masterImagePart.has_son == False:
        return None
    
    # マスターイメージ内で指定の名称があるか.
    targetShape = None
    s = masterImagePart.son
    while s.has_bro:
        s = s.bro
        if s.name == nameStr:
            targetShape = s
            break

    return targetShape

# ------------------------------------------------------------.
# キューブマップレンダリング結果を6つのマスターイメージとして分離.
# @param[in] outputPath         ファイルにキューブマップ画像を出力する場合のパス.
# @param[in] outputFileType     ファイル拡張子.
# ------------------------------------------------------------.
def createCubeTextures (outputPath, outputFileType):
    if scene.rendering.image == None or scene.rendering.image.has_image == False:
        return
    
    width  = scene.rendering.image.size[0]
    height = scene.rendering.image.size[1]
    orgTexWidth  = width / 3
    orgTexHeight = height / 4
    cubeTexWidth  = orgTexWidth - 2
    cubeTexHeight = orgTexHeight - 2

    cubeTexName = ['cubeTex_px','cubeTex_nx','cubeTex_py','cubeTex_ny','cubeTex_pz','cubeTex_nz']
    cubePosA = [ (orgTexWidth * 2, orgTexHeight), (0, orgTexHeight),
                 (orgTexWidth, 0), (orgTexWidth, orgTexHeight * 2),
                 (orgTexWidth, orgTexHeight * 3), (orgTexWidth, orgTexHeight) ]

    # 色補正を行うか.
    useColorCorrection = False
    if outputFileType != 'exr':
        useColorCorrection = True

    for i in range(6):
        xPos = cubePosA[i][0] + 1
        yPos = cubePosA[i][1] + 1

        # cubeTexName[i]の名前のマスターイメージが存在するか.
        masterImage = findMasterImageByName(cubeTexName[i])
        if masterImage == None:
            masterImage = scene.create_master_image(cubeTexName[i])

        masterImage.image = xshade.create_image((cubeTexWidth, cubeTexHeight), 128)

        for y in range(cubeTexHeight):
            for x in range(cubeTexWidth):
                # レンダリング画像上のピクセル色を取得.
                if i == 4:      # pzの場合は左右と上下を逆にする.
                    col = scene.rendering.image.get_pixel_rgba(cubeTexWidth + xPos - x, cubeTexHeight + yPos - y)
                else:
                    col = scene.rendering.image.get_pixel_rgba(x + xPos, y + yPos)

                # 色補正を行う.
                col2 = col
                if useColorCorrection:
                    col2 = scene.correction.correct([col[0], col[1], col[2]])

                # 色をmasterImage.imageに指定.
                masterImage.image.set_pixel_rgba(x, y, [col2[0], col2[1], col2[2], col[3]])

        # ファイル出力.
        if outputPath != '':
            fName = outputPath + '/' + cubeTexName[i] + '.' + outputFileType
            masterImage.image.save(fName)

# ----------------------------------------------------------.

# ダイアログボックスの作成.
dlg = xshade.create_dialog_with_uuid('51cbd867-c363-47f9-9741-7afa5a4e48ed')

cubeTexSize_id = dlg.append_selection('キューブマップサイズ : /256/512/1024/2048/4096', '')
outputImageFile_id = dlg.append_bool('イメージをファイル出力')
outputFilePath_id = dlg.append_path('出力フォルダ : ')
outputFileType_id = dlg.append_selection('出力イメージ形式 : /jpg/png/exr', '')

# デフォルトボタンを追加.
dlg.append_default_button()

# 値を指定.
dlg.set_value(cubeTexSize_id, 1)
dlg.set_value(outputImageFile_id, True)
dlg.set_value(outputFileType_id, 0)

# デフォルト値を指定.
dlg.set_default_value(cubeTexSize_id, 1)
dlg.set_default_value(outputImageFile_id, True)
dlg.set_default_value(outputFileType_id, 0)

# ダイアログボックスを表示.
if dlg.ask('キューブマップテクスチャを出力'):
    # ダイアログボックスでの値を取得.
    tSizeA = [256, 512, 1024, 2048, 4096]
    cubeTexSize = tSizeA[dlg.get_value(cubeTexSize_id)]

    outputImageFile = dlg.get_value(outputImageFile_id)

    fTypeA = ['jpg', 'png', 'exr']
    outputFileType = fTypeA[dlg.get_value(outputFileType_id)]

    outputPath = dlg.get_value(outputFilePath_id)
    if outputImageFile == False:
        outputPath = ''

    if outputImageFile and outputPath == '':
        print 'キューブマップテクスチャを出力するパスを指定してください。'
    else:
        # キューブマップレンダリングを行う.
        doRendering(cubeTexSize)

        # キューブマップレンダリング結果を6つのマスターイメージとして分離.
        createCubeTextures(outputPath, outputFileType)

        print 'キューブマップテクスチャを出力しました。'
        if outputPath != '':
            print 'キューブマップテクスチャを [' + outputPath + '] に出力しました。'
