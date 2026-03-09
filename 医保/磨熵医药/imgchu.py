import os
import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from paddleocr import PaddleOCR

# --------------------------
# 1. 初始化设置
# --------------------------


# 读取 Excel
input_file = '【用法用量】待查找list.xlsx'
df = pd.read_excel(input_file)

# 确保列存在，如果不存在则创建
if '处理方式' not in df.columns:
    df['处理方式'] = None

# 请求头 (保持你提供的 Header)

headers = {
    'accept': 'application/x.myapp.v1+json',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc2VydmVyLnBoYXJuZXhjbG91ZC5jb21cL2V4dGVybmFsXC9hdXRoZW50aWNhdGVcL2F1dGhvcml6YXRpb25zIiwiaWF0IjoxNzcwMTY3Mjg4LCJleHAiOjE3NzAxOTYwODgsIm5iZiI6MTc3MDE2NzI4OCwianRpIjoib3duNXY3RDBjcUlwdjZySSIsInN1YiI6MjE0NzMzLCJwcnYiOiJkZjY4MjExYmRhNjQwNGRkNjRhMWZkZDAyZjJiMjE5OTFlOGI2MTM0Iiwibmlja25hbWUiOm51bGx9.rtrHZ4ku-NBbeChUMehyWDBmo_-07eZiytCK5tezeTQ',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://data.pharnexcloud.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://data.pharnexcloud.com/',
    'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}



# --------------------------
# 3. 主循环逻辑
# --------------------------

print(f"开始处理，共 {len(df)} 条数据...")

for index, row in df.iterrows():
    common_name = row['商品通用名']
    # 如果品牌是NaN，转为空字符串
    brand_summary = row['品牌（汇总）'] if pd.notna(row['品牌（汇总）']) else ""

    print(f"[{index + 1}/{len(df)}] 正在搜索: {common_name} {brand_summary}")

    # 构造搜索请求
    # 注意：这里需要根据实际 API 的 filters 规则填入搜索词，否则搜索结果可能不准
    # 假设 API 支持 keyword 搜索，通常需要放在 filters 里
    search_payload = {
        'filters': [
            {
                'module_id': 803,
                'precise': 0,
                'value': common_name,
            },
            {
                'module_id': 804,
                'precise': 0,
                'value': brand_summary,
            },
        ],
        'per_page': 10,
        'page': 1,
    }

    # 为了演示，如果你的 filters 为空也能搜到，保持原样；
    # 建议加上搜索关键词，否则 API 返回的可能是默认列表
    if not search_payload['filters']:
        # 简单尝试直接在 query param 或者 payload 增加 keyword
        pass

    try:
        # 1. 搜索文档列表
        resp_search = requests.post(
            'https://server.pharnexcloud.com/external/medical/databases/159/documents',
            headers=headers,
            json=search_payload  # 使用带参数的 payload
        )
        data_list = resp_search.json().get('data', [])

        extracted_content = "未找到说明书"

        if len(data_list) > 0:
            doc_info = data_list[0]  # 取第一个结果
            file_url = doc_info.get('html_path')
            relative_path = doc_info.get('relative_path')

            if relative_path:
                extracted_content = '图片下载'
        else:
            print("   -> 未找到相关文档数据")

        # 4. 写入 DataFrame
        df.at[index, '处理方式'] = extracted_content
        print(f"   -> 提取结果: {extracted_content[:30]}...")

    except Exception as e:
        print(f"   -> 处理该行时发生错误: {e}")
        df.at[index, '处理方式'] = "ERROR"

    # 5. 实时保存 (防止程序中途崩溃数据丢失)
    if index % 5 == 0:
        df.to_excel('【处理方式】结果_temp.xlsx', index=False)

    # 礼貌性延时


# --------------------------
# 4. 最终保存
# --------------------------
output_filename = '【处理方式】img.xlsx'
df.to_excel(output_filename, index=False)
print(f"\n全部完成！结果已保存至 {output_filename}")
