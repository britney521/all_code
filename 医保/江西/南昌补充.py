import pandas as pd
from functools import wraps
from time import sleep
import requests
from loguru import logger
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import json
import base64
import csv

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

# AES 加密
def aes_encrypt(data, key):
    data_bytes = data.encode('utf-8')
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, key.encode('utf-8'))
    padded_data = pad(data_bytes, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    encrypted_data_b64 = base64.b64encode(encrypted_data).decode('utf-8')
    return encrypted_data_b64

# AES 解密
def aes_decrypt(encrypted_data, key):
    key_bytes = key.encode('utf-8')
    encrypted_data_bytes = base64.b64decode(encrypted_data)
    cipher = AES.new(key_bytes, AES.MODE_CBC, key_bytes)
    decrypted_data_bytes = cipher.decrypt(encrypted_data_bytes)
    decrypted_data_str = decrypted_data_bytes.decode('utf-8', errors='ignore')
    return json.loads(decrypted_data_str.replace('\0', ''))

# 带重试的 POST 请求
@retry(max_attempts=3, delay=2)
def make_post_request(url, json_data, cookies, headers):
    response = requests.post(url, json=json_data, cookies=cookies, headers=headers)
    response.raise_for_status()
    return response.json()
# 配置
cookies = {
    'UM_distinctid': '19a85e367a7213-0e24ace964f4bb-17525637-1fa400-19a85e367a83076',
    'XSRF-TOKEN': '10e226d3-467e-42ce-884a-ebb3f14a090c',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Access-Token': '666',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://ggfw.ybj.jiangxi.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://ggfw.ybj.jiangxi.gov.cn/miisa/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36',
    'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'x-term-type': '5',
}

key = "0011223344556677"
# 获取药品详情
def get_detail(medListCodg):
    details = []
    for page in range(1, 100):
        params = {
            "lnt": "108.366",
            "lat": "22.817",
            "medListCodg": medListCodg,
            "fixmedinsName": "",
            "sortWay": "price_priority_desc",
            "fixBlngAdmdvs": "360100",
            "pageNum": page,
            "pageSize": 100
        }
        encrypted_data = aes_encrypt(json.dumps(params), key)
        json_data = {'inputJson': encrypted_data}

        try:
            response = make_post_request(
                'https://ggfw.ybj.jiangxi.gov.cn/miisa/hcpp/api/drug/pric-compare',
                json_data=json_data,
                cookies=cookies,
                headers=headers
            )
            output = response['output']
            decrypted_data = aes_decrypt(output, key)
            code = decrypted_data['code']
            if code != 0:
                logger.error(f"{medListCodg} 未获取到详情数据")
                continue
            data = decrypted_data['data'].get('data')
            if not data or len(data) == 0:
                logger.warning(f"{medListCodg} 到达末尾页面")
                break
            for item in data:
                addr = item.get('addr')
                finlTrnsPric = item.get('finlTrnsPric')
                fixmedinsName = item.get('fixmedinsName')
                lnt = item.get('lnt')
                lat = item.get('lat')
                details.append({
                    'addr': addr,
                    "finlTrnsPric": finlTrnsPric,
                    "fixmedinsName": fixmedinsName,
                    "lnt": lnt,
                    "lat": lat,
                })
        except Exception as e:
            logger.error(f"获取药品详情失败: {e}")
            break
    return details

def main():
    # 城市配置（保持原有结构，后续扩展方便）

    # 1. 读取原始数据（pandas 直接读取，无需手动提取字段）
    df = pd.read_csv("江西南昌2.csv", encoding="utf-8-sig")
    duplicate_count = df.duplicated(subset=["药品名", "医保编号"]).sum()  # 统计重复数量
    df.drop_duplicates(subset=["药品名", "医保编号"], keep="first", inplace=True)
    logger.info(f"原始数据行数：{len(df) + duplicate_count}")
    logger.info(f"去重后行数：{len(df)}")
    logger.info(f"删除重复数据行数：{duplicate_count}")

    # 2. 定义输出字段（与表头对应，避免硬编码重复）
    output_fields = [
        '药品名', '医保编号', '药品规格', '最小包装数量', '最小包装单位', '药品企业', '均价',
        '在售药店数量', '批准文号', '药店名称', '药店价格', '药店地址',"经度","纬度"
    ]

    # 3. 用 with 语句自动管理文件（无需手动 close）
    with open('南昌2(带经纬度).csv', mode='w', newline='', encoding='utf-8') as file:
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
                    row.均价,  # 药品企业
                    row.在售药店数量,  # 在售药店数量
                    row.批准文号,  # 批准文号
                    detail['addr'],  # 药店名称
                    detail['finlTrnsPric'],  # 药店地址
                    detail['fixmedinsName'],  # 药店价格
                    detail.get('lnt', ''),  # 经度（兼容无数据）
                    detail.get('lat', '')  # 纬度（兼容无数据）
                ])




if __name__ == "__main__":
    main()