# -----------------------------------------------------.
# 単一色のテクスチャを生成.
# 
# @title \en Generate single color texture \enden
# @title \ja 単一色のテクスチャを生成 \endja
# -----------------------------------------------------.
scene = xshade.scene()

# ------------------------------------------------------------.
# 単一色のテクスチャを生成.
# @param[in] (redV, greenV, blueV)   RGB値.
# ------------------------------------------------------------.
def generateSingleColorTexture(redV, greenV, blueV):
    texSize = 8

    scene.begin_creating()
    masterImage = scene.create_master_image('colorTexture')
    masterImage.image = xshade.create_image((texSize, texSize))
    scene.end_creating()

    col = [redV, greenV, blueV]
    for y in range(texSize):
        for x in range(texSize):
            masterImage.image.set_pixel(x, y, col)

# ------------------------------------------------------------.

# ダイアログボックスの作成.
dlg = xshade.create_dialog_with_uuid('1cea0e98-c704-461f-bde5-c0b205a098a6')

color_id = dlg.append_rgb('色 : ')

# デフォルトボタンを追加.
dlg.append_default_button()

# 値を指定.
dlg.set_value(color_id, [1, 1, 1])

# デフォルト値を指定.
dlg.set_default_value(color_id, [1, 1, 1])

# ダイアログボックスを表示.
if dlg.ask('単一色テクスチャを生成'):
    # ダイアログボックスでの値を取得.
    col = dlg.get_value(color_id)

    # 単一色テクスチャを生成.
    generateSingleColorTexture(col[0], col[1], col[2])

