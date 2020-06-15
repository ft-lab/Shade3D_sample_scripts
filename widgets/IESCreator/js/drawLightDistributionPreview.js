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

     // 角度値から明るさを取得 (垂直).
    // @param[in] angleV  角度 0.0 - 180.0
    // @param[in] iOffset this.lightIntensityList[]のオフセット。複数断面がある場合の処理.
    function getAngleToIntensityA (angleV, iOffset) {
        var vCou = scope.lightAngleListA.length;
        var minAngle = scope.lightAngleListA[0];
        var maxAngle = scope.lightAngleListA[vCou - 1];
        if (angleV < minAngle) return 0.0;
        if (angleV > maxAngle) return 0.0;

        var lPos = 0;
        var rPos = vCou - 1;

        // 2分検索で明るさを取得.
        var rIntensity = 0.0;
        var fMin = 1e-4;
        while (lPos < rPos) {
            var cPos = parseInt((rPos + lPos) / 2);
            var lV = scope.lightAngleListA[lPos];
            var rV = scope.lightAngleListA[rPos];
            var cV = scope.lightAngleListA[cPos];
            if (Math.abs(angleV - lV) < fMin) {
                rIntensity = scope.lightIntensityList[lPos + iOffset];
                break;
            }
            if (Math.abs(angleV - rV) < fMin) {
                rIntensity = scope.lightIntensityList[rPos + iOffset];
                break;
            }
            if (Math.abs(angleV - cV) < fMin) {
                rIntensity = scope.lightIntensityList[cPos + iOffset];
                break;
            }
            if (lPos + 1 >= rPos || cPos == lPos || cPos == rPos) {
                for (var i = lPos; i <= rPos; ++i) {
                    if (i >= vCou) break;
                    var angle1 = scope.lightAngleListA[i];
                    var angle2 = scope.lightAngleListA[i + 1];
                    if (angleV >= angle1 && angleV <= angle2) {
                        var v1 = scope.lightIntensityList[i + iOffset];
                        var v2 = scope.lightIntensityList[i + 1 + iOffset];
                        var a1 = (angleV - angle1) / (angle2 - angle1);
                        var a2 = 1.0 - a1;
                        rIntensity = v1 * a2 + v2 * a1;
                        break;
                    }
                }
                break;
            }

            if (angleV <= cV) {
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
            for (var x = 0; x < width; x++) {
                var px = (parseFloat(x - centerX) / scope.zoom) / radius;
                var py = (parseFloat(y - centerY) / scope.zoom) / radius;
                var pz = scope.distanceFromWall / radius;
        
                var lenV = Math.sqrt(px * px + py * py + pz * pz);
                lenV = Math.max(0.001, lenV);

                var dirX = px / lenV;
                var dirY = py / lenV;
                var dirZ = pz / lenV;
        
                // (0, -1)を中心としたcosθの計算 (内積になる).
                var intensity = 0.0;
                var cosV = dirY;
                var angleV = 0.0;
                if (cosV < 0.0 && maxAngle <= 90.0) {	// 180度を超える場合.
                    intensity = 0.0;

                } else {
                    if (cosV < 0.0 && maxAngle > 90.0) {
                        // 度数に変換(0 - 90).
                        angleV = Math.acos(cosV) * 180.0 / Math.PI;
                        angleV = Math.max(0.0, angleV);
                        angleV = Math.min(90.0, angleV);
                        angleV += 90.0;
                    } else {
                        // 度数に変換(0 - 90).
                        angleV = Math.acos(cosV) * 180.0 / Math.PI;
                        angleV = Math.max(0.0, angleV);
                        angleV = Math.min(90.0, angleV);
                    }

                    var iOffset = 0;
                    if (!symmetryF) {   // 左右非対称にする場合.
                        if (dirX >= 0.0) iOffset = hPos1;
                        else iOffset = hPos2;
                    }
        
                    // angleVの位置での光度を取得.
                    intensity = getAngleToIntensityA(angleV, iOffset);

                    // 角度とcd/klmによる照度を計算.
                    //intensity = intensity * Math.pow(Math.cos(angleV * Math.PI / 180.0), 3.0) / sV;
                    intensity = intensity / sV;

                    intensity = (intensity * scope.brightness) / maxV;
        
                    if (intensity > 0.0 && lenV > 0.0) {
                        intensity = intensity / (lenV * lenV);
                    //    intensity = intensity / (py * py);
                    }
                }
                intensityA[iPos] = Math.min(1.0, intensity);
                iPos++;
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

