# -----------------------------------------------------.
# ダイアログボックスを表示.
#
# @title \en Show dialog box \enden
# @title \ja ダイアログボックスを表示 \endja
# -----------------------------------------------------.
import random

scene = xshade.scene()

# -----------------------------------------.
# 球を生成する.
# @param[in] num     生成する球の数.
# @param[in] radius  球の半径.
# @param[in] col     球の色.
# @param[in] isRnd   球の半径をランダムに変化させる場合はTrue.
# -----------------------------------------.
def doCreateSpheres (num, radius, col, isRnd):
  if num <= 0 or radius <= 0.0:
    return

  # 形状の作成開始.
  scene.begin_creating()
  scene.begin_part('spheres')

  # マスターサーフェスを作成.
  masterSurface = scene.create_master_surface('sphere')
  masterSurface.surface.diffuse_color = col

  # 球をランダム位置に生成.
  rangeV  = radius * 10.0
  rangeVH = rangeV * 0.5
  for i in range(num):
      # ランダムな位置
      px = random.random() * rangeV - rangeVH
      py = random.random() * rangeV - rangeVH
      pz = random.random() * rangeV - rangeVH
      pos = [px, py, pz]

      # 半径.
      r2 = radius
      if isRnd:
        r2 = (radius * 0.5) * random.random() + (radius * 0.5)

      # 球を生成.
      sphere = scene.create_sphere(None, pos, r2)

      # マスターサーフェスを割り当て.
      sphere.master_surface = masterSurface

  scene.end_part()

  # 形状の作成終了.
  scene.end_creating()

# -----------------------------------------.

# ダイアログボックスの作成.
dlg = xshade.create_dialog_with_uuid('eca9e3de-1cb3-4cd1-b1d2-dba1eb2c35f5')

num_id = dlg.append_int('個数', '個')
radius_id = dlg.append_float('半径', 'mm')
color_id = dlg.append_rgb('色')
random_id = dlg.append_bool('ランダム')

# デフォルトボタンを追加.
dlg.append_default_button()

# 値を指定.
dlg.set_value(num_id, 10)
dlg.set_value(radius_id, 100.0)
dlg.set_value(color_id, [1.0, 1.0, 1.0])
dlg.set_value(random_id, False)

# デフォルト値を指定.
dlg.set_default_value(num_id, 10)
dlg.set_default_value(radius_id, 100.0)
dlg.set_default_value(color_id, [1.0, 1.0, 1.0])
dlg.set_default_value(random_id, False)

# ダイアログボックスを表示.
if dlg.ask("球を生成"):
  # ダイアログボックスでの値を取得.
  num = dlg.get_value(num_id)
  radius = dlg.get_value(radius_id)
  col = dlg.get_value(color_id)
  isRnd = dlg.get_value(random_id)

  # 球を生成.
  doCreateSpheres(num, radius, col, isRnd)
