# -----------------------------------------------------.
# キューブマップテクスチャより、キューブマップを貼った立方体を作成.
# キューブマップテクスチャは、+X/-X/+Y/-Y/+Z/-Zが縦に並んだテクスチャとする.
#
# @title \en Create a cube with a cube map from a cube map texture \enden
# @title \ja キューブマップテクスチャより、キューブマップを貼った立方体を作成\endja
# -----------------------------------------------------.

import math

scene = xshade.scene()

# ---------------------------------------------------.
# マスターイメージを指定し、.
# キューブマップを貼り付けたポリゴンメッシュの立方体を作成.
# @param[in] masterImage  
# ---------------------------------------------------.
def createMeshCubeWithCubemap(masterImage):
    if masterImage.type != 10:
        return None
    
    cubeSize  = 1000.0
    cubeSizeH = cubeSize * 0.5

    # 頂点座標.
    meshVertices = []
    meshVertices.append([-cubeSizeH,  cubeSizeH,  cubeSizeH])
    meshVertices.append([ cubeSizeH,  cubeSizeH,  cubeSizeH])
    meshVertices.append([-cubeSizeH, -cubeSizeH,  cubeSizeH])
    meshVertices.append([ cubeSizeH, -cubeSizeH,  cubeSizeH])
    meshVertices.append([-cubeSizeH,  cubeSizeH, -cubeSizeH])
    meshVertices.append([ cubeSizeH,  cubeSizeH, -cubeSizeH])
    meshVertices.append([-cubeSizeH, -cubeSizeH, -cubeSizeH])
    meshVertices.append([ cubeSizeH, -cubeSizeH, -cubeSizeH])

    # 面のインデックス.
    meshFacesI = []
    meshFacesI.append([5, 1, 3, 7])     # +X
    meshFacesI.append([0, 4, 6, 2])     # -X
    meshFacesI.append([0, 1, 5, 4])     # +Y
    meshFacesI.append([6, 7, 3, 2])     # -Y
    meshFacesI.append([1, 0, 2, 3])     # +Z
    meshFacesI.append([4, 5, 7, 6])     # -Z

    # UV.
    fMin = 0.0001
    uSize = 1.0
    vSize = 1.0 / 6.0
    meshFaceUVs = []

    pV = 0.0
    meshFaceUVs.append([ [0.0, 0.0 + pV], [uSize - fMin, 0.0 + pV], [uSize - fMin, pV + vSize - fMin], [0.0, pV + vSize - fMin] ])
    pV += vSize
    meshFaceUVs.append([ [0.0, 0.0 + pV], [uSize - fMin, 0.0 + pV], [uSize - fMin, pV + vSize - fMin], [0.0, pV + vSize - fMin] ])
    pV += vSize
    meshFaceUVs.append([ [0.0, 0.0 + pV], [uSize - fMin, 0.0 + pV], [uSize - fMin, pV + vSize - fMin], [0.0, pV + vSize - fMin] ])
    pV += vSize
    meshFaceUVs.append([ [0.0, 0.0 + pV], [uSize - fMin, 0.0 + pV], [uSize - fMin, pV + vSize - fMin], [0.0, pV + vSize - fMin] ])
    pV += vSize
    meshFaceUVs.append([ [0.0, 0.0 + pV], [uSize - fMin, 0.0 + pV], [uSize - fMin, pV + vSize - fMin], [0.0, pV + vSize - fMin] ])
    pV += vSize
    meshFaceUVs.append([ [0.0, 0.0 + pV], [uSize - fMin, 0.0 + pV], [uSize - fMin, pV + vSize - fMin], [0.0, pV + vSize - fMin] ])

    # ポリゴンメッシュを作成.
    scene.begin_creating()
    pMesh = scene.begin_polygon_mesh('cube')

    for i in range(8):
        scene.append_polygon_mesh_vertex(meshVertices[i])

    for i in range(6):
        scene.append_polygon_mesh_face(meshFacesI[i])

    pMesh.append_uv_layer()
    uvIndex = 0
    for i in range(6):
        f = pMesh.face(i)
        for j in range(4):
            f.set_face_uv(uvIndex, j, meshFaceUVs[i][j])

    scene.end_polygon_mesh()

    pMesh.make_edges()   # 稜線を生成.

    # 表面材質を割り当て.
    pMesh.has_surface_attributes = True
    pMesh.surface.no_shading = True             # 陰影付けしない.
    pMesh.surface.do_not_cast_shadow = True     # 影を落とさない.
    pMesh.surface.do_not_show_shadow = True     # 影を表示しない.
    pMesh.surface.highlight = 0.0   # 光沢1.

    pMesh.surface.append_mapping_layer()
    curMappingLayer = pMesh.surface.mapping_layer(0)
    curMappingLayer.pattern = 14  # イメージマッピング.
    curMappingLayer.type    = 0  # 拡散反射.
    curMappingLayer.image   = masterImage.image
    curMappingLayer.blur    = True

    scene.end_creating()

    return pMesh

# -------------------------------------.
activeShape = scene.active_shape()
if createMeshCubeWithCubemap(activeShape) == None:
    print 'キューブマップのマスターイメージを選択してください。'







