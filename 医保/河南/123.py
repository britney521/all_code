import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080712) UnifiedPCMacWechat(0xf2641411) XWEB/16990',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'x-auth-token': '0f7385ef0122479eb8ca3d65b9fd07a8',
    'Origin': 'https://ggfw.ylbz.henan.gov.cn',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://ggfw.ylbz.henan.gov.cn/ltcapplet-ypbj/home/index?token=0f7385ef0122479eb8ca3d65b9fd07a8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
for page in range(1, 11):
    json_data = {
        'url': f'/zs-medicine-cheapest/api/medicine/list?areaCode=410100000000&pageNo={page}&pageSize=100',
        'method': 'GET',
    }

    response = requests.post('https://ggfw.ylbz.henan.gov.cn/ltcapplet/api/commonProgram', headers=headers, json=json_data)

    print(response.json())

    code = response.json()['code']
    records = response.json()['data']['records']
    if not records and len(records)==0:
        print('end')
    print(len(records))