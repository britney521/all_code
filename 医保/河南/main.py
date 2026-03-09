import requests
import csv
from loguru import logger

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080712) UnifiedPCMacWechat(0xf2641411) XWEB/16990',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'x-auth-token': '4801b6625e8143c2a6f9218dad22caa3',
    'Origin': 'https://ggfw.ylbz.henan.gov.cn',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://ggfw.ylbz.henan.gov.cn/ltcapplet-ypbj/home/index?token=4801b6625e8143c2a6f9218dad22caa3',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

city_dict = {
    # "410100000000": "郑州市",
    # "410200000000": "开封市",
    # "410300000000": "洛阳市",
    # "410400000000": "平顶山市",
    # "410500000000": "安阳市",
    # "410600000000": "鹤壁市",
    "410700000000": "新乡市",
    "410800000000": "焦作市",
    "410900000000": "濮阳市",
    "411000000000": "许昌市",
    "411100000000": "漯河市",
    "411200000000": "三门峡市",
    "411300000000": "南阳市",
    "411400000000": "商丘市",
    "411500000000": "信阳市",
    "411600000000": "周口市",
    "411700000000": "驻马店市",
    "419001000000": "济源市"
}
f = open('河南.csv', 'a', encoding='utf-8', newline='')
csv_writer = csv.writer(f)
# csv_writer.writerow(['城市', '药品名', '生产企业', '类别', '规格', '剂型', '价格', '在售药店'])
for areaCode,city in city_dict.items():

    for page in range(1,1000):
        logger.info(f"{city}---第{page}页-----")
        json_data = {
            'url': f'/zs-medicine-cheapest/api/medicine/list?areaCode={areaCode}&pageNo={page}&pageSize=100',
            'method': 'GET',
        }

        response = requests.post('https://ggfw.ylbz.henan.gov.cn/ltcapplet/api/commonProgram', headers=headers, json=json_data)

        # print(response.json())
        code = response.json()['code']
        records = response.json()['data']['records']
        if not records and len(records)==0:
            logger.warning(f"{city}---第{page}页到尾页-----")
            break
        for record in records:
            hilistName = record['hilistName']
            prodentpName = record['prodentpName']
            hilistCode = record['hilistCode']
            spec = record['spec']
            listType = record['listType']
            dosformName = record['dosformName']
            priceStr = record['priceStr']
            fixmedinsSalenum = record['fixmedinsSalenum']
            logger.info("{}--{}---{}---{}----{}---{}----{}".format(hilistName,prodentpName,listType,spec,dosformName,priceStr,fixmedinsSalenum))
            csv_writer.writerow([city,hilistName,prodentpName,listType,spec,dosformName,priceStr,fixmedinsSalenum])