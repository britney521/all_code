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
    'accessToken': "eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJoc2EiLCJuYW1lIjoiMjEwODgyMTk5MjEyMjkxMjE2IiwibG9naW5fdXNlcl9rZXkiOiIwN2M0MDA4ZS0wODhmLTQ1ZmItOGUyOS0xOTFkNTdjNWI2MGEifQ.l2bzuqolpVao2eDaxi1gYP_0k11bwMLC_9W1k7iMpqk",
    'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
}

def main():

    # 1. 读取原始数据（pandas 直接读取，无需手动提取字段）
    df = pd.read_csv("鸡西.csv", encoding="utf-8-sig")
    duplicate_count = df.duplicated(subset=["药品名", "医保编号"]).sum()  # 统计重复数量
    df.drop_duplicates(subset=["药品名", "医保编号"], keep="first", inplace=True)
    logger.info(f"原始数据行数：{len(df) + duplicate_count}")
    logger.info(f"去重后行数：{len(df)}")
    logger.info(f"删除重复数据行数：{duplicate_count}")

    # 2. 定义输出字段（与表头对应，避免硬编码重复）
    output_fields = [
        '药品名', '医保编号', '药品规格', '剂型', '药品企业', '包装',
        '在售药店数量', '批准文号','药店名称' , '药店价格','药店地址',"经度","纬度"
    ]

    # 3. 用 with 语句自动管理文件（无需手动 close）
    with open('鸡西(带经纬度).csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # writer.writerow(output_fields)


        # 5. 用 itertuples 遍历 DataFrame（效率更高）
        for row in df.itertuples(index=False, name='Drug'):
            # 直接通过 元组.属性名 提取字段（比字典更高效）
            medListCodg = row.医保编号
            regName = row.药品名

            # 6. 调用获取药店详情
            details = get_detail(medListCodg,"230300")
            logger.info(f"--- 药品{regName}--药店数{len(details)}")

            # 7. 写入药店数据（直接使用元组属性，减少中间变量）
            for detail in details:
                writer.writerow([
                    regName,  # 药品名
                    medListCodg,  # 医保编号
                    row.药品规格,  # 药品规格
                    row.剂型,  # 最小包装数量
                    row.药品企业,  # 药品企业
                    row.包装,  # 药品企业
                    row.在售药店数量,  # 在售药店数量
                    row.批准文号,  # 批准文号
                    *detail
                ])




if __name__ == "__main__":
    main()