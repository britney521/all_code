import time

import pandas as pd
import requests

cookies = {
    'webName': '9492b9e0-6499-41b0-959f-b41b49b80841',
    'zh_choose': 's',
    'MM_1xL8nvQydGCE0': '',
    '_yfxkpy_ssid_10003718': '%7B%22_yfxkpy_firsttime%22%3A%221723424462852%22%2C%22_yfxkpy_lasttime%22%3A%221723424462852%22%2C%22_yfxkpy_visittime%22%3A%221723424462852%22%2C%22_yfxkpy_cookie%22%3A%2220240812090102854109659689219835%22%7D',
    'Hm_lvt_3b3841fa5dff5e77feed1b64f6474e87': '1723424463',
    'Hm_lpvt_3b3841fa5dff5e77feed1b64f6474e87': '1723424463',
    'HMACCOUNT': '79D7E68F98D324B2',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'webName=9492b9e0-6499-41b0-959f-b41b49b80841; zh_choose=s; MM_1xL8nvQydGCE0=; _yfxkpy_ssid_10003718=%7B%22_yfxkpy_firsttime%22%3A%221723424462852%22%2C%22_yfxkpy_lasttime%22%3A%221723424462852%22%2C%22_yfxkpy_visittime%22%3A%221723424462852%22%2C%22_yfxkpy_cookie%22%3A%2220240812090102854109659689219835%22%7D; Hm_lvt_3b3841fa5dff5e77feed1b64f6474e87=1723424463; Hm_lpvt_3b3841fa5dff5e77feed1b64f6474e87=1723424463; HMACCOUNT=79D7E68F98D324B2',
    'Origin': 'http://hunan.chinatax.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'http://hunan.chinatax.gov.cn/taxpayercreditsearch/20190413003983',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'X-Requested-With': 'XMLHttpRequest',
}

for i in range(1,100):
    time.sleep(0.5)
    data = {
        'page': f'{i}',
        'limit': '11',
        'taxpayer_number': '',
        'taxpayer_name': '',
        'year': '2023',
        'siteName': '长沙',
        '_csrf': '09fd01be-3365-4a83-99a0-a327c1d04312',
    }

    response = requests.post('http://hunan.chinatax.gov.cn/taxpayercreditsearchgetdata', cookies=cookies, headers=headers, data=data, verify=False)
    datas = response.json()['data']
    df = pd.DataFrame(datas)
    print(f'第{i}页--------------------------------')
    print(df)
    if i == 1:
        df.to_csv('税务局.csv', mode='w', header=True, index=False)
    else:
        df.to_csv('税务局.csv', mode='a', header=False, index=False)