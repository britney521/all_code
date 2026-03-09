const {sm2,sm3} = require('sm-crypto');

const pub_hex = '04b3730c43da6b6d2b9d9e054b29cb6cdb362aca8a4dd9f7f9860322639a4c76c27949371c73dae23d343e8e8872723ba31d29df3949a62e39c970b078faab001a';

const priv_hex = "5f2ab37fe5648b70df4590def4fe05a21af47d23f876516a3d7a8dd1d271e17e";

// ------------------ SM2 加密（返回 hex） ------------------
function sm2_encrypt(plaintext) {
    return sm2.doEncrypt(plaintext, pub_hex, {
        mode: 1,       // C1C3C2 (与 gmssl 完美兼容)
        output: 'hex'  // 输出 hex
    });
}


// ------------------ SM2 解密（输入 hex） ------------------
function sm2_decrypt(cipher_hex) {
    return sm2.doDecrypt(cipher_hex, priv_hex, {
        mode: 1,         // C1C3C2
        output: 'utf8'   // 输出 UTF-8 明文
    });
}
function a(t) {
            return t.map((function(t) {
                return t = t.toString(16),
                1 === t.length ? "0" + t : t
            }
            )).join("")
        }

function get_signdata(t, e) {
            if (t = "string" === typeof t ? function(t) {
                for (var e = [], n = 0, i = t.length; n < i; n++) {
                    var r = t.codePointAt(n);
                    if (r <= 127)
                        e.push(r);
                    else if (r <= 2047)
                        e.push(192 | r >>> 6),
                        e.push(128 | 63 & r);
                    else if (r <= 55295 || r >= 57344 && r <= 65535)
                        e.push(224 | r >>> 12),
                        e.push(128 | r >>> 6 & 63),
                        e.push(128 | 63 & r);
                    else {
                        if (!(r >= 65536 && r <= 1114111))
                            throw e.push(r),
                            new Error("input is not supported");
                        n++,
                        e.push(240 | r >>> 18 & 28),
                        e.push(128 | r >>> 12 & 63),
                        e.push(128 | r >>> 6 & 63),
                        e.push(128 | 63 & r)
                    }
                }
                return e
            }(t) : Array.prototype.slice.call(t),
            e) {
                var n = e.mode || "hmac";
                if ("hmac" !== n)
                    throw new Error("invalid mode");
                var i = e.key;
                if (!i)
                    throw new Error("invalid key");
                return i = "string" === typeof i ? s(i) : Array.prototype.slice.call(i),
                a(o(t, i))
            }

            return sm3(t)
        }

// 加密
function get_endata(i) {
    // var UNICDOE = (1e6 * Math.random() + "" + (new Date).getMilliseconds()).replace(".", "")

    const cipher_hex = sm2_encrypt(JSON.stringify(i));
    const hash = get_signdata(JSON.stringify(i));
    return {
        encData:"04"+cipher_hex,
        signData:hash,
    }
}


// 解密
function get_data(data) {
    const plain = sm2_decrypt(data);
    // console.log("Recovered:", plain);
    return JSON.parse(plain)
}



