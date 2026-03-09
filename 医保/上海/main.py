import csv
import json
import traceback

import requests
import execjs
from requestsretry import request_with_retry
from loguru import logger

# ----------------- 1. Loguru 日志配置 -----------------
# 控制台会正常输出，同时会自动在当前目录生成日志文件，文件最大 10MB，自动轮转
logger.add("spider_log_{time:YYYY-MM-DD}.log", rotation="10 MB", level="INFO")

# 尝试加载 JS 逆向文件
try:
    ctx = execjs.compile(open('js/jiami.js', 'r', encoding='utf-8').read())
    logger.info("成功加载 jiami.js 加密环境")
except Exception as e:
    logger.critical(f"加载 JS 文件失败，请检查文件路径: {e}")
    exit(1)

headers = {
    'Accept': 'application/json;charset=UTF-8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Client-ID': '6efca3ef-056f-4c56-8a45-02af1ba79150',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;',
    'Origin': 'https://bjxt.smiic.net.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://bjxt.smiic.net.cn/ypcx/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}


def get_detail(drugCode, regName, rsaPublicKey):
    details = []
    for page in range(1, 100):
        try:
            n = {
                "code": "YBDRUG002",
                "identity": "",
                "departId": "",
                "purpose": "1",
                "qdlybz": "17",
                "admdvsL": "310000",
                "reqData": [
                    {
                        "drugCode": drugCode,
                        "phacName": "",
                        "priceSortFlag": "",
                        "saleSortFlag": "",
                        "distSortFlag": "",
                        "admdvs": 310000,
                        "pageSize": 100,
                        "pageNum": page
                    }
                ]
            }

            # 加密报错防护
            try:
                aeskey = ctx.call('genKey')
                encryptText = ctx.call('encrypt', n, aeskey)
                encryptedAESKey = ctx.call('get_rsaEncryptAesKey', aeskey, rsaPublicKey)
            except Exception as e:
                logger.error(f"[{regName}] 第{page}页 加密参数生成失败: {e}")
                continue

            json_data = {
                'encryptedAESKey': encryptedAESKey,
                'encryptText': encryptText,
                'pubChnl': '3',
                'accessToken': 'xJfiHHiBoeWBWQxwAz9yOcgEuc1zkVlwCDtrt67uoiRZyyg3CLSmHOs5PdH2aYEFUGEWwIN70uexqGVgncEm0Fg8bbtlpeae5H6tu8Z6E2oDgTIMSzTrPUnBgsTrX96kydSkG2s81gzZ3cohbesq51mRCVBjWd3SG2gZRFOx8LoEF95023fXXqxRpXm3x31lX4eZtIi12j9ohJOAnGqCHTk5JbrDaT5NZr4b89qXKiozoVznqyryEWq4RwKRg03socOhD5tCV6bVrPitGGke8oJwoCgf4FLC5nMnSGXwbLd5BsojrFHwbqjDB5vnA5La',
            }

            # 加入 timeout 防止请求卡死
            response = request_with_retry('post','https://bjxt.smiic.net.cn/hsa-mbs-pub/api/v1/main/operateRsa',
                                     headers=headers, json=json_data, timeout=15)
            response.raise_for_status()

            res_json = response.json()
            encData = res_json.get('data')

            if not encData:
                logger.warning(f"[{regName}] 第{page}页 未获取到 encData，跳过。接口返回: {res_json}")
                continue

            # 解密报错防护
            try:
                decrypt_json = ctx.call('decrypt', encData, aeskey)
                result = decrypt_json.get('data')
            except Exception as e:
                logger.error(f"[{regName}] 第{page}页 解密数据失败: {e}")
                continue

            if not result or len(result) == 0:
                logger.debug(f"[{regName}] 详情查询到达末尾，最后页码为: {page - 1}")
                break

            logger.info(f"[{regName}] 第{page}页 获取到 {len(result)} 条门店地址")

            for item in result:
                # 使用 .get() 设置默认值，防止字段缺失导致 KeyError 报错
                details.append({
                    "rtalPhacName": item.get('phacName', '未知药店'),
                    "addr": item.get('phacAddr', '未知地址'),
                    "pricMin": item.get('drugLastPrice', '未知'),
                    "longitude": item.get('lnt', ''),
                    "latitude": item.get('lat', ''),
                })

        except requests.exceptions.RequestException as e:
            logger.error(f"[{regName}] 第{page}页 网络请求失败: {e}")
            continue
        except Exception as e:
            logger.error(f"[{regName}] 第{page}页 发生未知错误: {e}\n{traceback.format_exc()}")
            continue

    return details


def main():
    output_fields = [
        '药品名', '医保编号', '药品规格', '最小包装数量', '最小包装单位', '药品企业', '均价', '价格区间',
        '在售药店数量', '药店名称', '药店地址', '药店价格', "经度", "纬度"
    ]

    # 获取全局 rsaPublicKey
    try:
        response = requests.get('https://bjxt.smiic.net.cn/hsa-mbs-pub/api/v1/main/keys', headers=headers, timeout=10)
        response.raise_for_status()
        rsaPublicKey = response.json().get('data', {}).get('rsaPublicKey')
        if not rsaPublicKey:
            raise ValueError("接口返回数据中未找到 rsaPublicKey")
        logger.info("成功获取全局 rsaPublicKey")
    except Exception as e:
        logger.critical(f"初始化获取公钥失败，程序终止: {e}")
        return

    # 正确使用 with 语句自动管理文件上下文
    try:
        with open('上海.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(output_fields)

            for page in range(1, 1000):
                try:
                    word = {
                        "code": "YBDRUG001",
                        "identity": "",
                        "departId": "",
                        "purpose": "1",
                        "qdlybz": "17",
                        "admdvsL": "310000",
                        "reqData": [{
                            "drugName": "",
                            "saleSortFlag": "",
                            "pageSize": 100,
                            "pageNum": page
                        }]
                    }

                    aeskey = ctx.call('genKey')
                    encryptText = ctx.call('encrypt', word, aeskey)
                    encryptedAESKey = ctx.call('get_rsaEncryptAesKey', aeskey, rsaPublicKey)

                    json_data = {
                        'encryptedAESKey': encryptedAESKey,
                        'encryptText': encryptText,
                        'pubChnl': '3',
                        'accessToken': 'xJfiHHiBoeWBWQxwAz9yOcgEuc1zkVlwCDtrt67uoiRZyyg3CLSmHOs5PdH2aYEFUGEWwIN70uexqGVgncEm0Fg8bbtlpeae5H6tu8Z6E2oDgTIMSzTrPUnBgsTrX96kydSkG2s81gzZ3cohbesq51mRCVBjWd3SG2gZRFOx8LoEF95023fXXqxRpXm3x31lX4eZtIi12j9ohJOAnGqCHTk5JbrDaT5NZr4b89qXKiozoVznqyryEWq4RwKRg03socOhD5tCV6bVrPitGGke8oJwoCgf4FLC5nMnSGXwbLd5BsojrFHwbqjDB5vnA5La'
                    }

                    # 假设你的 request_with_retry 已自带报错重试逻辑，这里我们仍需捕获它最终可能抛出的异常
                    response = request_with_retry(method='post',
                                                  url='https://bjxt.smiic.net.cn/hsa-mbs-pub/api/v1/main/operateRsa',
                                                  headers=headers, json=json_data)

                    res_json = response.json()
                    if res_json.get('success'):
                        encData = res_json.get('data')
                        if not encData:
                            logger.warning(f"--第{page}页-- 主列表数据为空，可能已无数据")
                            continue

                        decryptText = ctx.call('decrypt', encData, aeskey)
                        datas = decryptText.get('data', [])

                        if not datas:
                            logger.info(f"主列表抓取到达末尾，最后页码为 {page - 1}")
                            break

                        for data in datas:
                            try:
                                # 使用 get 预防脏数据导致异常
                                drugCode = data.get('drugCode', '')
                                drugName = data.get('drugName', '未知药品')
                                drugSpec = data.get('drugSpec', '')
                                drugAvgPrice = data.get('drugAvgPrice', '')
                                drugMinPrice = data.get('drugMinPrice', '')
                                drugMaxPrice = data.get('drugMaxPrice', '')
                                pacCnt = data.get('pacCnt', '')
                                pacUnt = data.get('pacUnt', '')
                                prodentpName = data.get('prodentpName', '')
                                phacCnt = data.get('phacCnt', 0)

                                # 将 rsaPublicKey 传递给内部函数，避免重复请求或作用域问题
                                details = get_detail(drugCode, drugName, rsaPublicKey)
                                logger.info(f"--第{page}页-- 药品: {drugName} -- 抓取到 {len(details)} 家门店详情")

                                for detail in details:
                                    writer.writerow([
                                        drugName, drugCode, drugSpec, pacCnt, pacUnt, prodentpName,
                                        drugAvgPrice, f'{drugMinPrice}-{drugMaxPrice}', phacCnt,
                                        detail['rtalPhacName'], detail['addr'], detail['pricMin'],
                                        detail['longitude'], detail['latitude']
                                    ])

                            except Exception as e:
                                logger.error(f"--第{page}页-- 写入或处理药品 {data.get('drugName')} 数据时报错: {e}")
                                continue
                    else:
                        logger.warning(
                            f"--第{page}页-- 主列表请求 success 状态为 False: {res_json.get('message', '未知原因')}")

                except Exception as e:
                    logger.error(f"--第{page}页-- 主列表抓取发生异常: {e}\n{traceback.format_exc()}")
                    continue  # 当前页失败，跳过并尝试抓取下一页

    except Exception as e:
        logger.critical(f"打开或写入 CSV 文件时发生严重错误: {e}")


if __name__ == '__main__':
    main()