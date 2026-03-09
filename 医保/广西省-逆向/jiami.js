var e = '04b3730c43da6b6d2b9d9e054b29cb6cdb362aca8a4dd9f7f9860322639a4c76c27949371c73dae23d343e8e8872723ba31d29df3949a62e39c970b078faab001a'
var i = {
    "appId": "rI6eAOjuVeaTqto9",
    "data": {
        "where": {
            "admdvs": "4502",
            "drugType": null,
            "regName": null,
            "longitude": "",
            "latitude": ""
        },
        "sort": [
            [
                "drugSale",
                "desc"
            ]
        ],
        "pageNum": 3,
        "pageSize": 10,
        "uniqueCode": "8115540538248436160"
    },
    "timestamp": 1763170444161,
    "version": "1.0.0"
}

var a = "04" + n.sm2.doEncrypt(JSON.stringify(i), e.toLowerCase(), 1)

var t = function(e) {
    return n.sm3(JSON.stringify(e))
}(i)
data = {
    encData: a,    // 加密后的数据
    signData: t    // 签名数据
}

console.log(data)

