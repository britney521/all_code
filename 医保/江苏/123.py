import requests

cookies = {
    'UM_distinctid': '19a72b07d78581-08189596296bed-17525637-1fa400-19a72b07d791271',
    'CNZZDATA1281383319': '1400709553-1762860760-%7C1763340955',
    'SERVERID': '063a1e3538f01f0a348725273ca244f4|1763340963|1763183430',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'UM_distinctid=19a72b07d78581-08189596296bed-17525637-1fa400-19a72b07d791271; CNZZDATA1281383319=1400709553-1762860760-%7C1763340955; SERVERID=063a1e3538f01f0a348725273ca244f4|1763340963|1763183430',
    'Pragma': 'no-cache',
    'Referer': 'https://ybj.jszwfw.gov.cn/jsyjt/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36',
    'city': '217',
    'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
}

response = requests.get(
    'https://ybj.jszwfw.gov.cn/jsyjt/apis/h5/drug/list?pageNum=105&pageSize=100&orderBy=drugTypeId,id&isAsc=asc,asc',
    cookies=cookies,
    headers=headers,
)

print(response.text)
code = response.json()['code']
data = response.json()['data']
total = data['total']
if code == 0 and len(data) > 0:
    lists = data['list']
    print(len(lists))