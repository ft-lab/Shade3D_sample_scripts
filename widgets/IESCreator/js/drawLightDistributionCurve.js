//---------------------------------------------------------.
// 配光曲線を描画するクラス.
//---------------------------------------------------------.

// @param[in] canvas               描画領域.
// @param[in] lightIntensityList   光度のリスト(Array(90 + 1)).
var DrawLightDistributionCurve = function(canvas, lightIntensityList) {
    this.canvas = canvas;
    this.lightIntensityList = lightIntensityList;
    this.lampLuminousFlux = 1000.0;             // ランプ光束.
    this.luminousIntensityScale = 1.0;          // 光度にかける倍率.
    this.maxLuminousIntensity = 500.0;          // 最大光度.
};

// ランプ光束を指定.
DrawLightDistributionCurve.prototype.setLampLuminousFlux = function (intensityV) {
    this.lampLuminousFlux = intensityV;
};

// 最大光度を指定.
DrawLightDistributionCurve.prototype.setMaxLuminousIntensity = function (intensityV) {
    this.maxLuminousIntensity = intensityV;
};

// 光度にかける倍率を指定.
DrawLightDistributionCurve.prototype.setLuminousIntensityScale = function (scaleV) {
    this.luminousIntensityScale = scaleV;
};

// 光度の配列を指定.
DrawLightDistributionCurve.prototype.setLightIntensityList = function (lightIntensityList) {
    this.lightIntensityList = lightIntensityList;
};

// 描画処理.
DrawLightDistributionCurve.prototype.draw = function () {
    var width  = this.canvas.width;
    var height = this.canvas.height;

    var context = this.canvas.getContext("2d");

    // 背景塗りつぶし.
    context.fillStyle = '#ffffff';
    context.fillRect(0, 0, width, height);

    var grayCol  = '#909090';
    var blackCol = '#000000';

    // 外枠を描画.
    context.beginPath();
    context.lineWidth = 1.0;
    context.strokeStyle = grayCol;
    context.strokeRect(0, 0, width, height);
    context.stroke();

    // 同心円を描画.
    var circleCou = 10;
    var centerX = width / 2;
    var centerY = height / 2;
    var maxR = parseFloat(width) * 0.5;
    var rD = maxR / parseFloat(circleCou);
    var r = rD;
    for (var i = 1; i < circleCou; ++i) {
        context.beginPath();
        context.strokeStyle = grayCol;
        context.lineWidth = 0.5;
        context.arc(centerX, centerY, r, 0, Math.PI * 2);
        context.stroke();
        r += rD;
    }

    // 10度ごとに向きを描画.
    for (var i = 0; i < 36; ++i) {
        var angleV = parseFloat(i) * 10.0;
        var dV = angleV * Math.PI / 180.0;
        var dxS = Math.cos(dV);
        var dyS = Math.sin(dV);
        var dx0 = dxS * rD;
        var dy0 = dyS * rD;
        var dx = dxS * maxR;
        var dy = dyS * maxR;
        if (i == 0 || i == 9 || i == 18 || i == 27) {
            dx0 = dy0 = 0.0;
        }
        context.beginPath();
        context.strokeStyle = grayCol;
        context.lineWidth = 0.5;
        context.moveTo(centerX + dx0, centerY - dy0);
        context.lineTo(centerX + dx, centerY - dy);
        context.stroke();
    }

	// 曲線を描画.
	{
		for (var loop = 0; loop < 2; ++loop) {
			context.beginPath();
			context.strokeStyle = blackCol;
			context.lineWidth = 1.0;
			var cou = this.lightIntensityList.length;
			for (var i = 0; i <= 90; ++i) {
				var angleV = parseFloat(i);
				var dV = (angleV - 90.0) * Math.PI / 180.0;
				var dxS = Math.cos(dV);
				var dyS = Math.sin(dV);
				if (loop == 1) dxS = -dxS;
				var v = this.lightIntensityList[i] * maxR / maxLuminousIntensity;
				var dx = dxS * v;
				var dy = dyS * v;
				if (i == 0) {
					context.moveTo(centerX + dx, centerY - dy);
				} else {
					context.lineTo(centerX + dx, centerY - dy);				
				}
			}
			context.stroke();
		}
	}

	// 光度値を描画.
	{
		context.font = "8pt Arial";
		context.fillStyle = '#000000';
		context.textAlign = "center";
        context.textBaseline = "alphabetic";        // デフォルト.

		var angleV = 0.0;
		var dV = (angleV - 90.0) * Math.PI / 180.0;
		var dxS = Math.cos(dV);
		var dyS = Math.sin(dV);
		var v = this.lightIntensityList[i] * maxR / this.maxLuminousIntensity;
		var dx = dxS * v;
		var dy = dyS * v;

		var cVal = this.maxLuminousIntensity.toString() + " (cd)";
		context.fillText(cVal, centerX , centerY + maxR - 3.0);
    }
    
    // ランプ光束と倍率を描画.
    {
		context.font = "8pt Arial";
		context.fillStyle = '#000000';
        context.textAlign = "left";
        context.textBaseline = "top";

        var strV = "ランプ光束 : " + this.lampLuminousFlux.toString() + " lm";
		context.fillText(strV, 4, 4);

        strV = "光度倍率 : x " + this.luminousIntensityScale.toString();
		context.fillText(strV, 4, 4 + 12);
    }
};

