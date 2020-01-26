# スクリプトのサンプル

## システム関連

|ファイル名|内容|
|--|--|
|[ExecuteExternalCommand.py](./ExecuteExternalCommand.py)|外部コマンドを実行し、結果の文字列を表示|
|[GetSysPath.py](./GetSysPath.py)|検索パスの一覧と追加|
|[GenerateUUID.py](./GenerateUUID.py)|UUIDを生成|

## モデリング関連

|ファイル名|内容|
|--|--|
|[CleanupPolygonmesh.py](./CleanupPolygonmesh.py)|ポリゴンメッシュの不要な頂点/稜線を削除|
|[GetPolygonmeshInfo.py](./GetPolygonmeshInfo.py)|ポリゴンメッシュ情報を取得|
|[GetSelectedPoint.py](./GetSelectedPoint.py)|選択頂点の座標値を取得|
|[GetSelectedShapes.py](./GetSelectedShapes.py)|選択形状を一覧|
|[SelectPolygonmesh.py](./SelectPolygonmesh.py)|シーンのポリゴンメッシュをすべて選択|
|[SetCursorPosition.py](./SetCursorPosition.py)|3次元カーソル位置を指定|
|[TraceHierarchy.py](./TraceHierarchy.py)|シーン階層をたどる|
|[CalcLineLength.py](./CalcLineLength.py)|線形状の長さを計算|
|[GetSceneInfo.py](./GetSceneInfo.py)|シーンの各要素数を取得|
|[ListUnreferencedImages.py](./ListUnreferencedImages.py)|未参照のイメージを一覧|
|[ShowDialog.py](./ShowDialog.py)|ダイアログボックスを表示|
|[ChangePoint.py](./ChangePoint.py)|選択ポイントの座標値を変更|
|[ClearBakeNormals.py](./ClearBakeNormals.py)|ポリゴンメッシュのインポートした固定法線をクリア|
|[AlignToLine.py](./AlignToLine.py)|選択形状を記憶した線形状に整列|
|[ConvLineToPolyLine.py](./ConvLineToPolyLine.py)|線形状を等間隔の直線群に変換|
|[ConvLineToMeshEdge.py](./ConvLineToMeshEdge.py)|線形状をポリゴンメッシュのエッジに変換|
|[LineToMeshTube.py](./LineToMeshTube.py)|線形状からポリゴンメッシュのチューブを作成|
|[GetActivePointsCount.py](./GetActivePointsCount.py)|線形状で選択されたコントロールポイント数を取得|
|[SelectPolygonmeshSingleVertex.py](./SelectPolygonmeshSingleVertex.py)|ポリゴンメッシュの重複頂点で、1つの頂点のみを選択|
|[CheckSkinMesh.py](./CheckSkinMesh.py)|スキンが割り当てられているポリゴンメッシュを列挙|
|[EnumLinePoints.py](./EnumLinePoints.py)|線形状のコントロールポイント情報を表示|
|[Calc2PointsLength.py](./Calc2PointsLength.py)|選択された2つの頂点(コントロールポイント)の長さを計算|
|[MeshToWireframe.py](./MeshToWireframe.py)|ポリゴンメッシュをワイヤーフレームに変換|
|[OptimizeMeshVertices.py](./OptimizeMeshVertices.py)|ポリゴンメッシュの直線を構成する頂点を除去し最適化|
|[ClearMeshVertexColorLayers.py](./ClearMeshVertexColorLayers.py)|ポリゴンメッシュの頂点カラーレイヤをまとめて削除|
|[CreateCubemapCube.py](./CreateCubemapCube.py)|キューブマップテクスチャより、キューブマップを貼った立方体を作成|
|[SelectMeshBoxes.py](./SelectMeshBoxes.py)|ポリゴンメッシュ内の直方体要素を選択|

## 表面材質関連

|ファイル名|内容|
|--|--|
|[SearchMaterial.py](./SearchMaterial.py)|マスターサーフェスではない独立した材質を持つ形状を列挙|
|[ToMasterSurfaces.py](./ToMasterSurfaces.py)|独立した表面材質をマスターサーフェスに整理|

## テクスチャ関連

|ファイル名|内容|
|--|--|
|[CreateColorTexture.py](./CreateColorTexture.py)|単一色のテクスチャを生成|
|[UnpackImages.py](./UnpackImages.py)|テクスチャイメージのRGBA要素を分解(Unpack)|
|[PackImages.py](./PackImages.py)|マスターイメージとしてRGBA要素を指定し、合成(Pack)|

## カメラ関連

|ファイル名|内容|
|--|--|
|[GetCameraFOV.py](./GetCameraFOV.py)|カメラの視野角度を取得|
|[CalcCameraNearClip.py](./CalcCameraNearClip.py)|透視投影カメラの近クリップ面までの距離を計算|


## レンダリング関連

|ファイル名|内容|
|--|--|
|[SaveRenderingImage.py](./SaveRenderingImage.py)|レンダリング画像をファイル保存|
|[GetZDepthImage.py](./GetZDepthImage.py)|レンダリングイメージのZ値(ZDepth)を取得し、マスターイメージとして出力|

## エクスポート関連

|ファイル名|内容|
|--|--|
|[ExportCubemapTextures.py](./ExportCubemapTextures.py)|キューブマップテクスチャを生成して出力|
