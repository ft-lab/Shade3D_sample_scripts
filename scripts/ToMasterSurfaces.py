# -----------------------------------------------------.
# 独立した表面材質をマスターサーフェスに整理.
# 同一と思われる表面材質は1つのマスターサーフェスにまとめる.
# 表面材質の「基本設定」「効果設定」と「マッピング」のみチェック.
# 「ボリューム設定」の移行は未対応.
#
# @title \en Make an independent surface the master surface \enden
# @title \ja 独立した表面材質をマスターサーフェス化 \endja
# -----------------------------------------------------.

scene = xshade.scene()

# --------------------------------------------------.
# float型のゼロチェック.
# --------------------------------------------------.
def isZero (v1, v2):
  vv = v1 - v2
  fMin = 0.001
  if vv > -fMin and vv < fMin:
    return True
  return False

# --------------------------------------------------.
# 色(RGB)のゼロチェック.
# --------------------------------------------------.
def isZeroColor (col1, col2):
  fMin = 0.001
  vv1 = col1[0] - col2[0]
  vv2 = col1[1] - col2[1]
  vv3 = col1[2] - col2[2]

  if vv1 > -fMin and vv1 < fMin and vv2 > -fMin and vv2 < fMin and vv3 > -fMin and vv3 < fMin:
    return True
  return False

# --------------------------------------------------.
# matrix(4x4)のゼロチェック.
# --------------------------------------------------.
def isZeroMatrix (matrix1, matrix2):
  retV = True
  for i in range(4):
    for j in range(4):
      if isZero(matrix1[i][j], matrix2[i][j]) == False:
        retV = False
        break
      if retV == False:
        break

  return retV

# --------------------------------------------------.
# 同一の表面材質かチェック.
# --------------------------------------------------.
def isSameSurface (surface1, surface2):
  # その他の設定.
  if surface1.has_aux != surface2.has_aux:
    return False
  if surface1.black_key_mask != surface2.black_key_mask:
    return False
  if isZero(surface1.direct_illumination, surface2.direct_illumination) == False:
    return False
  if isZero(surface1.indirect_illumination, surface2.indirect_illumination) == False:
    return False
  if surface1.dont_reflect_background != surface2.dont_reflect_background:
    return False
  if surface1.dont_visible_to_camera != surface2.dont_visible_to_camera:
    return False
  if surface1.dont_visible_to_indirect_rays != surface2.dont_visible_to_indirect_rays:
    return False
  if surface1.dont_visible_to_reflection_rays != surface2.dont_visible_to_reflection_rays:
    return False
  if surface1.dont_visible_to_refraction_rays != surface2.dont_visible_to_refraction_rays:
    return False
  if surface1.do_not_cast_shadow != surface2.do_not_cast_shadow:
    return False
  if surface1.do_not_reflect_objects != surface2.do_not_reflect_objects:
    return False
  if surface1.do_not_show_shadow != surface2.do_not_show_shadow:
    return False
  if surface1.white_key_mask != surface2.white_key_mask:
    return False
  if surface1.no_shading != surface2.no_shading:
    return False
  if surface1.smoother_shading != surface2.smoother_shading:
    return False
  if surface1.local_coordinates != surface2.local_coordinates:
    return False

  # 基本設定、効果設定.
  if surface1.has_aberration != surface2.has_aberration:
    return False

  if surface1.has_aberration:
    if isZero(surface1.aberration, surface2.aberration) == False:
      return False

  if surface1.has_ambient != surface2.has_ambient:
    return False
  
  if surface1.has_ambient:
    if isZero(surface1.ambient, surface2.ambient) == False:
      return False
    if isZeroColor(surface1.ambient_color, surface2.ambient_color) == False:
      return False

  if surface1.has_anisotropic != surface2.has_anisotropic:
    return False
  
  if surface1.has_anisotropic:
    if isZero(surface1.anisotropic, surface2.anisotropic) == False:
      return False

  if surface1.has_backlight != surface2.has_backlight:
    return False
  
  if surface1.has_backlight:
    if isZero(surface1.backlight, surface2.backlight) == False:
      return False
    if isZeroColor(surface1.backlight_color, surface2.backlight_color) == False:
      return False
  
  if surface1.has_diffuse != surface2.has_diffuse:
    return False
  
  if surface1.has_diffuse:   
    if isZero(surface1.diffuse, surface2.diffuse) == False:
      return False
    if isZeroColor(surface1.diffuse_color, surface2.diffuse_color) == False:
      return False
    
  if surface1.has_fresnel_reflection != surface2.has_fresnel_reflection:
    return False
  
  if surface1.has_fresnel_reflection:   
    if isZero(surface1.fresnel_reflection, surface2.fresnel_reflection) == False:
      return False

  if surface1.has_glow != surface2.has_glow:
    return False

  if surface1.has_glow:
    if isZero(surface1.glow, surface2.glow) == False:
      return False
    if isZeroColor(surface1.glow_color, surface2.glow_color) == False:
      return False
    if isZero(surface1.soft_glow, surface2.soft_glow) == False:
      return False
  
  if surface1.has_metallic != surface2.has_metallic:
    return False
  
  if surface1.has_metallic:
    if isZero(surface1.metallic, surface2.metallic) == False:
      return False
    if isZeroColor(surface1.metallic_color, surface2.metallic_color) == False:
      return False

  if surface1.has_reflection != surface2.has_reflection:
    return False

  if surface1.has_reflection:
    if isZero(surface1.reflection, surface2.reflection) == False:
      return False
    if isZeroColor(surface1.reflection_color, surface2.reflection_color) == False:
      return False

  if surface1.has_refraction != surface2.has_refraction:
    return False

  if surface1.has_refraction:
    if isZero(surface1.refraction, surface2.refraction) == False:
      return False

  if surface1.has_roughness != surface2.has_roughness:
    return False

  if surface1.has_roughness:
    if isZero(surface1.roughness, surface2.roughness) == False:
      return False

  if surface1.has_specular_1 != surface2.has_specular_1:
    return False

  if surface1.has_specular_1:
    if isZero(surface1.highlight, surface2.highlight) == False:
      return False
    if isZeroColor(surface1.highlight_color, surface2.highlight_color) == False:
      return False
    if isZero(surface1.highlight_size, surface2.highlight_size) == False:
      return False

  if surface1.has_specular_2 != surface2.has_specular_2:
    return False

  if surface1.has_specular_2:
    if isZero(surface1.highlight_2, surface2.highlight_2) == False:
      return False
    if isZeroColor(surface1.highlight_color_2, surface2.highlight_color_2) == False:
      return False
    if isZero(surface1.highlight_size_2, surface2.highlight_size_2) == False:
      return False

  if surface1.has_transparency != surface2.has_transparency:
    return False

  if surface1.has_transparency:
    if isZero(surface1.transparency, surface2.transparency) == False:
      return False
    if isZeroColor(surface1.transparency_color, surface2.transparency_color) == False:
      return False

  if surface1.has_pseudo_caustics != surface2.has_pseudo_caustics:
    return False

  if surface1.has_pseudo_caustics:
    if isZero(surface1.pseudo_caustics, surface2.pseudo_caustics) == False:
      return False
    if isZero(surface1.pseudo_caustics_aberration, surface2.pseudo_caustics_aberration) == False:
      return False
    if isZero(surface1.pseudo_caustics_brightness, surface2.pseudo_caustics_brightness) == False:
      return False
    if isZero(surface1.pseudo_caustics_bump, surface2.pseudo_caustics_bump) == False:
      return False

  # マッピング設定.
  if surface1.number_of_mapping_layers != surface2.number_of_mapping_layers:
    return False

  mapingLayerCou = surface1.number_of_mapping_layers
  if mapingLayerCou == 0:
    return True

  if surface1.has_mapping_layers == False and surface2.has_mapping_layers == False:
    return True

  # mapping layer.
  for i in range(mapingLayerCou):
    mLayer1 = surface1.mapping_layer(i)
    mLayer2 = surface2.mapping_layer(i)

    if mLayer1.pattern == 0 and mLayer2.pattern == 0:
      continue

    # イメージのマッピングの場合.
    if mLayer1.pattern == 14 and mLayer2.pattern == 14:
      if mLayer1.image == None and mLayer2.image == None:
        continue
      if mLayer1.image != None and mLayer2.image != None:
        if mLayer1.image.has_image == False or mLayer2.image.has_image == False:
          continue

    if isZero(mLayer1.actual_size[0], mLayer2.actual_size[0]) == False:
      return False
    if isZero(mLayer1.actual_size[1], mLayer2.actual_size[1]) == False:
      return False
    if mLayer1.actual_size_mode != mLayer2.actual_size_mode:
      return False

    if isZero(mLayer1.area[0], mLayer2.area[0]) == False:
      return False
    if isZero(mLayer1.area[1], mLayer2.area[1]) == False:
      return False
    if isZero(mLayer1.area[2], mLayer2.area[2]) == False:
      return False
    if isZero(mLayer1.area[3], mLayer2.area[3]) == False:
      return False

    if mLayer1.blend_mode != mLayer2.blend_mode:
      return False
    if mLayer1.blur != mLayer2.blur:
      return False
    if isZero(mLayer1.bump_height, mLayer2.bump_height) == False:
      return False
    if mLayer1.channel_mix != mLayer2.channel_mix:
      return False
    if mLayer1.flip_color != mLayer2.flip_color:
      return False
    if mLayer1.horizontal_flip != mLayer2.horizontal_flip:
      return False
    if isZeroColor(mLayer1.mapping_color, mLayer2.mapping_color) == False:
      return False
    if isZero(mLayer1.mapping_size, mLayer2.mapping_size) == False:
      return False

    if mLayer1.image != None and mLayer2.image != None:
      if mLayer1.image.has_image != mLayer2.image.has_image:
        return False

      # イメージが同一であるかチェック.
      if mLayer1.image.has_image == True and mLayer2.image.has_image == True:
        if mLayer1.image.equal(mLayer2.image) == False:
          return False

    if isZeroColor(mLayer1.origin, mLayer2.origin) == False:
      return False
    if mLayer1.parameter_mapping != mLayer2.parameter_mapping:
      return False
    if mLayer1.pattern != mLayer2.pattern:
      return False
    if mLayer1.pattern_name != mLayer2.pattern_name:
      return False
    if isZero(mLayer1.phase, mLayer2.phase) == False:
      return False
    if mLayer1.projection != mLayer2.projection:
      return False
    if mLayer1.repeat_image != mLayer2.repeat_image:
      return False
    if mLayer1.repetition_x != mLayer2.repetition_x:
      return False
    if mLayer1.repetition_y != mLayer2.repetition_y:
      return False
    if isZero(mLayer1.softness, mLayer2.softness) == False:
      return False
    if mLayer1.swap_axes != mLayer2.swap_axes:
      return False
    if isZero(mLayer1.turbulence, mLayer2.turbulence) == False:
      return False
    if mLayer1.type != mLayer2.type:
      return False
    if mLayer1.uv_mapping != mLayer2.uv_mapping:
      return False
    if mLayer1.vertical_flip != mLayer2.vertical_flip:
      return False
    if mLayer1.vertex_color_layer != mLayer2.vertex_color_layer:
      return False
    if isZero(mLayer1.weight, mLayer2.weight) == False:
      return False
    if isZeroMatrix(mLayer1.transformation, mLayer2.transformation) == False:
      return False

  return True

# -------------------------------------------------------.
# 指定の形状の独立した表面材質をマスターサーフェスにする.
# -------------------------------------------------------.
def convSurfaceToMasterSurface (shape, index):
  if shape.surface == None or shape.master_surface != None:
    return

  # マスターサーフェスを新しく作成.
  masterSurface = scene.create_master_surface("material_" + str(index))

  # masterSurfaceに、shape.surfaceの情報を複製.

  # その他の複製.
  masterSurface.surface.has_aux = shape.surface.has_aux
  masterSurface.surface.black_key_mask = shape.surface.black_key_mask
  masterSurface.surface.direct_illumination = shape.surface.direct_illumination
  masterSurface.surface.indirect_illumination = shape.surface.indirect_illumination
  masterSurface.surface.dont_reflect_background = shape.surface.dont_reflect_background
  masterSurface.surface.dont_visible_to_camera = shape.surface.dont_visible_to_camera
  masterSurface.surface.dont_visible_to_indirect_rays = shape.surface.dont_visible_to_indirect_rays
  masterSurface.surface.dont_visible_to_reflection_rays = shape.surface.dont_visible_to_reflection_rays
  masterSurface.surface.dont_visible_to_refraction_rays = shape.surface.dont_visible_to_refraction_rays
  masterSurface.surface.do_not_cast_shadow = shape.surface.do_not_cast_shadow
  masterSurface.surface.do_not_reflect_objects = shape.surface.do_not_reflect_objects
  masterSurface.surface.do_not_show_shadow = shape.surface.do_not_show_shadow
  masterSurface.surface.white_key_mask = shape.surface.white_key_mask
  masterSurface.surface.local_coordinates = shape.surface.local_coordinates
  masterSurface.surface.no_shading = shape.surface.no_shading
  masterSurface.surface.smoother_shading = shape.surface.smoother_shading

  # 基本設定/効果設定の複製.
  masterSurface.surface.has_aberration = shape.surface.has_aberration
  if masterSurface.surface.has_aberration:
    masterSurface.surface.aberration = shape.surface.aberration

  masterSurface.surface.has_ambient = shape.surface.has_ambient
  if masterSurface.surface.has_ambient:
    masterSurface.surface.ambient = shape.surface.ambient
    masterSurface.surface.ambient_color = shape.surface.ambient_color

  masterSurface.surface.has_anisotropic = shape.surface.has_anisotropic
  if masterSurface.surface.has_anisotropic:
    masterSurface.surface.anisotropic = shape.surface.anisotropic

  masterSurface.surface.has_backlight = shape.surface.has_backlight
  if masterSurface.surface.has_backlight:
    masterSurface.surface.backlight = shape.surface.backlight
    masterSurface.surface.backlight_color = shape.surface.backlight_color

  masterSurface.surface.has_diffuse = shape.surface.has_diffuse
  if masterSurface.surface.has_diffuse:
    masterSurface.surface.diffuse = shape.surface.diffuse
    masterSurface.surface.diffuse_color = shape.surface.diffuse_color

  masterSurface.surface.has_fresnel_reflection = shape.surface.has_fresnel_reflection
  if masterSurface.surface.has_fresnel_reflection:
    masterSurface.surface.fresnel_reflection = shape.surface.fresnel_reflection

  masterSurface.surface.has_glow = shape.surface.has_glow
  if masterSurface.surface.has_glow:
    masterSurface.surface.glow = shape.surface.glow
    masterSurface.surface.glow_color = shape.surface.glow_color
    masterSurface.surface.soft_glow = shape.surface.soft_glow

  masterSurface.surface.has_metallic = shape.surface.has_metallic
  if masterSurface.surface.has_metallic:
    masterSurface.surface.metallic = shape.surface.metallic
    masterSurface.surface.metallic_color = shape.surface.metallic_color

  masterSurface.surface.has_pseudo_caustics = shape.surface.has_pseudo_caustics
  if masterSurface.surface.has_pseudo_caustics:
    masterSurface.surface.pseudo_caustics = shape.surface.pseudo_caustics
    masterSurface.surface.pseudo_caustics_aberration = shape.surface.pseudo_caustics_aberration
    masterSurface.surface.pseudo_caustics_brightness = shape.surface.pseudo_caustics_brightness
    masterSurface.surface.pseudo_caustics_bump = shape.surface.pseudo_caustics_bump
  
  masterSurface.surface.has_reflection = shape.surface.has_reflection
  if masterSurface.surface.has_reflection:
    masterSurface.surface.reflection = shape.surface.reflection
    masterSurface.surface.reflection_color = shape.surface.reflection_color
  
  masterSurface.surface.has_refraction = shape.surface.has_refraction
  if masterSurface.surface.has_refraction:
    masterSurface.surface.refraction = shape.surface.refraction

  masterSurface.surface.has_roughness = shape.surface.has_roughness
  if masterSurface.surface.has_roughness:
    masterSurface.surface.roughness = shape.surface.roughness
  
  masterSurface.surface.has_specular_1 = shape.surface.has_specular_1
  if masterSurface.surface.has_specular_1:
    masterSurface.surface.highlight = shape.surface.highlight
    masterSurface.surface.highlight_color = shape.surface.highlight_color
    masterSurface.surface.highlight_size = shape.surface.highlight_size
  
  masterSurface.surface.has_specular_2 = shape.surface.has_specular_2
  if masterSurface.surface.has_specular_2:
    masterSurface.surface.highlight_2 = shape.surface.highlight_2
    masterSurface.surface.highlight_color_2 = shape.surface.highlight_color_2
    masterSurface.surface.highlight_size_2 = shape.surface.highlight_size_2
  
  masterSurface.surface.has_transparency = shape.surface.has_transparency
  if masterSurface.surface.has_transparency:
    masterSurface.surface.transparency = shape.surface.transparency
    masterSurface.surface.transparency_color = shape.surface.transparency_color

  # マッピングの複製.
  masterSurface.surface.has_mapping_layers = shape.surface.has_mapping_layers

  mappingLayerCou = shape.surface.number_of_mapping_layers
  if mappingLayerCou == 0 or masterSurface.surface.has_mapping_layers == False:
    shape.master_surface = masterSurface
    return

  # マッピングレイヤ情報を複製.
  for i in range(mappingLayerCou):
    srcMappingLayer = shape.surface.mapping_layer(i)

    # マッピングレイヤを追加.
    masterSurface.surface.append_mapping_layer()
    dstMappingLayer = masterSurface.surface.mapping_layer(i)

    # マッピングレイヤのパラメータをコピー.
    dstMappingLayer.actual_size = srcMappingLayer.actual_size
    dstMappingLayer.actual_size_mode = srcMappingLayer.actual_size_mode
    dstMappingLayer.area = srcMappingLayer.area
    dstMappingLayer.blend_mode = srcMappingLayer.blend_mode
    dstMappingLayer.blur = srcMappingLayer.blur
    dstMappingLayer.bump_height = srcMappingLayer.bump_height
    dstMappingLayer.channel_mix = srcMappingLayer.channel_mix
    dstMappingLayer.flip_color = srcMappingLayer.flip_color
    dstMappingLayer.horizontal_flip = srcMappingLayer.horizontal_flip
    dstMappingLayer.mapping_color = srcMappingLayer.mapping_color
    dstMappingLayer.mapping_size = srcMappingLayer.mapping_size

    dstMappingLayer.origin = srcMappingLayer.origin
    dstMappingLayer.parameter_mapping = srcMappingLayer.parameter_mapping
    dstMappingLayer.pattern = srcMappingLayer.pattern
    dstMappingLayer.phase = srcMappingLayer.phase
    dstMappingLayer.projection = srcMappingLayer.projection
    dstMappingLayer.repeat_image = srcMappingLayer.repeat_image
    dstMappingLayer.repetition_x = srcMappingLayer.repetition_x
    dstMappingLayer.repetition_y = srcMappingLayer.repetition_y
    dstMappingLayer.softness = srcMappingLayer.softness
    dstMappingLayer.swap_axes = srcMappingLayer.swap_axes
    dstMappingLayer.turbulence = srcMappingLayer.turbulence
    dstMappingLayer.type = srcMappingLayer.type
    dstMappingLayer.uv_mapping = srcMappingLayer.uv_mapping
    dstMappingLayer.vertical_flip = srcMappingLayer.vertical_flip
    dstMappingLayer.weight = srcMappingLayer.weight
    dstMappingLayer.vertex_color_layer = srcMappingLayer.vertex_color_layer
    dstMappingLayer.transformation = srcMappingLayer.transformation

    # イメージを指定.
    # これはマッピングパターンを指定後に呼ばないと無効になるため、最後に呼ぶ.
    if srcMappingLayer.image != None and srcMappingLayer.image.has_image:
      dstMappingLayer.image = srcMappingLayer.image

  shape.master_surface = masterSurface

# シーンをたどり、独立した表面材質を持つ形状を探す.
# 階層をたどり、独立した材質を持つ形状を検索
# @param[in]  shape         対象形状.
# @param[out] searchShapes  独立した材質を持つ形状を格納.
def searchMaterials (shape, searchShapes):
  if shape.type == 2 and shape.part_type == 11:  # カメラ.
    return
  if shape.type == 3:  # 光源.
    return
  if shape.type == 10:  # マスターイメージ.
    return
  if shape.type == 8:  # マスターサーフェス.
    return

  # マスターサーフェスを持たない場合.
  if shape.master_surface == None:
    # 表面材質を持つ場合.
    if shape.has_surface_attributes:
      searchShapes.append(shape)

  if shape.has_son:
    s = shape.son
    while s.has_bro:
      s = s.bro
      searchMaterials(s, searchShapes)

# マスターサーフェスを列挙.
# @param[in]  shape           対象形状.
# @param[out] masterSurfaces  マスターサーフェスを格納.
def getMasterSurfaces (shape, masterSurfaces):
  if shape.type == 8:  # マスターサーフェス.
    if shape.master_surface != None:
      masterSurfaces.append(shape.master_surface)

  if shape.has_son:
    s = shape.son
    while s.has_bro:
      s = s.bro
      getMasterSurfaces(s, masterSurfaces)
  
rootShape = scene.shape  # ルート形状.

# マスターサーフェスを列挙.
masterSurfacesA = []
getMasterSurfaces(rootShape, masterSurfacesA)

# 独立した表面材質を持つ形状を列挙.
searchShapesA = []
searchMaterials(rootShape, searchShapesA)

# 形状作成開始.
scene.begin_creating()

# マスターサーフェスと、各形状に割り当てられた独立した表面材質が一致するか.
convCou = 0
newCou = 0
for msLoop in range(len(masterSurfacesA)):
  masterSurface = masterSurfacesA[msLoop]

  for i in range(len(searchShapesA)):
    if searchShapesA[i] == None:
      continue

    # 表面材質が同じかチェック.
    if isSameSurface(searchShapesA[i].surface, masterSurface.surface):
      convCou += 1

      # searchShapesA[i]の表面材質を、masterSurfaceに置き換え.
      searchShapesA[i].master_surface = masterSurface
      searchShapesA[i] = None

# 独立した表面材質をマスターサーフェス化.
# また、同一のものはまとめる.
for i in range(len(searchShapesA)):
  if searchShapesA[i] == None:
    continue

  # searchShapesA[i]をマスターサーフェスにする.
  convSurfaceToMasterSurface(searchShapesA[i], newCou)

  masterSurface = searchShapesA[i].master_surface
  if masterSurface == None:
    continue

  newCou += 1

  for j in range(i + 1, len(searchShapesA)):
    if searchShapesA[j] == None:
      continue

    # 表面材質が同じかチェック.
    if isSameSurface(searchShapesA[j].surface, masterSurface.surface):
      convCou += 1

      # searchShapesA[j]の表面材質を、masterSurfaceに置き換え.
      searchShapesA[j].master_surface = masterSurface
      searchShapesA[j] = None

print "新しく追加したマスターサーフェス数 : " + str(newCou)
print "マスターサーフェスに置き換えた独立した材質数 : " + str(convCou)

# 形状作成終了.
scene.end_creating()

