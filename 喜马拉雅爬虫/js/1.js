
//  n = t[0]
//               , o = t[1]
//               , a = "".concat(o, "&&").concat(n);
var CryptoJS = require('crypto-js');
const pako = require('pako');

function _0x1ebaf8(_0x58e5cb) {
    var _0x56b073 = String(_0x58e5cb)
        , _0x3cff00 = _0x56b073["length"];
    if (!_0x3cff00)
        return _0x56b073;
    let _0x455bc4 = ''
        , _0x3847b7 = 0;
    for (; _0x3847b7 < _0x3cff00;) {
        let _0x3bcb1a = _0x56b073[_0x3847b7];
        if ('%' === _0x3bcb1a) {
            let _0x1a9fb5 = _0x3847b7 <= _0x3cff00 - 6 && 'u' === _0x56b073[_0x3847b7 + 1] ? _0x56b073["substring"](_0x3847b7 + 2, _0x3847b7 + 6) : _0x3847b7 <= _0x3cff00 - 3 ? _0x56b073["substring"](_0x3847b7 + 1, _0x3847b7 + 3) : '';
            4 === (_0x1a9fb5 = new RegExp("$+]F-A9-0[^".split("").reverse().join(""), 'i')["test"](_0x1a9fb5) ? _0x1a9fb5 : '')["length"] ? (_0x3bcb1a = String["fromCharCode"](parseInt(_0x1a9fb5, 16)),
                _0x3847b7 += 5) : 2 === _0x1a9fb5["length"] && (_0x3bcb1a = String["fromCharCode"](parseInt("00".split("").reverse().join("") + _0x1a9fb5, 16)),
                _0x3847b7 += 2);
        }
        _0x455bc4 += _0x3bcb1a,
            _0x3847b7 += 1;
    }
    return _0x455bc4;
}

function _stringToUint8Array(_0x70bf08) {

    for (var _0x4c9438 = _0x1ebaf8(encodeURIComponent(_0x70bf08))["split"](''), _0x688257 = [], _0x402a7f = 0; _0x402a7f < _0x4c9438["length"]; _0x402a7f++)
        _0x688257["push"](_0x4c9438[_0x402a7f]["charCodeAt"](0));
    return new Uint8Array(_0x688257);

}

function compress(_0x383a33) {
    return pako["deflate"](_0x383a33, {
        'level': 0x6
    });
}

function aesEncrypt(_0x1a4a6f, _0x292fa3) {

    var _0x29b5e5 = CryptoJS["enc"]["Utf8"]["parse"](_0x292fa3);
    return CryptoJS["AES"]["encrypt"](_0x1a4a6f, _0x29b5e5, {
        'iv': _0x29b5e5,
        'mode': CryptoJS["mode"]["ECB"],
        'padding': CryptoJS["pad"]["Pkcs7"]
    })["toString"]();

}

function aesDecrypt(cipherB64, password) {
    try {
        // 1. 密码 → WordArray（与加密保持一致）
        const keyIv = CryptoJS.enc.Utf8.parse(password);

        // 2. 解密参数
        const decryptedWA = CryptoJS.AES.decrypt(cipherB64, keyIv, {
            iv: keyIv,
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        });

        // 3. WordArray → UTF-8 字符串
        return decryptedWA.toString(CryptoJS.enc.Utf8);
    } catch (e) {
        console.error('AES 解密失败:', e);
        return null;
    }
}

function base64ToArrayBuffer(_0x5cf3f5) {
    for (var _0x2ca832 = atob(_0x5cf3f5), _0x316c2f = _0x2ca832["length"], _0x2e5d83 = new Uint8Array(_0x316c2f), _0x535814 = 0; _0x535814 < _0x316c2f; _0x535814++)
        _0x2e5d83[_0x535814] = _0x2ca832["charCodeAt"](_0x535814);
    return _0x2e5d83["buffer"];
}

/* ====== 3. 主入口（等价于 this["_getProcessData"]） ====== */
function getProcessData(obj, password) {

    // 1. 对象 -> JSON -> Uint8Array
    const jsonStr = JSON.stringify(obj);
    const u8 = _stringToUint8Array(jsonStr);

    // 2. 压缩
    const compressed = compress(u8);

    // 3. 转成 CryptoJS WordArray
    const wa = CryptoJS.lib.WordArray.create(compressed);

    // 4. AES 加密 -> Base64
    const b64 = aesEncrypt(wa, password);

    // 5. Base64 -> ArrayBuffer
    // return base64ToArrayBuffer(b64);
    return b64;

}



var key = "m9ZtRrz:qujT8@da";

function get_dr2() {
            var _0x7f512b = _0x2cb62a;
            try {
                ({
                    'start': function() {},
                    'stop': function() {}
                })["start"]();
                var _0x589744 = window;
                let _0x41ced9 = Object["getOwnPropertyNames"](_0x589744)["filter"](_0x2c82af=>!new RegExp('_|\x5cd{3,}','')["test"](_0x2c82af));
                var _0x4336b4, _0x26549c = new RegExp('Gecko\x5c/','')["test"](navigator["userAgent"]), _0x51c97b = "Event", _0x523ea8 = ["PerformanceNavigationTiming", "Performance"], _0x41338b = (_0x26549c && (-1 != (_0x4336b4 = _0x41ced9["indexOf"](_0x51c97b)) && (_0x41ced9 = [...(_0x41ced9 = _0x41ced9["slice"](0, _0x4336b4)["concat"](_0x41ced9["slice"](_0x4336b4 + 1))), _0x51c97b]),
                _0x523ea8["forEach"](_0x114efe=>{
                    var _0x5557df = _0x7f512b
                      , _0x114efe = _0x41ced9["indexOf"](_0x114efe);
                    -1 != _0x114efe && _0x41ced9["splice"](_0x114efe, 1);
                }
                )),
                _0x41ced9["filter"](_0x3bca15=>new RegExp("zom".split("").reverse().join(""),'i')["test"](_0x3bca15))["length"]), _0x317a95 = _0x41ced9["filter"](_0x28e001=>new RegExp('webkit','i')["test"](_0x28e001))["length"], _0x4d4f55 = _0x41ced9["filter"](_0x2af24e=>new RegExp('apple','i')["test"](_0x2af24e))["length"], _0x5c8b9b = {
                    'keys': _0x41ced9,
                    'apple': _0x4d4f55,
                    'moz': _0x41338b,
                    'webkit': _0x317a95
                }, _0x5d0990 = JSON["stringify"](_0x5c8b9b);
                return _0x59e56f["md5"](_0x5d0990);
            } catch (_0x2bf1b9) {
                return '';
            }
        }

        // Tw1 lL1 sV5 GJ2 Dr2 MB8 ZH2 nE4 dV4
function get_buffer(timestr,uid) {
    const data = {
    "Zf5": timestr,
    "GF9": "2.0.0",
    "HW5": "t6pfoml9679z52kqw93uqu75eflqdg1bykhl",
    "ew1": {
        "Wg7": "Mozilla",
        "lV1": "Google Inc.",
        "Xt4": "Netscape",
        "yV2": "5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "KY1": "MacIntel",
        "Le3": "Tmxhcm9vei81LjAgKE56eHJtZ2xoczsgUm1ndm8gTnp4IExIIEMgMTBfMTVfNykgWmtrb3ZEdnlQcmcvNTM3LjM2IChQU0dOTywgb3JwdiBUdnhwbCkgWHNpbG52LzEyOC4wLjAuMCBIenV6aXIvNTM3LjM2",
        "kH1": 978,
        "ad5": 1920,
        "Ua9": 24,
        "TQ6": 1080,
        "kC7": 1920,
        "me8": 24,
        "eY9": true,
        "Kn2": false,
        "OM3": true,
        "sw8": false,
        "uW3": -1,
        "iO8": "https://www.ximalaya.com/album/"+uid,
        "By1": "www.ximalaya.com",
        "Gv4": "/album/"+uid,
        "ef2": "",
        "tZ2": "https:",
        "OG4": true,
        "kx1": true,
        "VD6": true,
        "Ov6": false,
        "lq3": "zh-CN",
        "ef5": [
            "zh-CN",
            "zh"
        ],
        "OK3": 2,
        "Fg5": true,
        "qS2": [
            1920,
            975,
            1869,
            898
        ],
        "Fc5": "light"
    },
    "HK3": {
        "iI1": {
            "NF1": -1,
            "cA1": -1,
            "NK5": -1,
            "VP4": "-1.00",
            "RX5": -1,
            "VP6": -1,
            "tJ4": -1
        },
        "ti4": {
            "xm9": true,
            "is3": 1
        },
        "AV9": 12,
        "aK8": "Google Inc. (Apple)",
        "df6": "ANGLE (Apple, ANGLE Metal Renderer: Apple M4 Pro, Unspecified Version)",
        "WB9": "UxZFXBRABkdAARcSUhRDVkBGB0NHUxBCABMQAUwSXRM",
        "pD7": "AEFCAE0QAExLAkVDBkdDUBBKXEVDXUxLARYVXEFBUxA",
        "da2": "VUdHSkVHV0FFUkVEVURHU0RB",
        "dt2": 8,
        "Sy6": -480,
        "MS3": "Asia/Shanghai",
        "pi9": false,
        "Ao1": [],
        "BH5": 0,
        "UG4": [
            "Andale Mono",
            "Arial",
            "Arial Black",
            "Arial Hebrew",
            "Arial Narrow",
            "Arial Rounded MT Bold",
            "Arial Unicode MS",
            "Comic Sans MS",
            "Courier",
            "Courier New",
            "Geneva",
            "Georgia",
            "Helvetica",
            "Helvetica Neue",
            "Impact",
            "LUCIDA GRANDE",
            "Microsoft Sans Serif",
            "Monaco",
            "Palatino",
            "Tahoma",
            "Times",
            "Times New Roman",
            "Trebuchet MS",
            "Verdana",
            "Wingdings",
            "Wingdings 2",
            "Wingdings 3"
        ]
    },
    "fc9": {
        "cx4": "4g",
        "zY8": -1,
        "yj6": 10,
        "dV4": 250,
        "yX4": false
    },
    "pX4": "7A9231:C4BA41:324E2A:f700",
    "Ud2": "D2U9qkIfZDRb6kI0MdFy/2ME2YDNkmugkYSmw2YoM5OggXa5",
    "Cb7": null,
    "Gp5": null,
    "Zn6": {
        "oe2": "0",
        "EV9": "true",
        "xu2": "1441A790E638FC63C1A16A093AA064090F07505CB569A950EF3E5E646CD1A0B3",
        "CY8": "",
        "nE4": 386956,
        "Tw1": [
            532.6999999880791,
            387453.6999999881
        ],
        "Sb1": false
    },
    "lL1": "7d423e13b26c612ad38d64d6a55ea1af",
    "uT8": "-1",
    "sV5": 1,
    "Vo6": "",
    "hi9": 0,
    "fd2": {
        "Pf5": 1756633864988,
        "Ja5": "7A9231:C4BA41:324E2A:f700",
        "xz7": "1b1314e3-82f1-42ac-2ae2-bfff96a40747",
        "av1": "D2U9qkIfZDRb6kI0MdFy/2ME2YDNkmugkYSmw2YoM5OggXa5",
        "cp9": 302
    },
    "ck9": "h5_goyxvzyohd",
    "uS7": "",
    "jm9": 2,
    "GJ2": "f9ef3959-f9a7-44de-bd33-8a495c58149d-fcs011",
    "MT7": "33-00000-0000-1111111-000000-0011-000000-0000-00000-0",
    "BG5": false,
    "Fd8": "2",
    "Dr2": "NjUydTQ2MnU0NDg2dXU2MHl6Nzg0dTA5N3U5enczNHc",
    "lp7": "OTl6NDE3ODM5MDUydjd6MzY1eDd5eTQ5eDkzdzAweDM",
    "iq7": false,
    "MB8": "IOB0m2cgyY",
    "ZH2": "PPMqb0ILky",
    "DP5": "1441A7909C087DBBE7CE59881B9DF8B9"
};
    const buf = getProcessData(data, key);
    return buf
}


function generate() {
    _0x6c56f3 = Date["now"]();
    return (_0x6c56f3 += performance['now']()),
        "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"['replace'](new RegExp("\u005b\u0078\u0079\u005d", "\u0067"), function (_0x28a9b4) {
            var _0x5b4a44 = (_0x6c56f3 + (0x1b717 ^ 0x1b707) * Math['random']()) % (0xe7f76 ^ 0xe7f66) | 0xe63e7 ^ 0xe63e7;
            return _0x6c56f3 = Math['floor'](_0x6c56f3 / (0x7c559 ^ 0x7c549)),
                ("\u0078" === _0x28a9b4 ? _0x5b4a44 : (0x3696e ^ 0x3696d) & _0x5b4a44 | 0x23319 ^ 0x23311)['toString'](0x7b7fc ^ 0x7b7ec);
        });
}


