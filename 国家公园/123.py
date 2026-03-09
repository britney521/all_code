import requests

cookies = {
    '_RGUID': 'e2f377fe-00eb-409d-93d6-850e179cbfb1',
    '_RSG': 'T2qw0u_TpBEn.BdNuGXMF9',
    '_RDG': '288db3c22bf42e2ab803aa65b90e7b7196',
    'GUID': '09031164116742831658',
    'nfes_isSupportWebP': '1',
    'UBT_VID': '1741495310056.90abroPuCsSe',
    'MKT_CKID': '1741495310505.twf2u.v29p',
    '_RF1': '240e%3A368%3A8bf5%3Afc9d%3Af03b%3A200c%3A38d1%3A4600',
    '_bfaStatusPVSend': '1',
    '_ubtstatus': '%7B%22vid%22%3A%221741495310056.90abroPuCsSe%22%2C%22sid%22%3A7%2C%22pvid%22%3A12%2C%22pid%22%3A0%7D',
    '_bfi': 'p1%3D0%26p2%3D290510%26v1%3D12%26v2%3D3',
    '_bfaStatus': 'success',
    '_bfa': '1.1741495310056.90abroPuCsSe.1.1750483734276.1750484142339.7.13.290510',
    '_jzqco': '%7C%7C%7C%7C1750478360662%7C1.1560283885.1750478360629.1750481495046.1750484142637.1750481495046.1750484142637.0.0.0.4.4',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'cookieorigin': 'https://you.ctrip.com',
    'origin': 'https://you.ctrip.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://you.ctrip.com/',
    'sec-ch-ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
    'x-ctx-ubt-pageid': '290510',
    'x-ctx-ubt-pvid': '13',
    'x-ctx-ubt-sid': '7',
    'x-ctx-ubt-vid': '1741495310056.90abroPuCsSe',
    # 'cookie': '_RGUID=e2f377fe-00eb-409d-93d6-850e179cbfb1; _RSG=T2qw0u_TpBEn.BdNuGXMF9; _RDG=288db3c22bf42e2ab803aa65b90e7b7196; GUID=09031164116742831658; nfes_isSupportWebP=1; UBT_VID=1741495310056.90abroPuCsSe; MKT_CKID=1741495310505.twf2u.v29p; _RF1=240e%3A368%3A8bf5%3Afc9d%3Af03b%3A200c%3A38d1%3A4600; _bfaStatusPVSend=1; _ubtstatus=%7B%22vid%22%3A%221741495310056.90abroPuCsSe%22%2C%22sid%22%3A7%2C%22pvid%22%3A12%2C%22pid%22%3A0%7D; _bfi=p1%3D0%26p2%3D290510%26v1%3D12%26v2%3D3; _bfaStatus=success; _bfa=1.1741495310056.90abroPuCsSe.1.1750483734276.1750484142339.7.13.290510; _jzqco=%7C%7C%7C%7C1750478360662%7C1.1560283885.1750478360629.1750481495046.1750484142637.1750481495046.1750484142637.0.0.0.4.4',
}

params = {
    '_fxpcqlniredt': '09031164116742831658',
    'x-traceID': '09031164116742831658-1750484175543-2015786',
}

json_data = {
    'arg': {
        'channelType': 2,
        'collapseType': 0,
        'commentTagId': 0,
        'pageIndex': 196,
        'pageSize': 10,
        'poiId': 77753,
        'sourceType': 1,
        'sortType': 3,
        'starType': 0,
    },
    'head': {
        'cid': '09031164116742831658',
        'ctok': '',
        'cver': '1.0',
        'lang': '01',
        'sid': '8888',
        'syscode': '09',
        'auth': '',
        'xsid': '',
        'extension': [],
    },
}


response = requests.options('https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList', params=params, headers=headers)
print(response.text)

response = requests.post(
    'https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList',
    params=params,
    cookies=cookies,
    headers=headers,
    json=json_data,
)
print(response.text)

