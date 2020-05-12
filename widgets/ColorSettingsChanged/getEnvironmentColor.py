# ---------------------------------------.
# 環境設定の色を返す.
# ---------------------------------------.
# 色情報を16進数の文字列に変換.
def convColorToString (val):
    iVal = int(val[0] * 255.0)
    strR = '%02x' % iVal

    iVal = int(val[1] * 255.0)
    strG = '%02x' % iVal

    iVal = int(val[2] * 255.0)
    strB = '%02x' % iVal

    return '#' + strR + strG + strB

# ウィンドウ背景色.
backColor = [0.0, 0.0, 0.0]
v = (xshade.preference().base_brightness + 1.0) * 0.44
backColor[0] = v
backColor[1] = v
backColor[2] = v

# テキスト色.
textColor = [0.0, 0.0, 0.0]
if xshade.preference().base_brightness <= 0.2:
    textColor = [1.0, 1.0, 1.0]

# ウィンドウ背景色.
backColorStr = convColorToString(backColor)

# ウィンドウテキスト色.
textColorStr = convColorToString(textColor)

# 結果をJSON文字列で返す.
result = '{"background" : "' + backColorStr + '", "text" : "' + textColorStr + '"}'

