# ----------------------------------------------------------.
# IESファイル保存.
# IESファイルは、垂直面（断面）ごとの光度配列があり、これが水平の分割ごとに存在.
# 光度配列の要素としては、len(angleListA) * len(angleListB) の個数分存在することになる.

# 以下は入力情報.
#   angleListA               角度の配列 (垂直の断面部).
#   angleListB               角度の配列 (水平).
#   intensityList            光度の配列 (len(angleListA) * len(angleListB)分).
#   luminousIntensityScale   光度にかける倍率.
#   lampLuminousFlux         ランプ光束(lm).
# ----------------------------------------------------------.

# ファイルダイアログボックスを表示し、保存するフルパスを取得.
dialog = xshade.create_dialog()
filePath = dialog.ask_path(False, "IES(.ies)|ies")

result = ''

# IESNA91の参考.
#  http://entercad.ru/acad_aug.en/ws73099cc142f48755f058a10f71c104f3-3b1a.htm

# IESファイルに出力.
def writeIES (f):
    # ヘッダ.
    f.write('IESNA\n')

    # 出力データの情報.
    fileInfo = 'IES Creator for Shade3D'
    f.write('[TEST] ' + fileInfo + '\n')

    # 照明器具のメーカー.
    manufactureName = 'Shade3D'
    f.write('[MANUFAC] ' + manufactureName + '\n')

    # 固定値.
    f.write('TILT=NONE\n')

    # 角度の要素数.
    angleACou = len(angleListA)
    angleBCou = len(angleListB)

    # 固定値.
    paramStr = '1 '

    # ランプ光束 (lm).
    paramStr += str(lampLuminousFlux) + ' '

    # 光度(cd)値の倍率.
    paramStr += str(luminousIntensityScale) + ' '

    # 垂直角度の数.
    paramStr += str(angleACou) + ' '

    # 水平角度の数.
    paramStr += str(angleBCou) + ' '

    # 固定値.
    paramStr += '1 '

    # 単位の種類。1 : フィート、2 : メートル.
    paramStr += '2 '

    f.write(paramStr + '\n')

    # 発光する開口部の幅、長さ、高さ。通常は 0 0 0 を指定.
    f.write('0 0 0\n')

    # 固定値.
    f.write('1 1 0\n')

    # 垂直角度の配列.
    strV = ''
    for i in range(angleACou):
        if strV != '':
            strV += ' '
        strV += str(angleListA[i])
    f.write(strV + '\n')

    # 水平角度の配列。0.0のみの場合は軸対称になる.
    strV = ''
    for i in range(angleBCou):
        if strV != '':
            strV += ' '
        strV += str(angleListB[i])
    f.write(strV + '\n')

    # 光度(cd)のリスト.
    iPos = 0
    for i in range(angleBCou):
        strV = ''
        for j in range(angleACou):
            if strV != '':
                strV += ' '
            strV += str(intensityList[iPos])
            iPos += 1
        f.write(strV + '\n')

if filePath != '':
    # ファイルパスをPythonで理解できるようにUTF-8から変換.
    filePath = filePath.decode('utf-8')

    try:
        f = open(filePath, mode='w')
        writeIES(f)
        f.close()

    except Exception as e:
        result = 'error : ' + str(e)
