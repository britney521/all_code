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
if '用法用量' not in df.columns:
    df['用法用量'] = None

# 请求头 (保持你提供的 Header)
headers = {
    'accept': 'application/x.myapp.v1+json',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc2VydmVyLnBoYXJuZXhjbG91ZC5jb21cL2V4dGVybmFsXC9hdXRoZW50aWNhdGVcL2F1dGhvcml6YXRpb25zIiwiaWF0IjoxNzcwMTIzNzg4LCJleHAiOjE3NzAxNTI1ODgsIm5iZiI6MTc3MDEyMzc4OCwianRpIjoiM3ZnU1ZSV2wxMWZhdWthWiIsInN1YiI6MjE0NzMzLCJwcnYiOiJkZjY4MjExYmRhNjQwNGRkNjRhMWZkZDAyZjJiMjE5OTFlOGI2MTM0Iiwibmlja25hbWUiOm51bGx9.gmU0FUDBbCMV8cmEWCGmCF1upY4uQHittOQsqRHtiis',
    # 注意：Token 可能会过期
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://data.pharnexcloud.com',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}


# --------------------------
# 2. 功能函数定义
# --------------------------

def extract_from_html(html_content):
    """从 HTML 文本中提取用法用量（兼容 Table、Div 和 纯文本结构）"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # 关键词列表
        keywords = ["用法用量", "用法与用量"]

        # -------------------------------------------------------
        # 策略 1: 查找表格结构 (th -> td)
        # -------------------------------------------------------
        target_th = soup.find('th', string=lambda text: text and any(k in text for k in keywords))
        if target_th:
            next_td = target_th.find_next_sibling('td')
            if next_td:
                print("   [调试] 命中策略 1: 表格结构")
                return next_td.get_text(strip=True)

        # -------------------------------------------------------
        # 策略 2: 查找 DIV/段落结构 (div/h/p -> next_sibling)
        # -------------------------------------------------------
        potential_tags = ['div', 'p', 'span', 'h3', 'h4', 'strong', 'b']
        targets = soup.find_all(potential_tags)
        for tag in targets:
            text = tag.get_text(strip=True)
            # 标题必须包含关键词，且长度短（避免匹配到正文）
            if any(k in text for k in keywords) and len(text) < 20:
                next_node = tag.find_next_sibling()
                if next_node:
                    print("   [调试] 命中策略 2: DIV/段落结构")
                    return next_node.get_text(strip=True)

        # -------------------------------------------------------
        # 策略 3: 全文正则提取 (针对您刚才发的这种大段文本)
        # -------------------------------------------------------
        # 1. 获取纯文本，用换行符分隔，保留段落感
        full_text = soup.get_text(separator="\n", strip=True)

        # 2. 定义正则：寻找 “【用法用量】” 开头，直到遇到下一个 “【” 或 “不良反应” 等关键词
        # 解释：
        # (?:【|^)      -> 开头可能是 【 或者 行首
        # (用法.*?)     -> 匹配 用法用量 或 用法与用量
        # (?:】|[:：])? -> 结尾可能是 】 或者 冒号，也可能没有
        # \s* -> 允许有空格
        # (.*?)         -> 【核心内容】(非贪婪匹配)
        # (?= ... )     -> 截止条件(正向预查)：遇到下个【，或遇到“不良反应”等词，或文件结束
        pattern = r"(?:【|^)\s*(?:用法用量|用法与用量)(?:】|[:：])?\s*(.*?)(?=\n?\s*(?:【|\[|不良反应|禁忌|注意事项|规格|贮藏|有效期|批准文号)|$)"

        match = re.search(pattern, full_text, re.DOTALL | re.IGNORECASE)

        if match:
            print("   [调试] 命中策略 3: 全文正则提取")
            return match.group(1).strip()

    except Exception as e:
        print(f"HTML 解析出错: {e}")

    return None


# def extract_from_image(temp_img_name):
#     """保存图片 -> OCR 识别 -> 正则提取"""
#
#
#     try:
#         # 2. 进行 OCR 识别
#         # 注意：标准 PaddleOCR 库使用 .ocr() 方法，而不是 .predict()
#         result = ocr.predict(temp_img_name)
#
#         if not result or not result[0]:
#             return None
#
#         # 3. 拼接文本 (使用换行符拼接，利于正则匹配)
#         rec_texts = result[0]['rec_texts']  # list[str]
#         all_txt = " ".join(rec_texts)
#
#         # 4. 正则提取
#         # 匹配 "用法用量" 或 "用法与用量" 开头，直到遇到下一个大标题
#         pattern = r"(用法用量|用法与用量)[:：]?\s*(.*?)(?=\n\s*(不良反应|禁忌|注意事项|规格|贮藏|有效期|批准文号)|$)"
#         match = re.search(pattern, all_txt, re.DOTALL)
#
#         if match:
#             return match.group(2).strip()
#
#     except Exception as e:
#         print(f"图片识别出错: {e}")
#
#     return None


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

            if file_url:
                # --- 分支 A: HTML 处理 (走下载接口) ---
                # 使用 'in' 判断，防止 URL 带参数导致 endswith 失效
                print("   -> 类型判断: HTML (调用下载接口)")
                file_resp = requests.get(
                    'https://server.pharnexcloud.com/external/medical/files/download',
                    headers=headers,
                    params={'url': file_url}
                )
                file_resp.encoding = 'utf-8'  # 防止乱码

                res = extract_from_html(file_resp.text)
                if res: extracted_content = res
            elif relative_path:
                imgheaders = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
                    'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"macOS"',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Site': 'cross-site',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-User': '?1',
                    'Sec-Fetch-Dest': 'document',
                    'Referer': 'https://data.pharnexcloud.com/',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                }
                print("   -> 类型判断: 图片 (直接下载)")
                file_resp1 = requests.get(
                    relative_path,
                    headers=imgheaders  # 图片直链通常也需要鉴权头? 如果不需要可去掉
                )
                temp_img_name = f"img/temp_{index + 1}.png"
                extracted_content = '代读取图片'
                # 1. 保存为临时文件 (PaddleOCR 需要文件路径)
                with open(temp_img_name, 'wb') as f:
                    f.write(file_resp1.content)
                # res = extract_from_image(temp_img_name)
                # if res:
                #     extracted_content = res
            else:
                print(f"   -> 未知文件类型: {file_url}")
                extracted_content = "不支持的文件格式"
        else:
            print("   -> 未找到相关文档数据")

        # 4. 写入 DataFrame
        df.at[index, '用法用量'] = extracted_content
        print(f"   -> 提取结果: {extracted_content[:30]}...")

    except Exception as e:
        print(f"   -> 处理该行时发生错误: {e}")
        df.at[index, '用法用量'] = "ERROR"

    # 5. 实时保存 (防止程序中途崩溃数据丢失)
    if index % 5 == 0:
        df.to_excel('【用法用量】结果_temp.xlsx', index=False)

    # 礼貌性延时


# --------------------------
# 4. 最终保存
# --------------------------
output_filename = '【用法用量】提取完成.xlsx'
df.to_excel(output_filename, index=False)
print(f"\n全部完成！结果已保存至 {output_filename}")
