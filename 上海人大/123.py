import json
import time

import requests
from bs4 import BeautifulSoup

cookies = {
    'JSESSIONID': '6913A107E84FED961488328A5F29F420',
    'Hm_lvt_3bd83c7cf65d9651b52511ea2cdcdfd5': '1772456257',
    'HMACCOUNT': '221DCC5A65DE2271',
    '_pk_testcookie.149.5229': '1',
    '_pk_ses.149.5229': '1',
    'Hm_lpvt_3bd83c7cf65d9651b52511ea2cdcdfd5': '1772512874',
    '_pk_id.149.5229': '313efabd63864b94.1772456257.4.1772512874.1772511491.',
}

headers = {
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'JSESSIONID=6913A107E84FED961488328A5F29F420; Hm_lvt_3bd83c7cf65d9651b52511ea2cdcdfd5=1772456257; HMACCOUNT=221DCC5A65DE2271; _pk_testcookie.149.5229=1; _pk_ses.149.5229=1; Hm_lpvt_3bd83c7cf65d9651b52511ea2cdcdfd5=1772512874; _pk_id.149.5229=313efabd63864b94.1772456257.4.1772512874.1772511491.',
    'Pragma': 'no-cache',
    'Referer': 'https://www.shrd.gov.cn/shrd/2024n/2024n.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}
page = 1000
params = {
            'startrecord': str(1 + (page-1)*10),
            'endrecord': str(page*10),
            'perpage': '10',
            'contentTemplate': '',
            'columnId': '593f0397-04d7-44c3-8339-240a77a793ce', # columnId  '593f0397-04d7-44c3-8339-240a77a793ce'
            '_': str(int(time.time()*1000)),
        }

response = requests.get(
    'https://www.shrd.gov.cn/TrueCMS/messageController/getMessage.do',
    params=params,
    cookies=cookies,
    headers=headers,
)
print(response.text)

result = json.loads(response.text)['result']
# 第一步：解析外层XML结构，提取所有record标签
xml_soup = BeautifulSoup(result, 'html.parser')
records = xml_soup.find_all('record')
print(len(records))