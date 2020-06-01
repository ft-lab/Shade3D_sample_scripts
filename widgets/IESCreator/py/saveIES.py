# ----------------------------------------------------------.
# IESファイル保存.
#
# 以下は入力情報.
#   intensityList            光度の配列(90 + 1要素分).
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
    f.write('IESNA91\n')
    f.write('TILT=NONE\n')

    # 出力データの情報 (以下は読み込みに失敗するのでコメントアウト).
    #fileInfo = ''
    #f.write('[TEST] ' + fileInfo + '\n')

    # 照明器具のメーカー (以下は読み込みに失敗するのでコメントアウト).
    #manufactureName = ''
    #f.write('[MANUFAC] ' + manufactureName + '\n')

    # 固定値.
    paramStr = '1 '

    # ランプ光束 (lm).
    paramStr += str(lampLuminousFlux) + ' '

    # 光度(cd)値の倍率.
    paramStr += str(luminousIntensityScale) + ' '

    # 垂直角度の数.
    paramStr += '91 '

    # 水平角度の数.
    paramStr += '1 '

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
    for i in range(91):
        if strV != '':
            strV += ' '
        strV += str(i)
    f.write(strV + '\n')

    # 水平角度の配列.
    f.write('0\n')

    # 光度(cd)のリスト.
    strV = ''
    for i in range(91):
        if strV != '':
            strV += ' '
        strV += str(intensityList[i])
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
