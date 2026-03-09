import time

import pandas as pd
import requests
from loguru import logger
from time import sleep
import csv
from functools import wraps

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
                    logger.error(f"请求失败，尝试次数 {attempts + 1}/{max_attempts}: {e}")
                    attempts += 1
                    sleep(delay)
            logger.error("请求失败，已达到最大尝试次数。")
            raise Exception("请求失败，已达到最大尝试次数。")
        return wrapper
    return decorator

# 使用装饰器包装请求函数
@retry(max_attempts=3, delay=2)
def make_request(url, params=None, cookies=None, headers=None):
    response = requests.get(url, params=params, cookies=cookies, headers=headers)
    response.raise_for_status()  # 检查请求是否成功
    return response.json()

# 获取药品详情
def get_detail(drugNum):
    details = []
    for page in range(0, 100):
        params = {
            'sort': '1',
            'pageNum': str(page),
            'pageSize': '100',
            'drugNum': drugNum,
            'longitude': '119.9644',
            'latitude': '31.7928',
        }
        try:
            response_data = make_request('https://ybj.jszwfw.gov.cn/jsyjt/apis/h5/drug/storeList', params=params, cookies=cookies, headers=headers)
            code = response_data['code']
            data = response_data['data']
            total = data['total']
            if code == 0 and len(data) > 0:
                lists = data['list']
                if len(lists) > 0:
                    for item in lists:
                        storeName = item.get('storeName')
                        storeAddress = item.get('storeAddress')
                        storePrice = item.get('storePrice')
                        longitude = item.get('longitude')
                        latitude = item.get('latitude')
                        details.append({
                            'storeName': storeName,
                            'storeAddress': storeAddress,
                            'storePrice': storePrice,
                            'longitude': longitude,
                            'latitude': latitude
                        })
                else:
                    logger.info(f"第{page}页没有更多数据。退出循环。")
                    break
            else:
                logger.info(f"第{page}页没有数据。退出循环。")
                break
        except Exception as e:
            logger.error(f"获取药品详情失败: {e}")
            break
    return details


# Cookies 和 Headers
cookies = {
    'UM_distinctid': '19a72b07d78581-08189596296bed-17525637-1fa400-19a72b07d791271',
    'SERVERID': '063a1e3538f01f0a348725273ca244f4|1763207828|1763183430',
    'CNZZDATA1281383319': '1400709553-1762860760-%7C1763207828',
}
headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
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



def main():
    # 城市配置（保持原有结构，后续扩展方便）

    # 1. 读取原始数据（pandas 直接读取，无需手动提取字段）
    df = pd.read_csv("江苏药品.csv", encoding="utf-8-sig")
    duplicate_count = df.duplicated(subset=["药品名", "医保编号"]).sum()  # 统计重复数量
    df.drop_duplicates(subset=["药品名", "医保编号"], keep="first", inplace=True)
    logger.info(f"原始数据行数：{len(df) + duplicate_count}")
    logger.info(f"去重后行数：{len(df)}")
    logger.info(f"删除重复数据行数：{duplicate_count}")

    # 2. 定义输出字段（与表头对应，避免硬编码重复）
    output_fields = [
      '药品名', '医保编号', '药品规格', '最小包装数量', '最小包装单位', '药品企业', '最高价格', '最低价格', '在售药店数量', '批准文号', '药店名称', '药店地址', '药店价格',"经度", "纬度"
    ]

    # 3. 用 with 语句自动管理文件（无需手动 close）
    with open('常州(带经纬度).csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(output_fields)


        # 5. 用 itertuples 遍历 DataFrame（效率更高）
        for row in df.itertuples(index=False, name='Drug'):
            # 直接通过 元组.属性名 提取字段（比字典更高效）
            medListCodg = row.医保编号
            regName = row.药品名

            # 6. 调用获取药店详情
            details = get_detail(medListCodg)
            logger.info(f"--- 药品{regName}--药店数{len(details)}")

            # 7. 写入药店数据（直接使用元组属性，减少中间变量）
            for detail in details:
                writer.writerow([
                    regName,  # 药品名
                    medListCodg,  # 医保编号
                    row.药品规格,  # 药品规格
                    row.最小包装数量,  # 最小包装数量
                    row.最小包装单位,  # 最小包装单位
                    row.药品企业,  # 药品企业
                    row.最高价格,  # 药品企业
                    row.最低价格,  # 药品企业
                    row.在售药店数量,  # 在售药店数量
                    row.批准文号,  # 批准文号
                    detail['storeName'],  # 药店名称
                    detail['storeAddress'],  # 药店地址
                    detail['storePrice'],  # 药店价格
                    detail.get('longitude', ''),  # 经度（兼容无数据）
                    detail.get('latitude', '')  # 纬度（兼容无数据）
                ])




if __name__ == "__main__":
    main()