import csv
import json
from functools import wraps
import pandas as pd
from loguru import logger
import requests
from time import sleep
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 定义重试装饰器
def retry(max_attempts=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"重试 {attempts + 1} 失败: {e}")
                    attempts += 1
                    sleep(delay)
            logger.error("重试三次也失败")
        return wrapper
    return decorator

def get_detail(medListCodg,areaNo):
    details = []
    for page in range(1,100):
        json_data = {
            'orderTypeCode': '1',
            'areaNo': areaNo,
            'medListCodg': medListCodg,
            'flage': 'P',
            'sortTypeCode': 'asc',
            'fixmedinsName': '',
            'lat': 45.28,
            'lnt': 130.98,
            'pageNo': page,
            'pageSize': 100,
        }

        @retry(max_attempts=3, delay=2)
        def make_request():
            response = requests.post(
                'https://ggfw.hljybj.org.cn/phac/hsa-net-phac-otc/drugInv/rx/query',
                cookies=cookies,
                headers=headers,
                json=json_data,
                verify=False,
            )
            statuscode = response.json()['code']
            data = response.json()['data']
            return statuscode,data

        statuscode,data = make_request()

        if statuscode == 0 and len(data) > 0:
            lists = data['list']
            if len(lists) > 0:
                for list in lists:
                    # 地址
                    addr = list.get('addr')
                    # 价格
                    rtalPric = list.get('rtalPric')
                    # 在售公司
                    fixmedinsName = list.get('fixmedinsName')
                    lat = list.get('lat')
                    lnt = list.get('lnt')
                    details.append([addr,rtalPric,fixmedinsName,lat,lnt])
            else:
                break
    return details


cookies = {
    'headerStatus': '0',
    'headerShow': 'false',
    'SESSION_FLAG': '0',
    'EXIT_STAMP': '1763183589534',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://ggfw.hljybj.org.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://ggfw.hljybj.org.cn/phac/phacH5/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36',
    'accessToken': "eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJoc2EiLCJuYW1lIjoiMjEwODgyMTk5MjEyMjkxMjE2IiwibG9naW5fdXNlcl9rZXkiOiJkZjBhODFhMS04NjEwLTQ2MzQtOTJmNS00OWI3MzMwOTI4OGQifQ._k7BdCfQIxMKY_jjMv02hTlEEl8s6q5-wLHacYK3Gd4",
    'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
}
# with open('data.json', 'r', encoding='utf-8') as f:
#     keywords = json.load(f)
df = pd.read_csv('/Users/britlee/Desktop/pythonProject/爬虫/医保/江西/江西南昌2.csv')
keywords = df['药品名'].tolist()
keywords = list(set(keywords))
citys = {
   # "绥化":"231200",
   "鸡西":"230300",
}

f = open('河南.csv', 'a', encoding='utf-8', newline='')
csv_writer = csv.writer(f)
# csv_writer.writerow([
#         '药品名', '医保编号', '药品规格', '剂型', '药品企业', '包装',
#         '在售药店数量', '批准文号','药店名称' , '药店价格','药店地址'
#     ])

for word in keywords:
    for city,code in citys.items():
        for page in range(1,100):
            json_data = {
                'areaNo': code,
                'pageNo': page,
                'pageSize': 100,
                'name': word,
                'medListCodg': '',
                'goodsClass': '',
                'drugEntp': '',
                'natDrugNo': '',
            }


            @retry(max_attempts=3, delay=2)
            def make_request():
                response = requests.post(
                    'https://ggfw.hljybj.org.cn/phac/hsa-net-phac-otc/queryDrugList/queryDis',
                    cookies=cookies,
                    headers=headers,
                    json=json_data,
                    verify=False,
                )
                statuscode = response.json()['code']
                data = response.json()['data']
                return statuscode,data


            statuscode,data = make_request()
            if statuscode == 0 and len(data) > 0:
                lists = data['list']
                if len(lists) > 0:
                    for list in lists:
                        # 药品名称
                        name = list.get('name')
                        # 药品编码
                        medListCodg = list.get('medListCodg')
                        # 药品规格
                        spec = list.get('spec')
                        # 剂型
                        dosunt = list.get('dosunt')
                        # 包装
                        pack = list.get('pack')
                        # 生成企业
                        drugEntp = list.get('drugEntp')
                        # 批准文号
                        pzwh = list.get('pzwh')
                        # 在售药店数量
                        count = list.get('count')
                        details = get_detail(medListCodg, code)
                        for detail in details:
                            logger.info('关键字{}搜索到{}'.format(word, ''.join(detail)))
                            csv_writer.writerow([name, medListCodg, spec, dosunt, drugEntp,pack,count, pzwh,*detail])
                else:
                    logger.info('关键字{}搜索到尾页'.format(word))
                    break
            else:
                logger.info('关键字{}搜索到尾页'.format(word))
                break