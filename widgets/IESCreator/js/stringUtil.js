//---------------------------------------------------------.
// 文字列処理関数.
//---------------------------------------------------------.

var StringUtil = {};
StringUtil.name = "StringUtil";

// 小数点の指定ケタ数までを文字列化.
StringUtil.getFloatToString = function (fVal, sCou) {
    if (sCou == 0) {
        return parseInt(fVal).toString();
    }
    var scale = Math.pow(10.0, sCou);
    fI = parseInt(fVal * scale);
    var fVal2 = parseFloat(fI) / scale; 
    return fVal2.toString();
};

