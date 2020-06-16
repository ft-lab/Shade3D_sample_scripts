//---------------------------------------------------------.
// 配光のプレビューを描画するクラス.
//---------------------------------------------------------.
// @param[in] canvas               描画領域.
// @param[in] lightAngleListA      角度のリスト (垂直).
// @param[in] lightAngleListB      角度のリスト (水平).
// @param[in] lightIntensityList   光度のリスト (垂直 * 水平).
var DrawLightDistributionPreview = function(canvas, lightAngleListA, lightAngleListB, lightIntensityList) {
    this.canvas = canvas;
    this.lightAngleListA    = lightAngleListA;
    this.lightAngleListB    = lightAngleListB;
    this.lightIntensityList = lightIntensityList;
    
    this.maxLuminousIntensity = 500.0;          // 最大光度.
    this.lampLuminousFlux = 1000.0;             // ランプ光束.
    this.luminousIntensityScale = 1.0;          // 光度にかける倍率.
    this.previewImage = null;                   // ピクセル描画のImage.

    // プレビューでの光源の中心位置.
    this.lightCenterX = parseFloat(this.canvas.width) * 0.5;
    this.lightCenterY = 20.0;

    this.brightness = 1.0;                      // 輝度.
    this.zoom = 1.0;                            // ズーム.
    this.distanceFromWall = 1.0;                // 壁から離れる距離.

    var scope = this;

    // 角度値から明るさを取得.
    // @param[in] cosTheta  垂直角度 0 ~ 180.
    // @param[in] cosPhi    水平角度 -180 ~ +180.
    function getAngleToIntensityA (cosTheta, cosPhi) {
        var vCou = scope.lightAngleListA.length;
        var minAngle = scope.lightAngleListA[0];
        var maxAngle = scope.lightAngleListA[vCou - 1];
        if (cosTheta < minAngle) return 0.0;
        if (cosTheta > maxAngle) return 0.0;

        var lPos = 0;
        var rPos = vCou - 1;

        // 水平方向の採用断面を取得.
        var iOffset = 0;
        if (scope.lightAngleListB.length == 1) {
            // 軸対称.
        } else {
            // 水平角度で、対象の範囲を取得.
            // TODO :まだ未実装..
            var minAngleB = scope.lightAngleListB[0];
            var maxAngleB = scope.lightAngleListB[lightAngleListB.length - 1];

            var angle2 = cosPhi + 360.0;
            var angle2I = parseInt(angle2);
            angle2 -= parseFloat(angle2I);
            
            if (cosPhi < 0.0) iOffset = (lightAngleListB.length - 1) * vCou;
        }

        // 2分検索で明るさを取得.
        var rIntensity = 0.0;
        var fMin = 1e-4;
        while (lPos < rPos) {
            var cPos = parseInt((rPos + lPos) / 2);
            var lV = scope.lightAngleListA[lPos];
            var rV = scope.lightAngleListA[rPos];
            var cV = scope.lightAngleListA[cPos];
            if (Math.abs(cosTheta - lV) < fMin) {
                rIntensity = scope.lightIntensityList[lPos + iOffset];
                break;
            }
            if (Math.abs(cosTheta - rV) < fMin) {
                rIntensity = scope.lightIntensityList[rPos + iOffset];
                break;
            }
            if (Math.abs(cosTheta - cV) < fMin) {
                rIntensity = scope.lightIntensityList[cPos + iOffset];
                break;
            }
            if (lPos + 1 >= rPos || cPos == lPos || cPos == rPos) {
                for (var i = lPos; i <= rPos; ++i) {
                    if (i >= vCou) break;
                    var angle1 = scope.lightAngleListA[i];
                    var angle2 = scope.lightAngleListA[i + 1];
                    if (cosTheta >= angle1 && cosTheta <= angle2) {
                        var v1 = scope.lightIntensityList[i + iOffset];
                        var v2 = scope.lightIntensityList[i + 1 + iOffset];
                        var a1 = (cosTheta - angle1) / (angle2 - angle1);
                        var a2 = 1.0 - a1;
                        rIntensity = v1 * a2 + v2 * a1;
                        break;
                    }
                }
                break;
            }

            if (cosTheta <= cV) {
                rPos = cPos;
            } else {
                lPos = cPos;
            }
        }

        return rIntensity;
    };

    // マウスクリックされた時に呼ばれる.
    function onClickCanvas (e) {
        // canvasの位置を取得.
        var px = 0;
        var py = 0;
        var curElement = scope.canvas;
        while (curElement != null) {
            px += curElement.offsetLeft;
            py += curElement.offsetTop;
            if (curElement.parentElement == null) break;
            curElement = curElement.parentElement;
        }

        // マウス位置をローカル座標での位置に変換.        
		var mx = e.clientX - px;
  		var my = e.clientY - py;

        // 光源の中心位置を変更.
        scope.lightCenterX = parseFloat(mx);
        scope.lightCenterY = parseFloat(my);
      
        scope.draw();
    };

    // ランプ光束を指定.
    this.setLampLuminousFlux = function (intensityV) {
        scope.lampLuminousFlux = intensityV;
    };

    // 最大光度を指定.
    this.setMaxLuminousIntensity = function (intensityV) {
        scope.maxLuminousIntensity = intensityV;
    };

    // 光度にかける倍率を指定.
    this.setLuminousIntensityScale = function (scaleV) {
        scope.luminousIntensityScale = scaleV;
    };

    // 壁から離れる距離を指定.
    this.setDistanceFromWall = function (dist) {
        scope.distanceFromWall = dist;
    }

    // ズーム値を指定.
    this.setZoom = function (zoomV) {
        scope.zoom = zoomV;
    }

    // 光度の配列を指定.
    this.setLightIntensityList = function (lightAngleListA, lightAngleListB, lightIntensityList) {
        scope.lightAngleListA    = lightAngleListA;
        scope.lightAngleListB    = lightAngleListB;
        scope.lightIntensityList = lightIntensityList;
    };

    // 輝度を指定.
    this.setBrightness = function (fVal) {
        scope.brightness = fVal;
    };

    // 描画処理.
    this.draw = function () {
        var width  = scope.canvas.width;
        var height = scope.canvas.height;
        var context = scope.canvas.getContext("2d");

        // ピクセル描画のImageを作成.
        if (scope.previewImage == null) {
            scope.previewImage = context.createImageData(width, height);
        }

        var widthH = width / 2;
        var centerX = scope.lightCenterX;
        var centerY = scope.lightCenterY;
        var radius = parseFloat(widthH) * 0.8;

        var maxV = 1000.0;

        // cd/klm にする.
        var sV = (scope.lampLuminousFlux / scope.luminousIntensityScale) / 1000.0;

        // 角度の最大値を取得.
        // 90.0と180.0で左右対称にするか180度使うか決まる.
        var maxAngle = scope.lightAngleListA[scope.lightAngleListA.length - 1];

        // 対象にする場合.
        var symmetryF = (maxAngle <= 90.0 && scope.lightAngleListB.length == 1);

        var vAngleCou = scope.lightAngleListA.length;

        // 明るさを配列に格納.
        var intensityA = new Array(width * height);
        var hPos1 = 0;
        var hPos2 = (scope.lightAngleListB.length - 1) * vAngleCou;
        var iPos = 0;
        for (var y = 0; y < height; y++) {
            for (var x = 0; x < width; x++, iPos++) {
                intensityA[iPos] = 1.0;
                var px = (parseFloat(x - centerX) / scope.zoom) / radius;
                var py = (parseFloat(y - centerY) / scope.zoom) / radius;
                var pz = scope.distanceFromWall / radius;
        
                var lenV = Math.sqrt(px * px + py * py + pz * pz);
                if (lenV < 0.0001) continue;

                var dirX = px / lenV;
                var dirY = py / lenV;
                var dirZ = pz / lenV;
                if (Math.abs(dirX) < 0.001 && Math.abs(dirZ) < 0.001) continue;

                // (dirX, dirY, dirZ)より、垂直(Theta)と水平方向(Phi)の回転を取得.
                var cosTheta = Math.acos(dirY);     // 0 ~ -180.
                var cosPhi   = Math.acos(dirX / Math.sqrt(dirX*dirX + dirZ*dirZ));      // -180 ~ + 180.
                if (dirZ < 0.0) cosPhi = -cosPhi;

                // 度数に変換.
                cosTheta = cosTheta * 180.0 / Math.PI;
                cosPhi   = cosPhi * 180.0 / Math.PI;
        
                var intensity = 0.0;
                if (dirY < 0.0 && maxAngle <= 90.0) {	// 180度を超える場合.
                    intensity = 0.0;

                } else {
                    // angleVの位置での光度を取得.
                    intensity = getAngleToIntensityA(cosTheta, cosPhi);

                    // 角度とcd/klmによる照度を計算.
                    intensity = intensity / sV;

                    intensity = (intensity * scope.brightness) / maxV;
        
                    if (intensity > 0.0 && lenV > 0.0) {
                        intensity = intensity / (lenV * lenV);
                    }
                }
                intensityA[iPos] = Math.min(1.0, intensity);
            }
        }

        // Imageを更新.
        iPos = 0;
        var iPos2 = 0;
        for (var y = 0; y < height; y++) {
            for (var x = 0; x < width; x++) {
                var iV = parseInt(intensityA[iPos] * 255.0);
                scope.previewImage.data[iPos2 + 0] = iV;
                scope.previewImage.data[iPos2 + 1] = iV;
                scope.previewImage.data[iPos2 + 2] = iV;
                scope.previewImage.data[iPos2 + 3] = 255;
                iPos2 += 4;
                iPos++;
            }
        }

        // 画像を描画.
        context.putImageData(scope.previewImage, 0, 0);
    };

    // マウスイベントを登録.
    scope.canvas.addEventListener('click', onClickCanvas, false);
};

