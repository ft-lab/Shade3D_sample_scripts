# -----------------------------------------------------.
# 線形状のコントロールポイント情報を表示
#
# @title \en Display control points information of line shape \enden
# @title \ja 線形状のコントロールポイント情報を表示 \endja
# -----------------------------------------------------.
scene = xshade.scene()

# 指定の形状が線形状の場合、コントロールポイント情報を出力.
def showLineData (shape):
    if shape.type != 4:
        print '線形状を選択してください。'
        return
    
    totalCou = shape.total_number_of_control_points
    for i in range(totalCou):
        cp = shape.control_point(i)

        # 位置を取得.
        pStr  = '{:.2f}'.format(cp.position[0]) + ', '
        pStr += '{:.2f}'.format(cp.position[1]) + ', '
        pStr += '{:.2f}'.format(cp.position[2])
        print 'position (' + str(i) + ') : (' + pStr + ')'

        # in_handleを取得.
        pStr  = '{:.2f}'.format(cp.in_handle[0]) + ', '
        pStr += '{:.2f}'.format(cp.in_handle[1]) + ', '
        pStr += '{:.2f}'.format(cp.in_handle[2])
        print 'in_handle (' + str(i) + ') : (' + pStr + ')'

        # out_handleを取得.
        pStr  = '{:.2f}'.format(cp.out_handle[0]) + ', '
        pStr += '{:.2f}'.format(cp.out_handle[1]) + ', '
        pStr += '{:.2f}'.format(cp.out_handle[2])
        print 'out_handle (' + str(i) + ') : (' + pStr + ')'

# アクティブ形状のコントロールポイント情報を表示.
shape = scene.active_shape()
showLineData(shape)

