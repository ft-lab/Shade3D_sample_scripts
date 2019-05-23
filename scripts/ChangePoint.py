# -----------------------------------------------------.
# 選択ポイントの座標値を変更.
#
# @title \en Change coordinate value of selected point \enden
# @title \ja 選択ポイントの座標値を変更 \endja
# -----------------------------------------------------.
scene = xshade.scene()

# -------------------------------------------------------.
# 指定形状の、アクティブなポイントの座標位置を返す.
# 複数の選択がある場合は、はじめのポイントの座標を返す.
# @param[in] shape  対象形状.
# @return ポイントの座標値 [x, y, z].
# -------------------------------------------------------.
def getActivePoint (shape):
  retPos = None
  active_vers = shape.active_vertex_indices
  if active_vers != None and len(active_vers) > 0:
    for index in (active_vers):
      if shape.type == 7:   # ポリゴンメッシュの場合.
        retPos = shape.vertex(index).position
      else:
        retPos = shape.control_point(index).position

  return retPos

# -------------------------------------------------------.
# 指定の形状の、アクティブなポイントを指定の座標で置き換え.
# @param[in] shape  対象形状.
# @param[in] pos    ポイントの座標値 [x, y, z].
# -------------------------------------------------------.
def changeActivePoint (shape, pos):
  #scene.begin_creating()

  active_vers = shape.active_vertex_indices
  if active_vers != None and len(active_vers) > 0:
    for index in (active_vers):
      if shape.type == 7:   # ポリゴンメッシュの場合.
        shape.vertex(index).position = pos
      else:
        shape.control_point(index).position = pos
  
  # スキンに関する情報を更新.
  shape.update_skin_bindings()

  # 形状情報を更新.
  shape.update()

  #scene.end_creating()

# -------------------------------------------------------.

# 選択形状の選択状態なポイント位置を取得し、値を変更するインターフェースを出す.
shape = scene.active_shape()

if scene.is_modify_mode:   # 形状編集モードの場合.
  # 選択形状で、選択状態のポイントの座標を取得.
  aPos = getActivePoint(shape)

  if aPos != None:
    #　ダイアログボックスを作成.
    dlg = xshade.create_dialog()
    point_id = dlg.append_vec3('ポイントの座標値')
    dlg.set_value(point_id, aPos)

    # ダイアログボックスを表示.
    if dlg.ask("ポイント座標を変更"):
      pos2 = dlg.get_value(point_id)

      # 選択ポイントの座標値を変更.
      changeActivePoint(shape, pos2)
  else:
    print "ポイントが選択されていません。"

else:
  print "形状編集モード + 頂点選択モードで使用してください。"
    
