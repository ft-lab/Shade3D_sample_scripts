//---------------------------------------------------------.
// グラフを描画するクラス.
//---------------------------------------------------------.

// @param[in] canvas               描画領域.
// @param[in] lightAngleListA      角度のリスト (垂直).
// @param[in] lightAngleListB      角度のリスト (水平).
// @param[in] lightIntensityList   光度のリスト (水平 * 垂直分).
var DrawEditGraph = function(canvas, lightAngleListA, lightAngleListB, lightIntensityList) {
    this.canvas = canvas;
    this.lightAngleListA    = lightAngleListA;
    this.lightAngleListB    = lightAngleListB;
    this.lightIntensityList = lightIntensityList;

    this.lampLuminousFlux = 1000.0;             // ランプ光束.
    this.luminousIntensityScale = 1.0;          // 光度にかける倍率.
    this.maxLuminousIntensity = 500.0;          // 最大光度.

    var scope = this;

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

    // 光度の配列を指定.
    this.setLightIntensityList = function (lightAngleListA, lightAngleListB, lightIntensityList) {
        scope.lightAngleListA    = lightAngleListA;
        scope.lightAngleListB    = lightAngleListB;
        scope.lightIntensityList = lightIntensityList;
    };

    // 描画処理.
    this.draw = function () {
        var width  = scope.canvas.width;
        var height = scope.canvas.height;

        var context = scope.canvas.getContext("2d");

        // 背景塗りつぶし.
        context.fillStyle = '#052005';
        context.fillRect(0, 0, width, height);

        var hMargin = 32;
        var vMargin = 24;
        var dWidth  = width - hMargin * 2;
        var dHeight = height - vMargin * 2;

        // マス目を描画.
        // 横軸が角度.
        // 縦軸は明るさ (cd).
        context.lineWidth = 0.5;
        var mCol = '#408040';
        var xCou = 9;
        var yCou = 10;
        var dx = parseFloat(dWidth) / parseFloat(xCou);
        var dy = parseFloat(dHeight) / parseFloat(yCou);
        var px = 0.0;
        for (var i = 0; i <= xCou; i++) {
            context.beginPath();
            context.strokeStyle = mCol;
            context.moveTo(hMargin + px, vMargin);
            context.lineTo(hMargin + px, dHeight + vMargin);
            context.stroke();
            px += dx;
        }

        var py = dHeight + vMargin;
        for (var i = 0; i <= yCou; i++) {
            context.beginPath();
            context.strokeStyle = mCol;
            context.moveTo(hMargin, py);
            context.lineTo(width - hMargin, py);
            context.stroke();
            py -= dy;
        }

        // cd/klm にする.
        var sV = (scope.lampLuminousFlux / scope.luminousIntensityScale) / 1000.0;

        // 水平の目盛りを描画.
        {
            context.font = "8pt Arial";
            context.fillStyle = '#ffffff';
            context.textAlign = "center";
            context.textBaseline = "top";

            maxAngle = scope.lightAngleListA[scope.lightAngleListA.length - 1];
            dAngle = maxAngle / parseFloat(xCou);

            px = hMargin;
            py = dHeight + vMargin + 2;
            for (var i = 0; i <= xCou; i++) {
                var str = StringUtil.getFloatToString(i * dAngle, 0);
                context.fillText(str, px, py);
                px += dx;
            }
            context.fillText("(度)", hMargin + dWidth + hMargin * 0.6, py);
        }

        // 垂直の目盛りを描画.
        {
            context.font = "8pt Arial";
            context.fillStyle = '#ffffff';
            context.textAlign = "right";
            context.textBaseline = "top";

            px = hMargin - 4;
            py = dHeight + vMargin - dy - 3;
            var dVal = (scope.maxLuminousIntensity) / parseFloat(yCou);
            var lVal = dVal;
            for (var i = 1; i <= yCou; i++) {
                var str = StringUtil.getFloatToString(lVal, 2);
                context.textAlign = "right";
                context.fillText(str, px, py);
                py -= dy;
                lVal += dVal;
            }

            context.fillText("(cd/klm)", px + 20, 8);
        }

        // グラフを描画.
        {
            context.lineWidth = 1.0;
            context.beginPath();
            context.strokeStyle = '#ffffff';

            var posList = new Array();

            var angleCou = scope.lightAngleListA.length;
            px = hMargin;
            dx = dWidth / parseFloat(angleCou - 1);
            py = 0.0;
            var scale = parseFloat(dHeight);
            var prevY = 0.0; 
            for (var i = 0; i < angleCou; i++, px += dx) {
                py = dHeight + vMargin;
                py -= (scope.lightIntensityList[i] / sV) * scale / scope.maxLuminousIntensity;
                //if (py < vMargin) py = vMargin;
                if (i == 0) {
                    context.moveTo(px, py);
                    continue;
                }
                context.lineTo(px, py);
                posList.push([px, py]);
            }
            context.stroke();

            // ポイントを描画.
            {
                context.fillStyle = '#ffff00';
                var sizeV = 1;
                for (var i = 0; i < posList.length; ++i) {
                    var pV = posList[i];
                    context.fillRect(pV[0] - sizeV, pV[1] - sizeV, sizeV + sizeV, sizeV + sizeV);
                }
            }
        }
    };
};

