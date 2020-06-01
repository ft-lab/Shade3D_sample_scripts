//---------------------------------------------------------.
// 配光のプレビューを描画するクラス.
//---------------------------------------------------------.
// @param[in] canvas               描画領域.
// @param[in] lightIntensityList   光度のリスト(Array(90 + 1)).
var DrawLightDistributionPreview = function(canvas, lightIntensityList) {
    this.canvas = canvas;
    this.lightIntensityList = lightIntensityList;
    this.maxLuminousIntensity = 500.0;          // 最大光度.
    this.lampLuminousFlux = 1000.0;             // ランプ光束.
    this.luminousIntensityScale = 1.0;          // 光度にかける倍率.
    this.previewImage = null;                   // ピクセル描画のImage.
    this.brightness = 1.0;                      // 輝度.
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
DrawLightDistributionPreview.prototype.setLightIntensityList = function (lightIntensityList) {
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

    // Imageを更新.
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
                var angleI = parseInt(Math.acos(cosV) * 180.0 / Math.PI);
                angleI = Math.max(0, angleI);
                angleI = Math.min(89, angleI);
                intensity = this.lightIntensityList[angleI] * this.luminousIntensityScale;
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

    // 画像を描画.
    context.putImageData(this.previewImage, 0, 0);
};
