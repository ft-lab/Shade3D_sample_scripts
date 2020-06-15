//---------------------------------------------------------.
// 配光曲線を描画するクラス.
//---------------------------------------------------------.

// @param[in] canvas               描画領域.
// @param[in] lightAngleListA      角度のリスト (垂直).
// @param[in] lightAngleListB      角度のリスト (水平).
// @param[in] lightIntensityList   光度のリスト (垂直 * 水平).
var DrawLightDistributionCurve = function(canvas, lightAngleListA, lightAngleListB, lightIntensityList) {
    this.canvas = canvas;
    this.lightAngleListA    = lightAngleListA;
    this.lightAngleListB    = lightAngleListB;
    this.lightIntensityList = lightIntensityList;

    this.lampLuminousFlux = 1000.0;             // ランプ光束.
    this.luminousIntensityScale = 1.0;          // 光度にかける倍率。通常は1.0.
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
        var maxR0 = parseFloat(width) * 0.5;
        var maxR = parseFloat(width) * 0.45;
        var rD = maxR / parseFloat(circleCou);
        var r = rD;
        for (var i = 1; i <= circleCou; ++i) {
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
            var dx = dxS * maxR0;
            var dy = dyS * maxR0;
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

        // cd/klm にする.
        var sV = (scope.lampLuminousFlux / scope.luminousIntensityScale) / 1000.0;

        // 曲線を描画.
        {
            var maxAngle = scope.lightAngleListA[scope.lightAngleListA.length - 1];

            // 明るさは、光度値 * 1000.0 / (ランプ光束) で計算できる.
            if (maxAngle <= 90.0 && scope.lightAngleListB.length == 1) {
                // 左右対称の場合.
                for (var loop = 0; loop < 2; ++loop) {
                    context.beginPath();
                    context.strokeStyle = blackCol;
                    context.lineWidth = 1.0;
                    var lCou = scope.lightAngleListA.length;
                    for (var i = 0; i < lCou; ++i) {
                        var angleV = scope.lightAngleListA[i];
                        var dV = (angleV - 90.0) * Math.PI / 180.0;
                        var dxS = Math.cos(dV);
                        var dyS = Math.sin(dV);
                        if (loop == 1) dxS = -dxS;
                        var v = (scope.lightIntensityList[i] / sV) * maxR / scope.maxLuminousIntensity;
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
            } else {
                // 180度反映の場合.
                context.beginPath();
                context.strokeStyle = "#e07070";
                context.lineWidth = 1.0;
                var lCou = scope.lightAngleListA.length;

                // 水平角度で90.0度回転したものを描画.
                {
                    // 0 ~ +180 へ反映.
                    var hPos1 = 0;
                    for (var i = 0; i < scope.lightAngleListB.length; ++i) {
                        if (Math.abs(scope.lightAngleListB[i] - 90.0) < 0.01) {
                            hPos1 = i;
                            break;
                        }
                    }

                    var iPos1 = hPos1 * lCou;
                    {
                        for (var i = 0; i < lCou; ++i) {
                            var angleV = scope.lightAngleListA[i];
                            var dV = (angleV - 90.0) * Math.PI / 180.0;
                            var dxS = Math.cos(dV);
                            var dyS = Math.sin(dV);
            
                            var v = scope.lightIntensityList[i + iPos1];
                            v = v / sV;
                            v = v * maxR / scope.maxLuminousIntensity;
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

                    // 0 ~ -180 へ反映.
                    {
                        var iPos2 = (scope.lightAngleListB.length - 1 - hPos1) * lCou;
                        for (var i = 0; i < lCou; ++i) {
                            var angleV = scope.lightAngleListA[i];
                            var dV = (-90.0 - angleV) * Math.PI / 180.0;
                            var dxS = Math.cos(dV);
                            var dyS = Math.sin(dV);
            
                            var v = scope.lightIntensityList[i + iPos2];
                            v = v / sV;
                            v = v * maxR / scope.maxLuminousIntensity;
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

                context.beginPath();
                context.lineWidth = 1.0;
                context.strokeStyle = blackCol;

                // 0 ~ +180 へ反映.
                {
                    var hPos1 = 0;
                    var iPos1 = hPos1 * lCou;
                    for (var i = 0; i < lCou; ++i) {
                        var angleV = scope.lightAngleListA[i];
                        var dV = (angleV - 90.0) * Math.PI / 180.0;
                        var dxS = Math.cos(dV);
                        var dyS = Math.sin(dV);
        
                        var v = scope.lightIntensityList[i + iPos1];
                        v = v / sV;
                        v = v * maxR / scope.maxLuminousIntensity;
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

                // 0 ~ -180 へ反映.
                {
                    var iPos2 = (scope.lightAngleListB.length - 1 - hPos1) * lCou;
                    for (var i = 0; i < lCou; ++i) {
                        var angleV = scope.lightAngleListA[i];
                        var dV = (-90.0 - angleV) * Math.PI / 180.0;
                        var dxS = Math.cos(dV);
                        var dyS = Math.sin(dV);
        
                        var v = scope.lightIntensityList[i + iPos2];
                        v = v / sV;
                        v = v * maxR / scope.maxLuminousIntensity;
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
        }

        // 光度値を描画.
        {
            context.font = "8pt Arial";
            context.fillStyle = '#606060';
            context.textAlign = "center";
            //context.textBaseline = "alphabetic";        // デフォルト.
            context.textBaseline = "top";

            var angleV = 0.0;
            var dV = (angleV - 90.0) * Math.PI / 180.0;
            var dxS = Math.cos(dV);
            var dyS = Math.sin(dV);
            
            var dCou = 5;
            var maxI = scope.maxLuminousIntensity;
            var dI = maxI / parseFloat(dCou);
            var curI = dI;
            for (var i = 1; i <= dCou; ++i) {
                var v = curI * maxR / scope.maxLuminousIntensity;
                var dx = dxS * v;
                var dy = dyS * v;

                var cVal = parseInt(curI).toString();
                if (i == dCou) cVal += " (cd)";
                context.fillText(cVal, centerX + dx , centerY - dy - 8.0);
            
                curI += dI;
            }
        }

        // 角度値を描画.
        {
            context.font = "8pt Arial";
            context.fillStyle = '#606060';
            context.textAlign = "center";
            context.textBaseline = "top";

            var dist = parseFloat(width) * 0.46;
            for (var angleV = 0.0; angleV <= 180.0; angleV += 30.0) {
                var dV = (angleV - 90.0) * Math.PI / 180.0;
                var dxS = Math.cos(dV);
                var dyS = Math.sin(dV);
                var dx = dxS * dist;
                var dy = dyS * dist;
                var cVal = parseInt(angleV).toString() + "°";
                context.fillText(cVal, centerX + dx , centerY - dy);

                if (Math.abs(angleV - 0.0) > 0.001 && Math.abs(angleV - 180.0) > 0.001) {
                    context.fillText(cVal, centerX - dx , centerY - dy);
                }
            }
        }
        
        // ランプ光束と倍率を描画.
        {
            context.font = "8pt Arial";
            context.fillStyle = '#000000';
            context.textAlign = "left";
            context.textBaseline = "top";

            var strV = "ランプ光束 : " + scope.lampLuminousFlux.toString() + " lm";
            context.fillText(strV, 4, 4);

            // 最大光度を取得.
            var maxL = LightIntensityUtil.getMaxIntensity(scope.lightIntensityList, false, 1.0 / sV);
            if (maxL > 0.0) {
                strV = "最大光度 : " + StringUtil.getFloatToString(maxL, 2) + " cd/klm";
                context.fillText(strV, 4, 20);
            }

            //strV = "光度倍率 : x " + scope.luminousIntensityScale.toString();
            //context.fillText(strV, 4, 4 + 12);
        }
    };
};

