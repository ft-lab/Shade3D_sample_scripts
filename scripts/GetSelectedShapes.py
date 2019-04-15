# -----------------------------------------------------.
# 選択形状を一覧する.
#   ブラウザで選択した形状名と種類、パートの場合はパートの種類を取得.
# -----------------------------------------------------.
scene = xshade.scene()

# パートの種類を取得.
def getPartType (shape):
    if shape.part_type == 0:
        return "パート"
    if shape.part_type == 1:
        return "自由曲面"
    if shape.part_type == 2:
        return "回転ジョイント"
    if shape.part_type == 3:
        return "直線移動ジョイント"
    if shape.part_type == 4:
        return "拡大縮小ジョイント"
    if shape.part_type == 5:
        return "均等拡大縮小ジョイント"
    if shape.part_type == 6:
        return "光源ジョイント"
    if shape.part_type == 7:
        return "パスジョイント"
    if shape.part_type == 8:
        return "変形ジョイント"
    if shape.part_type == 9:
        return "カスタムジョイント"
    if shape.part_type == 10:
        return "ボールジョイント"
    if shape.part_type == 11:
        return "カメラ"
    if shape.part_type == 12:
        return "サウンド"
    if shape.part_type == 13:
        return "スイッチ"
    if shape.part_type == 14:
        return "パスリプリケータ"
    if shape.part_type == 15:
        return "サーフェスリプリケータ"
    if shape.part_type == 16:
        return "ボーンジョイント"
    if shape.part_type == 100:
        return "マスターサーフェス"
    if shape.part_type == 101:
        return "リンク"
    if shape.part_type == 102:
        return "マスターイメージ"
    if shape.part_type == 103:
        return "マスターオブジェクト"
    if shape.part_type == 104:
        return "マスターオブジェクト（外部参照形状）"
    if shape.part_type == 105:
        return "ローカル座標"
    return str(shape.type)

# 形状の種類を取得.
def getType (shape):
    if shape.type == 2:
        return "パート (" + getPartType(shape) + ")"
    if shape.type == 3:
        return "光源"
    if shape.type == 4:
        return "線形状"
    if shape.type == 5:
        return "球"
    if shape.type == 6:
        return "円"
    if shape.type == 7:
        return "ポリゴンメッシュ"
    if shape.type == 8:
        return "マスターサーフェス"
    if shape.type == 10:
        return "マスターイメージ"
    return "?"


for shape in scene.active_shapes:
    print "[" + shape.name + "]" + " : 種類 " + getType(shape)



