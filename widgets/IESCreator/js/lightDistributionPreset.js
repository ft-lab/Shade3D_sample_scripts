//---------------------------------------------------------.
// プリセット情報を指定.
// presetType ... 0 : 点光源、1 : スポットライト、2 : ランダム/対称、 3 : ランダム/非対称.
//---------------------------------------------------------.

var LightDistributionPreset = function(presetType) {
    this.presetType = presetType;
    this.lightAngleA        = null;         // 垂直角度のArray.
    this.lightAngleB        = null;         // 水平角度のArray.
    this.lightIntensityList = null;         // 光度のArray (垂直角度 * 水平角度).
};

// 垂直角度のArrayを取得.
LightDistributionPreset.prototype.getLightAngleA = function () {
    return this.lightAngleA;
};

// 水平角度のArrayを取得.
LightDistributionPreset.prototype.getLightAngleB = function () {
    return this.lightAngleB;
};

// 光度のArrayを取得.
LightDistributionPreset.prototype.getLightIntensityList = function () {
    return this.lightIntensityList;
};

// プリセットの指定.
LightDistributionPreset.prototype.doPreset = function (presetType) {
    var maxV = 200.0;

    if (presetType == 0) {    // 点光源の表現.
        var cou = 180;
        this.lightAngleA        = new Array(cou + 1);
        this.lightIntensityList = new Array(cou + 1);
        var pos = 0.0;
        var dV = 1.0 / parseFloat(cou);
        for (var i = 0; i <= cou; i++) {
            this.lightAngleA[i] = parseFloat(i);
            this.lightIntensityList[i] = 79.5774;	//100.0;
            pos += dV;
        }

        // 水平角度の値.
        this.lightAngleB = new Array(1);
        this.lightAngleB[0] = 0.0;
        return;
    }

    if (presetType == 1) {      // スポットライトの表現.
        var angleV  = 120;      // スポットライトの角度.
        var angleVH = angleV / 2;
        var softnessMargin = 5;

        var cou = 90;
        this.lightAngleA        = new Array(cou + 1);
        this.lightIntensityList = new Array(cou + 1);
        var pos = 0.0;
        var dV = 1.0 / parseFloat(cou);
        for (var i = 0; i <= cou; i++) {
            this.lightAngleA[i] = parseFloat(i);
            var iV = 79.5774;
            if (i > angleVH && i < angleVH + softnessMargin) {
                iV *= 1.0 - parseFloat(i - angleVH) / parseFloat(softnessMargin);
            } else if (i >= angleVH + softnessMargin) {
                iV = 0.0;
            }
            this.lightIntensityList[i] = iV;
            pos += dV;
        }

        // 水平角度の値.
        this.lightAngleB = new Array(1);
        this.lightAngleB[0] = 0.0;
    }

    if (presetType == 2) {      // ランダム/軸対称.
        var cou = 90;
        this.lightAngleA        = new Array(cou + 1);
        this.lightIntensityList = new Array(cou + 1);
        var pos = 0.0;
        var dV = 1.0 / parseFloat(cou);
        for (var i = 0; i <= cou; i++) {
            var p = (1.0 - Math.pow(pos, 1.2));     // 1.6
            this.lightAngleA[i] = parseFloat(i);
            this.lightIntensityList[i] = p * maxV;
            pos += dV;
        }

        // ランダムに揺らす.
        var vD = 800.0 / parseFloat(cou);
        var vP = 0.0;
        for (var i = 0; i < cou; ++i) {
            var v2 = Math.sin(vP * Math.PI / 180.0);
            v2 = (1.0 + v2) * 0.1;  // 0.5
            this.lightIntensityList[i] = Math.max(0.0, this.lightIntensityList[i] - v2 * maxV * 0.2);
            vP += vD;
        }

        // 水平角度の値.
        this.lightAngleB = new Array(1);
        this.lightAngleB[0] = 0.0;
    }

    if (presetType == 3) {      // ランダム/軸非対称/複数断面を持つ.
        var cou = 45;
        var dmCou = 8;
        this.lightAngleA        = new Array(cou + 1);
        this.lightAngleB        = new Array(dmCou + 1);
        this.lightIntensityList = new Array((cou + 1) * (dmCou + 1));

        // 水平角度の指定.
        {
            var vP = 0.0;
            var vD = 180.0 / parseFloat(dmCou);
            for (var i = 0; i <= dmCou; i++) {
                this.lightAngleB[i] = vP;
                vP += vD;
            }
        }

        // 垂直角度の指定.
        {
            var vP = 0.0;
            var vD = 180.0 / parseFloat(cou);
            for (var i = 0; i <= cou; i++) {
                this.lightAngleA[i] = vP;
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
                    this.lightIntensityList[i + iPos] = (p * 0.9 + v2 * 0.1) * maxV * scaleV2;
                    pos += dV;
                    scaleV = Math.max(0.0, scaleV - dV);
                    angleV += angleD;
                }

                iPos += cou + 1;
            }
        }
    }
};