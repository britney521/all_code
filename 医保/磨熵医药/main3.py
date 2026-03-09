import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
import os

# --------------------------
# 1. 配置与初始化
# --------------------------
input_file = '【用法用量】提取完成.xlsx'
output_file = '【用法用量】HTML暴力补全版.xlsx'

# --- 新增：定义HTML保存目录 ---
html_save_dir = 'html_docs'
if not os.path.exists(html_save_dir):
    os.makedirs(html_save_dir)
    print(f"已创建目录: {html_save_dir}")

if not os.path.exists(input_file):
    print(f"错误：找不到文件 {input_file}")
    exit()

df = pd.read_excel(input_file)
print(f"读取成功，共 {len(df)} 行数据")

# 请求头
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
# 2. 核心函数：全文正则提取
# --------------------------
def extract_by_text_regex(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        full_text = soup.get_text(separator="\n", strip=True)

        pattern = r"(?:【|^)\s*(?:用法用量|用法与用量)(?:】|[:：])?\s*(.*?)(?=\n\s*(?:【|\[|不良反应|禁忌|注意事项|规格|贮藏|有效期|批准文号|生产企业)|$)"
        match = re.search(pattern, full_text, re.DOTALL | re.IGNORECASE)

        if match:
            content = match.group(1).strip()
            if len(content) > 1:
                return content
        return None
    except Exception as e:
        print(f"   [解析错误] {e}")
        return None

# --------------------------
# 3. 主循环
# --------------------------
count = 0
for index, row in df.iterrows():
    current_status = str(row['用法用量']).strip()
    target_conditions = ['未找到说明书', '未找到用法用量信息', 'nan', 'None', 'ERROR']

    if current_status in target_conditions or pd.isna(row['用法用量']):
        common_name = row['商品通用名']
        brand = row['品牌（汇总）'] if pd.notna(row['品牌（汇总）']) else ""

        print(f"[{index + 1}/{len(df)}] 正在补全: {common_name} {brand}")

        search_payload = {
            'filters': [
                {'module_id': 803, 'precise': 0, 'value': common_name},
                {'module_id': 804, 'precise': 0, 'value': brand},
            ],
            'per_page': 10,
            'page': 1,
        }

        try:
            # 搜索请求
            resp = requests.post(
                'https://server.pharnexcloud.com/external/medical/databases/159/documents',
                headers=headers,
                json=search_payload,
                timeout=10
            )
            data_list = resp.json().get('data', [])

            if data_list:
                doc = data_list[0]
                file_url = doc.get('html_path')

                if file_url and ('.html' in file_url.lower() or '.htm' in file_url.lower()):
                    print("   -> 下载 HTML...")

                    file_resp = requests.get(
                        'https://server.pharnexcloud.com/external/medical/files/download',
                        headers=headers,
                        params={'url': file_url},
                        timeout=15
                    )
                    file_resp.encoding = 'utf-8'

                    # --- 新增功能：保存 HTML 到本地 ---
                    local_html_path = os.path.join(html_save_dir, f"temp_{index + 1}.html")
                    try:
                        with open(local_html_path, 'w', encoding='utf-8') as f:
                            f.write(file_resp.text)
                        print(f"   -> [文件已保存] {local_html_path}")
                    except Exception as save_err:
                        print(f"   -> [保存失败] {save_err}")
                    # ------------------------------------

                    # 3. 暴力正则解析
                    res = extract_by_text_regex(file_resp.text)

                    if res:
                        df.at[index, '用法用量'] = res
                        print(f"   [成功] 提取到内容: {res[:20]}...")
                        count += 1
                    else:
                        print("   [失败] 正则未匹配到内容")
                        df.at[index, '用法用量'] = "HTML内容未匹配到正则"
                else:
                    print("   -> 跳过: 非HTML文件或URL为空")
            else:
                print("   -> 搜索无结果")

        except Exception as e:
            print(f"   -> 网络或请求异常: {e}")

        time.sleep(0.5)

        if count > 0 and count % 10 == 0:
            df.to_excel(output_file, index=False)
            print("   --- 临时保存 ---")

# --------------------------
# 4. 最终保存
# --------------------------
df.to_excel(output_file, index=False)
print(f"\n补全结束！共修复 {count} 条数据，HTML文件已保存在 '{html_save_dir}' 目录，结果已保存至 {output_file}")