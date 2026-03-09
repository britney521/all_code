import time
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

# 获取药品列表并写入 CSV
def get_drug_list_and_write_csv():
    # 打开 CSV 文件
    with open('drug_list.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 写入表头
        writer.writerow([
            '药品名', '医保编号', '药品规格', '最小包装数量', '最小包装单位', '药品企业', '最高价格', '最低价格', '在售药店数量', '批准文号', '药店名称', '药店地址', '药店价格'
        ])

        for page in range(1, 3000):

            try:
                response_data = make_request(
                    f'https://ybj.jszwfw.gov.cn/jsyjt/apis/h5/drug/list?pageNum={page}&pageSize=100&orderBy=drugTypeId,id&isAsc=asc,asc',
                    cookies=cookies,
                    headers=headers,
                )
                code = response_data['code']
                data = response_data['data']
                total = data['total']
                if code == 0 and len(data) > 0:
                    lists = data['list']
                    if len(lists) > 0:
                        for item in lists:
                            registerName = item.get('registerName')
                            nationalDrugNum = item.get('nationalDrugNum')
                            actualSize = item.get('actualSize')
                            minPackageQuantity = item.get('minPackageQuantity')
                            packageUnit = item.get('packageUnit')
                            medicineCompany = item.get('medicineCompany')
                            storeCount217 = item.get('storeCount217')
                            approvalNumber = item.get('approvalNumber')
                            maxPrice217 = item.get('maxPrice217')
                            minPrice217 = item.get('minPrice217')

                            # 获取药品详情
                            details = get_detail(nationalDrugNum)
                            logger.info(f"第{page}页, 药品名: {registerName}, 在售店铺数: {len(details)}")
                            for detail in details:
                                writer.writerow([
                                    registerName, nationalDrugNum, actualSize, minPackageQuantity, packageUnit, medicineCompany, maxPrice217, minPrice217, storeCount217, approvalNumber,
                                    detail['storeName'], detail['storeAddress'], detail['storePrice']
                                ])
                    else:
                        logger.info(f"第{page}页没有更多数据。退出循环。")
                        break
                else:
                    logger.info(f"第{page}页没有数据。退出循环。")
                    break
            except Exception as e:
                logger.error(f"获取药品列表失败: {e}")
                break

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

# 执行获取药品列表并写入 CSV
get_drug_list_and_write_csv()