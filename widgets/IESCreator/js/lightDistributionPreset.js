//---------------------------------------------------------.
// プリセット情報を指定.
// presetType ... 0 : 点光源、1 : スポットライト、2 : ランダム/対称、 3 : ランダム/非対称.
//---------------------------------------------------------.

var LightDistributionPreset = function(presetType) {
    this.presetType = presetType;
    this.lightAngleA        = null;         // 垂直角度のArray.
    this.lightAngleB        = null;         // 水平角度のArray.
    this.lightIntensityList = null;         // 光度のArray (垂直角度 * 水平角度).

    var scope = this;

    // 垂直角度のArrayを取得.
    this.getLightAngleA = function () {
        return scope.lightAngleA;
    };

    // 水平角度のArrayを取得.
    this.getLightAngleB = function () {
        return scope.lightAngleB;
    };

    // 光度のArrayを取得.
    this.getLightIntensityList = function () {
        return scope.lightIntensityList;
    };

    // プリセットの指定.
    this.doPreset = function (presetType) {
        var maxV = 200.0;

        if (presetType == 0) {    // 点光源の表現.
            var cou = 180;
            scope.lightAngleA        = new Array(cou + 1);
            scope.lightIntensityList = new Array(cou + 1);
            var pos = 0.0;
            var dV = 1.0 / parseFloat(cou);
            for (var i = 0; i <= cou; i++) {
                scope.lightAngleA[i] = parseFloat(i);
                scope.lightIntensityList[i] = 79.5774;	//100.0;
                pos += dV;
            }

            // 水平角度の値.
            scope.lightAngleB = new Array(1);
            scope.lightAngleB[0] = 0.0;
            return;
        }

        if (presetType == 1) {      // スポットライトの表現.
            var angleV  = 120;      // スポットライトの角度.
            var angleVH = angleV / 2;
            var softnessMargin = 5;

            var cou = 90;
            scope.lightAngleA        = new Array(cou + 1);
            scope.lightIntensityList = new Array(cou + 1);
            var pos = 0.0;
            var dV = 1.0 / parseFloat(cou);
            for (var i = 0; i <= cou; i++) {
                scope.lightAngleA[i] = parseFloat(i);
                var iV = 79.5774;
                if (i > angleVH && i < angleVH + softnessMargin) {
                    iV *= 1.0 - parseFloat(i - angleVH) / parseFloat(softnessMargin);
                } else if (i >= angleVH + softnessMargin) {
                    iV = 0.0;
                }
                scope.lightIntensityList[i] = iV;
                pos += dV;
            }

            // 水平角度の値.
            scope.lightAngleB = new Array(1);
            scope.lightAngleB[0] = 0.0;
        }

        if (presetType == 2) {      // ランダム/軸対称.
            var cou = 90;
            scope.lightAngleA        = new Array(cou + 1);
            scope.lightIntensityList = new Array(cou + 1);
            var pos = 0.0;
            var dV = 1.0 / parseFloat(cou);
            for (var i = 0; i <= cou; i++) {
                var p = (1.0 - Math.pow(pos, 1.2));     // 1.6
                scope.lightAngleA[i] = parseFloat(i);
                scope.lightIntensityList[i] = p * maxV;
                pos += dV;
            }

            // ランダムに揺らす.
            var vD = 800.0 / parseFloat(cou);
            var vP = 0.0;
            for (var i = 0; i < cou; ++i) {
                var v2 = Math.sin(vP * Math.PI / 180.0);
                v2 = (1.0 + v2) * 0.1;  // 0.5
                scope.lightIntensityList[i] = Math.max(0.0, scope.lightIntensityList[i] - v2 * maxV * 0.2);
                vP += vD;
            }

            // 水平角度の値.
            scope.lightAngleB = new Array(1);
            scope.lightAngleB[0] = 0.0;
        }

        if (presetType == 3) {      // ランダム/軸非対称/複数断面を持つ.
            var cou = 45;
            var dmCou = 8;
            scope.lightAngleA        = new Array(cou + 1);
            scope.lightAngleB        = new Array(dmCou + 1);
            scope.lightIntensityList = new Array((cou + 1) * (dmCou + 1));

            // 水平角度の指定.
            {
                var vP = 0.0;
                var vD = 180.0 / parseFloat(dmCou);
                for (var i = 0; i <= dmCou; i++) {
                    scope.lightAngleB[i] = vP;
                    vP += vD;
                }
            }

            // 垂直角度の指定.
            {
                var vP = 0.0;
                var vD = 180.0 / parseFloat(cou);
                for (var i = 0; i <= cou; i++) {
                    scope.lightAngleA[i] = vP;
                    vP += vD;
                }
            }

            // 光度の指定.
            {
                var iPos = 0;
                for (var loop = 0; loop <= dmCou; ++loop) {
                    var pos = 0.0;
                    var dV = 1.0 / (parseFloat(cou) * 0.7);
                    var scaleV = 1.0;
                    var angleV = 0.0;
                    var vR = (Math.random() * 5.0) + 2.0;
                    var angleD = 360.0 * vR / parseFloat(cou);
                    for (var i = 0; i <= cou; i++) {
                        var p = (1.0 - Math.pow(pos, 1.6));
                        var v2 = Math.sin(angleV * Math.PI / 180.0);
                        var scaleV2 = 1.0 - Math.pow(1.0 - scaleV, 2.0);
                        scope.lightIntensityList[i + iPos] = (p * 0.9 + v2 * 0.1) * maxV * scaleV2;
                        pos += dV;
                        scaleV = Math.max(0.0, scaleV - dV);
                        angleV += angleD;
                    }

                    iPos += cou + 1;
                }
            }
        }
    };

    // 最大光度を取得.
    this.getMaxLuminousIntensity = function () {
        var maxV = 100.0;
        var lCou = scope.lightIntensityList.length;
        if (lCou == 0) return maxV;

        maxV = 0.0;
        for (var i = 0; i < lCou; ++i) {
            var v = scope.lightIntensityList[i];
            maxV = Math.max(v, maxV);
        }

        // 区切りのいい数値にする.
        if (maxV <= 100.0) {
            var vA = [0.0, 20.0, 40.0, 50.0, 60.0, 80.0, 100.0];
            for (var i = 0; i < vA.length - 1; ++i) {
                if (maxV >= vA[i] && maxV <= vA[i+1]) {
                    maxV = vA[i+1];
                    break;
                }
            }
            return maxV;
        }
        if (maxV <= 1000.0) {
            var vA = [100.0, 200.0, 400.0, 500.0, 600.0, 800.0, 1000.0];
            for (var i = 0; i < vA.length - 1; ++i) {
                if (maxV >= vA[i] && maxV <= vA[i+1]) {
                    maxV = vA[i+1];
                    break;
                }
            }
            return maxV;
        }
        {
            var mI = parseInt(maxV / 1000.0);
            maxV = parseFloat((mI + 1) * 1000);
        }

        return maxV;
    };
};

