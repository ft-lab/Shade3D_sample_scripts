//---------------------------------------------------------.
// 光源の明るさ処理のユーティリティ関数.
//---------------------------------------------------------.

var LightIntensityUtil = {};
LightIntensityUtil.name = "LightIntensityUtil";

// リスト内の明るさ値の最大を取得.
// [in] intensityList  明るさの配列.
// [in] wellDefined    区切りのいい値にする場合はtrue.
// [in] scaleV         倍率.
LightIntensityUtil.getMaxIntensity = function (intensityList, wellDefined, scaleV) {
    var maxV = 100.0;
    var lCou = intensityList.length;
    
    if (lCou == 0) {
        if (wellDefined) return maxV;
        return 0.0;
    }

    maxV = 0.0;
    for (var i = 0; i < lCou; ++i) {
        var v = intensityList[i] * scaleV;
        maxV = Math.max(v, maxV);
    }
    if (!wellDefined) return maxV;

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
        var mI = parseInt(maxV / 50.0);
        maxV = parseFloat((mI + 1) * 50);
/*
        var vA = [100.0, 200.0, 400.0, 500.0, 600.0, 800.0, 1000.0];
        for (var i = 0; i < vA.length - 1; ++i) {
            if (maxV >= vA[i] && maxV <= vA[i+1]) {
                maxV = vA[i+1];
                break;
            }
        }
*/
        return maxV;
    }
    {
        var mI = parseInt(maxV / 200.0);
        maxV = parseFloat((mI + 1) * 200);
    }

    return maxV;
};

