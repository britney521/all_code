const CryptoJS = require("crypto-js");
const JSEncrypt = require('jsencrypt');

i = {
    "clientId": "6efca3ef-056f-4c56-8a45-02af1ba79150",
    "aesKey": "pktAYvVq7p0eGQWE",
    "rsaEncryptAesKey": "VVnpdqDHQBdrQLYFtM7IaxL7lKe0cZRNa5sTrcXkhQZbwDNZGBSqxDRgT0+q1B49GoYyZDAV6aLlE5qRqdVBUuLJbDxcgymRHkDp6yezu+Hvs3+d+DsUaQTR09JTTMS5ZcjRipIBHYPIU29B7OkqXyTqtwt8jSHWA+LyaVAThL0iTsFiHDrv39fhOprb0zeY8p6Dd6yVdbJlvU04XtXkOVenR4hgRAcZfHE6HUwqompQ9cIBRZNye6EZgqvZMhOJtn16bcLhYF7SdDCF7/3ce6JodkwYfL+xtmFQFRhyhjI/MuY0YkLShM6HQQQPOyeRcLfoN8/gZfnBiGzwvqGlOA=="
}
// word = {
//     "code": "YBDRUG001",
//     "identity": "",
//     "departId": "",
//     "purpose": "1",
//     "qdlybz": "17",
//     "admdvsL": "310000",
//     "reqData": [
//         {
//             "drugName": "",
//             "saleSortFlag": "",
//             "pageSize": 5,
//             "pageNum": 4
//         }
//     ]
// }

function genKey() {
    for (var t = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : 16, e = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", r = "", i = 0; i < t; i++)
        r += e.charAt(Math.random() * e.length);
    return r
}

function encrypt(word, keyStr) {
    // 1. 如果传入的是对象，先转为 JSON 字符串
    if (word instanceof Object) {
        word = JSON.stringify(word);
    }

    // 2. 将内容和密钥解析为 UTF-8 格式
    const srcs = CryptoJS.enc.Utf8.parse(word);
    const key = CryptoJS.enc.Utf8.parse(keyStr);

    // 3. 执行 AES 加密
    const encrypted = CryptoJS.AES.encrypt(srcs, key, {
        mode: CryptoJS.mode.ECB,     // 对应 n.default.mode.ECB
        padding: CryptoJS.pad.Pkcs7  // 对应 n.default.pad.Pkcs7
    });

    // 4. 返回字符串 (CryptoJS 默认返回 Base64 格式的字符串)
    return encrypted.toString();
}

function decrypt(t, e) {
    // 1. 解析密钥 (对应 n.default.enc.Utf8.parse(e))
    const key = CryptoJS.enc.Utf8.parse(e);

    // 2. AES 解密 (对应 n.default.AES.decrypt)
    const r = CryptoJS.AES.decrypt(t, key, {
        mode: CryptoJS.mode.ECB,    // 对应 n.default.mode.ECB
        padding: CryptoJS.pad.Pkcs7 // 对应 n.default.pad.Pkcs7
    });

    // 3. 将解密后的 WordArray 转为 UTF-8 字符串
    // 对应 n.default.enc.Utf8.stringify(r).toString()
    // 注意：CryptoJS.enc.Utf8.stringify(r) 得到的就是 string，后面的 .toString() 其实是多余的，但为了还原逻辑保留
    let i = CryptoJS.enc.Utf8.stringify(r).toString();

    // 4. JSON 解析逻辑 (完全还原源码逻辑)
    // 源码逻辑："{" !== i.charAt(0) && "[" !== i.charAt(0) || (i = JSON.parse(i))
    // 解释：如果字符串以 '{' 或者 '[' 开头，就执行 JSON.parse
    try {
        if (i.charAt(0) === '{' || i.charAt(0) === '[') {
            i = JSON.parse(i);
        }
    } catch (err) {
        // 原代码没有 try-catch，但在实际开发中，如果解密出来的字符串看起来像JSON但格式不对，
        // JSON.parse 会报错导致程序崩溃。建议加上 try-catch。
        console.warn("JSON解析失败，返回原字符串", err);
    }

    return i;
}


// 假设你已经引入了 JSEncrypt 库
// 或者是网站本身就有 JSEncrypt 对象

function rsaEncrypt(content, publicKey) {
    // 1. 创建加密对象实例
    var encryptor = new JSEncrypt();

    // 2. 设置公钥
    // JSEncrypt 非常智能，通常能处理带头/不带头的 PEM 格式
    encryptor.setPublicKey(publicKey);

    // 3. 加密
    // 返回的结果通常已经是 Base64 编码的字符串
    var encrypted = encryptor.encrypt(content);

    return encrypted;
}

// --- 测试 ---

function get_rsaEncryptAesKey(aesKey,Key){
    // 这里的公钥就是你从网页 JS 里找到的那串
var pubKey = `-----BEGIN PUBLIC KEY-----
${Key}
-----END PUBLIC KEY-----`;

var result = rsaEncrypt(aesKey, pubKey);

console.log("加密结果:", result);
return result
// 结果类似于: "N1p3/..."
}

//
// console.log(get_rsaEncryptAesKey('rMAisR4mzzUp9IpO'))