import random

import pandas as pd
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


def main():
    # 城市配置（保持原有结构，后续扩展方便）
    citys = {
        # "南宁市": "4501",
        "柳州市": "4502",
    }
    # 1. 读取原始数据（pandas 直接读取，无需手动提取字段）
    df = pd.read_csv("柳州药品.csv", encoding="utf-8-sig")
    df = df[df['城市']=="柳州市"]
    duplicate_count = df.duplicated(subset=["药品名", "医保编号"]).sum()  # 统计重复数量
    df.drop_duplicates(subset=["药品名", "医保编号"], keep="first", inplace=True)
    logger.info(f"原始数据行数：{len(df) + duplicate_count}")
    logger.info(f"去重后行数：{len(df)}")
    logger.info(f"删除重复数据行数：{duplicate_count}")

    # 2. 定义输出字段（与表头对应，避免硬编码重复）
    output_fields = [
        "城市", "药品名", "医保编号", "药品规格", "最小包装数量", "最小包装单位",
        "药品企业", "价格区间", "均价", "在售药店数量", "批准文号",
        "药店名称", "药店地址", "药店价格", "经度", "纬度"
    ]

    # 3. 用 with 语句自动管理文件（无需手动 close）
    with open('柳州(带经纬度).csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # writer.writerow(output_fields)

        # 4. 遍历城市
        for city, code in citys.items():
            # 5. 用 itertuples 遍历 DataFrame（效率更高）
            for row in df.itertuples(index=False, name='Drug'):
                # 直接通过 元组.属性名 提取字段（比字典更高效）
                medListCodg = row.医保编号
                regName = row.药品名

                # 6. 调用获取药店详情
                details = get_detail(medListCodg, regName, code)
                logger.info(f"城市{city}--- 药品{regName}--药店数{len(details)}")

                # 7. 写入药店数据（直接使用元组属性，减少中间变量）
                for detail in details:
                    writer.writerow([
                        city,
                        regName,  # 药品名
                        medListCodg,  # 医保编号
                        row.药品规格,  # 药品规格
                        row.最小包装数量,  # 最小包装数量
                        row.最小包装单位,  # 最小包装单位
                        row.药品企业,  # 药品企业
                        row.价格区间,  # 价格区间
                        row.均价,  # 均价
                        row.在售药店数量,  # 在售药店数量
                        row.批准文号,  # 批准文号
                        detail['rtalPhacName'],  # 药店名称
                        detail['addr'],  # 药店地址
                        detail['pricMin'],  # 药店价格
                        detail.get('longitude', ''),  # 经度（兼容无数据）
                        detail.get('latitude', '')  # 纬度（兼容无数据）
                    ])


if __name__ == "__main__":
    main()