import requests
import pandas as pd
from datetime import datetime
cookies = {
    'cf_clearance': 'TR7qxzOUv1wa_19xWH_LzUeVzhLB9DxIK_cUMf8lt58-1765271828-1.2.1.1-0bYE6zp4WtkACSWs6TdjK7XzzAJC6wCGpOaEIT0SVMXvnh3fIiM3QQR55p.YHxkfeUTJI4mYNtKU3GShHxyOzzTQcAuE5fyjwUX1JyW_1Houx_SGeqInSfqvWQ.2r6rkXtYBC1h1zjTY0ITHgwWNmSRScRyZ0XCFwYLFKKoK2JcwcEd1TQQGzWmMSzjobuJA.FOXNgWbcvWZfEjT1veMmHHYzyboR2oe52P1vDLpmySTFK5.Q6t9t70_lZSBisHL',
}

def convert_echarts_to_excel(echarts_data, output_file="echarts_data.xlsx"):
    """
    将 ECharts 时间序列数据转换为 Excel 文件

    参数:
        echarts_data: 包含 start, step, values 的字典
        output_file: 输出的 Excel 文件名
    """
    # 提取数据
    start_ts = echarts_data["start"]
    step = echarts_data["step"]
    values = echarts_data["values"]

    # 生成日期列表
    dates = []
    for i in range(len(values)):
        # 计算当前时间戳（秒转毫秒）
        current_ts = (start_ts + i * step) * 1000
        # 转换为日期对象
        date_obj = datetime.fromtimestamp(current_ts / 1000)
        # 格式化为 YYYY-MM-DD 字符串
        dates.append(date_obj.strftime("%Y-%m-%d"))

    # 创建 DataFrame
    df = pd.DataFrame({
        "日期": dates,
        "数值": values
    })

    # 导出到 Excel
    df.to_excel(output_file, index=False, engine="openpyxl")
    print(f"数据已成功导出到 {output_file}")
headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': 'cf_clearance=TR7qxzOUv1wa_19xWH_LzUeVzhLB9DxIK_cUMf8lt58-1765271828-1.2.1.1-0bYE6zp4WtkACSWs6TdjK7XzzAJC6wCGpOaEIT0SVMXvnh3fIiM3QQR55p.YHxkfeUTJI4mYNtKU3GShHxyOzzTQcAuE5fyjwUX1JyW_1Houx_SGeqInSfqvWQ.2r6rkXtYBC1h1zjTY0ITHgwWNmSRScRyZ0XCFwYLFKKoK2JcwcEd1TQQGzWmMSzjobuJA.FOXNgWbcvWZfEjT1veMmHHYzyboR2oe52P1vDLpmySTFK5.Q6t9t70_lZSBisHL',
    'origin': 'https://steamdb.info',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://steamdb.info/app/810740/charts/',
    'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
    'sec-ch-ua-arch': '"arm"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"128.0.6541.223"',
    'sec-ch-ua-full-version-list': '"Not;A=Brand";v="24.0.0.0", "Chromium";v="128.0.6541.223"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"15.6.1"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

code = "810740"

params = {
    'appid': '810740',
}

response = requests.get('https://steamdb.info/api/GetGraphMax/', params=params, cookies=cookies, headers=headers)
data = response.json()['data']
print(data)

convert_echarts_to_excel(data, output_file=f"echarts_data{code}.xlsx")
# response = requests.get('https://steamdb.info/api/GetGraphWeek/', params=params, cookies=cookies, headers=headers)
# print(response.text)










