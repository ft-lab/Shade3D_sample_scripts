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
    this.brightness = 1.0;                      // 輝度.

    // 角度値から明るさを取得 (垂直).
    // @param[in] angleV  角度 0.0 - 180.0
    // @param[in] iOffset this.lightIntensityList[]のオフセット。複数断面がある場合の処理.
    this.getAngleToIntensityA = function (angleV, iOffset) {
        var vCou = this.lightAngleListA.length;
        var minAngle = this.lightAngleListA[0];
        var maxAngle = this.lightAngleListA[vCou - 1];
        if (angleV < minAngle) return 0.0;
        if (angleV > maxAngle) return 0.0;

        var lPos = 0;
        var rPos = vCou - 1;

        // 2分検索で明るさを取得.
        var rIntensity = 0.0;
        var fMin = 1e-4;
        while (lPos < rPos) {
            var cPos = parseInt((rPos + lPos) / 2);
            var lV = this.lightAngleListA[lPos];
            var rV = this.lightAngleListA[rPos];
            var cV = this.lightAngleListA[cPos];
            if (Math.abs(angleV - lV) < fMin) {
                rIntensity = this.lightIntensityList[lPos + iOffset];
                break;
            }
            if (Math.abs(angleV - rV) < fMin) {
                rIntensity = this.lightIntensityList[rPos + iOffset];
                break;
            }
            if (Math.abs(angleV - cV) < fMin) {
                rIntensity = this.lightIntensityList[cPos + iOffset];
                break;
            }
            if (lPos + 1 >= rPos || cPos == lPos || cPos == rPos) {
                for (var i = lPos; i <= rPos; ++i) {
                    if (i >= vCou) break;
                    var angle1 = this.lightAngleListA[i];
                    var angle2 = this.lightAngleListA[i + 1];
                    if (angleV >= angle1 && angleV <= angle2) {
                        var v1 = this.lightIntensityList[i + iOffset];
                        var v2 = this.lightIntensityList[i + 1 + iOffset];
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
    }
};

// ランプ光束を指定.
DrawLightDistributionPreview.prototype.setLampLuminousFlux = function (intensityV) {
    this.lampLuminousFlux = intensityV;
};

// 最大光度を指定.
DrawLightDistributionPreview.prototype.setMaxLuminousIntensity = function (intensityV) {
    this.maxLuminousIntensity = intensityV;
};

// 光度にかける倍率を指定.
DrawLightDistributionPreview.prototype.setLuminousIntensityScale = function (scaleV) {
    this.luminousIntensityScale = scaleV;
};

// 光度の配列を指定.
DrawLightDistributionPreview.prototype.setLightIntensityList = function (lightAngleListA, lightAngleListB, lightIntensityList) {
    this.lightAngleListA    = lightAngleListA;
    this.lightAngleListB    = lightAngleListB;
    this.lightIntensityList = lightIntensityList;
};

// 輝度を指定.
DrawLightDistributionPreview.prototype.setBrightness = function (fVal) {
    this.brightness = fVal;
};

// 描画処理.
DrawLightDistributionPreview.prototype.draw = function () {
    var width  = this.canvas.width;
    var height = this.canvas.height;
    var context = this.canvas.getContext("2d");

	// ピクセル描画のImageを作成.
	if (this.previewImage == null) {
		this.previewImage = context.createImageData(width, height);
	}

    var widthH = width / 2;
    var centerX = parseFloat(widthH);
    var centerY = parseFloat(20);
    var radius = parseFloat(widthH) * 0.8;

    var maxV = 1000.0;

    // 角度の最大値を取得.
    // 90.0と180.0で左右対称にするか180度使うか決まる.
    var maxAngle = this.lightAngleListA[this.lightAngleListA.length - 1];

    // 対象にする場合.
    var symmetryF = (maxAngle <= 90.0 && this.lightAngleListB.length == 1);

    var vAngleCou = this.lightAngleListA.length;

    // Imageを更新.
    if (symmetryF) {
        var iPos = 0;
        for (var y = 0; y < height; y++) {
            for (var x = 0; x < width; x++) {
                var px = parseFloat(x - centerX) / radius;
                var py = parseFloat(y - centerY) / radius;
    
                var lenV = Math.sqrt(px * px + py * py);
                var dirX = px / lenV;
                var dirY = py / lenV;
    
                // (0, -1)を中心としたcosθの計算 (内積になる).
                var intensity = 0.0;
                var cosV = dirY;
                if (cosV < 0.0) {	// 180度を超える場合.
                    intensity = 0.0;
                } else {
                    // 度数に変換(0 - 90).
                    var angleV = Math.acos(cosV) * 180.0 / Math.PI;
                    angleV = Math.max(0.0, angleV);
                    angleV = Math.min(90.0, angleV);
    
                    // angleVの位置での光度を取得.
                    intensity = this.getAngleToIntensityA(angleV, 0);
    
                    intensity = intensity * this.luminousIntensityScale;
                    intensity = (intensity * this.brightness) / maxV;
    
                    if (intensity > 0.0 && lenV > 0.0) {
                        intensity = intensity / (lenV * lenV);
                    }
                    intensity = Math.max(0.0, intensity);
                    intensity = Math.min(1.0, intensity);
                }
    
                var iV = parseInt(intensity * 255.0);
                this.previewImage.data[iPos + 0] = iV;
                this.previewImage.data[iPos + 1] = iV;
                this.previewImage.data[iPos + 2] = iV;
                this.previewImage.data[iPos + 3] = 255;
                iPos += 4;
            }
        }
    } else {
        // 左右非対称にする場合.
        var hPos1 = 0;
        var hPos2 = (this.lightAngleListB.length - 1) * vAngleCou;
        var iPos = 0;
        for (var y = 0; y < height; y++) {
            for (var x = 0; x < width; x++) {
                var px = parseFloat(x - centerX) / radius;
                var py = parseFloat(y - centerY) / radius;
    
                var lenV = Math.sqrt(px * px + py * py);
                var dirX = px / lenV;
                var dirY = py / lenV;
    
                // (0, -1)を中心としたcosθの計算 (内積になる).
                var intensity = 0.0;
                var cosV = dirY;
                if (cosV < 0.0) {	// 180度を超える場合.
                    intensity = 0.0;
                } else {
                    // 度数に変換(0 - 90).
                    var angleV = Math.acos(cosV) * 180.0 / Math.PI;
                    angleV = Math.max(0.0, angleV);
                    angleV = Math.min(90.0, angleV);

                    var iOffset = 0;
                    if (dirX >= 0.0) iOffset = hPos1;
                    else iOffset = hPos2;
    
                    // angleVの位置での光度を取得.
                    intensity = this.getAngleToIntensityA(angleV, iOffset);
    
                    intensity = intensity * this.luminousIntensityScale;
                    intensity = (intensity * this.brightness) / maxV;
    
                    if (intensity > 0.0 && lenV > 0.0) {
                        intensity = intensity / (lenV * lenV);
                    }
                    intensity = Math.max(0.0, intensity);
                    intensity = Math.min(1.0, intensity);
                }
    
                var iV = parseInt(intensity * 255.0);
                this.previewImage.data[iPos + 0] = iV;
                this.previewImage.data[iPos + 1] = iV;
                this.previewImage.data[iPos + 2] = iV;
                this.previewImage.data[iPos + 3] = 255;
                iPos += 4;
            }
        }
    }

    // 画像を描画.
    context.putImageData(this.previewImage, 0, 0);
};
