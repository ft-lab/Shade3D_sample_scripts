# ----------------------------------------------------------.
# IESファイルを読み込み.
#
# 以下はresultへの出力情報。JSONのデータとして返す.
#   lampLuminousFlux       ランプ光束(lm).
#   luminousIntensityScale 光度にかける倍率.
#   angleListA             度数の配列 (垂直).
#   angleListB             度数の配列 (水平).
#   intensityList          光度の配列 (水平 * 垂直分).
# ----------------------------------------------------------.
import json

# 対応するIESのフォーマットは、IESNA91

# ファイルダイアログボックスを表示し、読み込むするフルパスを取得.
dialog = xshade.create_dialog()
filePath = dialog.ask_path(True, "IES(.ies)|ies")

result = ''
resultData = {"lampLuminousFlux" : 0.0, "luminousIntensityScale" : 1.0, "angleListA" : [], "angleListB" : [], "intensityList" : [], "errorMessage" : ""}

# IESファイルを読み込み.
def loadIES (f):
    strA = ''
    chkIESNA = False
    errF = False
    for lineStr in f:
        # 1行の空白や改行コードを取り除く.
        lineStr = lineStr.strip()
        if lineStr == '':
            continue

        # ヘッダ部の読み込み.
        if lineStr.find('IESNA') >= 0:
            chkIESNA = True
            continue

        if chkIESNA == False:
            errF = True
            break

        if lineStr.find('TILT=') >= 0:
            continue

        if lineStr.find('[TEST]') >= 0:
            continue

        if lineStr.find('[MANUFAC]') >= 0:
            continue

        if lineStr.find('[') >= 0:
            continue

        # 文字列を連結.
        if strA != '':
            strA += ' '
        strA += lineStr

    # スペースで分解.
    strList = []
    if strA != '':
        strList = strA.split()      # スペース、タブ、改行などで分割.
        if strList.count <= 13:
            errF = True

    if errF:
        resultData["errorMessage"] = '読み込みに失敗しました。'
        return

    # ランプ光束 (lm).
    resultData["lampLuminousFlux"] = float(strList[1])

    # 光度にかける倍率.
    resultData["luminousIntensityScale"] = float(strList[2])

    # 垂直角度の数.
    dCouA = int(strList[3])

    # 水平角度の数.
    dCouB = int(strList[4])

    # 要素数のチェック.
    cou = 13 + (dCouA + dCouB) + dCouA * dCouB
    if cou != len(strList):
        resultData["errorMessage"] = '読み込みに失敗しました。' + str(cou) + " <> " + str(len(strList))
        return

    # 配列に角度値を入れる.
    resultData["angleListA"] = [0.0] * dCouA
    resultData["angleListB"] = [0.0] * dCouB

    for i in range(dCouA):
        resultData["angleListA"][i] = float(strList[13 + i])

    for i in range(dCouB):
        resultData["angleListB"][i] = float(strList[13 + dCouA + i])

    # 配列に光度値を入れる.
    resultData["intensityList"] = [0.0] * (dCouA * dCouB)
    iPos = 0
    for i in range(dCouB):
        for j in range(dCouA):
            resultData["intensityList"][iPos] = float(strList[13 + dCouA + dCouB + iPos])
            iPos += 1

if filePath != '':
    # ファイルパスをPythonで理解できるようにUTF-8から変換.
    filePath = filePath.decode('utf-8')

    try:
        f = open(filePath)
        loadIES(f)
        f.close()
    except Exception as e:
        resultData["errorMessage"] = str(e)

    result = json.dumps(resultData, ensure_ascii=False)
