import random
import requests
import time
import csv
from never_jscore import Context
from loguru import logger
from functools import wraps
from time import sleep
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = requests.Session()

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

def get_unicode(timestamp):
    # 生成随机数和当前时间戳
    random_number = int(1e6 * random.random())
    return str(random_number) + str(timestamp)

def get_detail(medListCodg, regName, code):
    details = []
    for page in range(1, 100):
        timestr = int(time.time() * 1000)
        i = {
            "appId": "rI6eAOjuVeaTqto9",
            "data": {
                "where": {
                    "admdvs": code,
                    "rtalPhacName": "",
                    "distance": "",
                    "medListCodg": medListCodg,
                    "regName": regName,
                    "longitude": "",
                    "latitude": ""
                },
                "sort": [
                    [
                        "pric",
                        "asc"
                    ]
                ],
                "pageNum": page,
                "pageSize": 1000
            },
            "timestamp": timestr,
            "version": "1.0.0"
        }

        result = ctx.call("get_endata", [i])
        json_data = {
            'appId': 'rI6eAOjuVeaTqto9',
            'timestamp': timestr,
            'version': '1.0.0',
            'encData': result['encData'],
            'signData': result['signData'],
        }

        @retry(max_attempts=3, delay=2)
        def make_request():
            response = session.post(
                'https://ybwt.ybj.gxzf.gov.cn/hsa-local-test/hsa-pss-pw/apply/others/drugPriceComparision/getDrugRtalPhacInfo',
                headers=headers,
                json=json_data,
                timeout=20,
                verify=False
            )
            return response

        response = make_request()
        encData = response.json().get('encData')
        if not encData:
            logger.error("未获取到 encData")
            continue

        res = ctx.call("get_data", encData[2:])

        data = res.get('data')
        statuscode = data.get('code')
        result = data.get('data', {}).get('result')
        if statuscode != 0:
            logger.error("详情异常")
        if not result or len(result) == 0:
            logger.info(f"详情到末尾页了")
            break
        logger.info(f"{regName}-获取到-{len(result)}条门店地址")
        for item in result:
            rtalPhacName = item.get('rtalPhacName')
            addr = item.get('addr')
            pricMin = item.get('pricMin')
            longitude = item.get('longitude')
            latitude = item.get('latitude')
            details.append({
                "rtalPhacName": rtalPhacName,
                "addr": addr,
                "pricMin": pricMin,
                "longitude": longitude,
                "latitude": latitude,
            })

    return details


ctx = Context()
ctx.compile(open('sm.js', 'r', encoding="utf-8").read())

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://ybwt.ybj.gxzf.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://ybwt.ybj.gxzf.gov.cn/web/drug-price-compare/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36',
    'accessToken': '',
    'appId': 'rI6eAOjuVeaTqto9',
    'channlId': 'rI6eAOjuVeaTqto9',
    'scene': 'known',
    'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sourc': 'browser',
}

if __name__ == '__main__':

    citys = {
        "南宁市": "4501",
        # "柳州市": "4502",
    }

    file = open('南宁市.csv', mode='a', newline='', encoding='utf-8')
    writer = csv.writer(file)
    # 写入表头
    # writer.writerow([
    #     "城市",
    #     '药品名', '医保编号', '药品规格', '最小包装数量', '最小包装单位', '药品企业', '价格区间', '均价',
    #     '在售药店数量', '批准文号', '药店名称', '药店地址', '药店价格',"经度","纬度"
    # ])

    for city, code in citys.items():
        def get_city_data(city, code):
            for page in range(35, 2000):
                timestr = int(time.time() * 1000)
                UNICDOE = get_unicode(timestr)
                i = {
                    'appId': 'rI6eAOjuVeaTqto9',
                    "data": {
                        "where": {
                            "admdvs": code,
                            "drugType": "",
                            "regName": "",
                            "longitude": "",
                            "latitude": ""
                        },
                        "sort": [
                            [
                                "drugSale",
                                "desc"
                            ]
                        ],
                        "pageNum": page,
                        "pageSize": 100,
                        "uniqueCode": UNICDOE
                    },
                    "timestamp": timestr,
                    "version": "1.0.0"
                }

                result = ctx.call("get_endata", [i])
                json_data = {
                    'appId': 'rI6eAOjuVeaTqto9',
                    'timestamp': timestr,
                    'version': '1.0.0',
                    'encData': result['encData'],
                    'signData': result['signData'],
                }

                @retry(max_attempts=3, delay=2)
                def make_request():
                    response = session.post(
                        'https://ybwt.ybj.gxzf.gov.cn/hsa-local-test/hsa-pss-pw/apply/others/drugPriceComparision/getDrugInfo',
                        headers=headers,
                        json=json_data,
                        timeout=20,
                        verify=False
                    )
                    return response

                response = make_request()
                encData = response.json().get('encData')

                res = ctx.call("get_data", encData[2:])

                data = res.get('data')
                result = data.get('data', {}).get('result')
                if not result or len(result) == 0:
                    logger.error(f"第{page}页没有数据退出")
                    break
                for item in result:
                    # 药品名
                    regName = item.get('regName')
                    # 医保编号
                    medListCodg = item.get('medListCodg')
                    # 生产企业
                    prodentpName = item.get('prodentpName')
                    # 药品规格
                    drugSpec = item.get('drugSpec')
                    # 批准文号
                    aprvno = item.get('aprvno')
                    # 在售药店数量
                    onSaleOrg = item.get('onSaleOrg')
                    # 均价
                    phacAvgPric = item.get('phacAvgPric')
                    # 最小包装单位
                    minPacunt = item.get('minPacunt')
                    # 最小包装数量
                    minPacCnt = item.get('minPacCnt')
                    # 价格区间
                    phacMinPric = item.get('phacMinPric')
                    phacMaxPric = item.get('phacMaxPric')
                    price_area = f"{phacMaxPric}-{phacMinPric}"

                    details = get_detail(medListCodg, regName, code)
                    logger.info(f"城市{city}--第{page}页-- 药品{regName}--药店数{len(details)}")
                    for detail in details:
                        writer.writerow([city, regName, medListCodg, drugSpec, minPacCnt, minPacunt, prodentpName, price_area, phacAvgPric, onSaleOrg, aprvno
                                         , detail['rtalPhacName'], detail['addr'], detail['pricMin'],detail['longitude'],detail['latitude']])

        get_city_data(city, code)

    file.close()