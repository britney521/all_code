import csv
import json
import time
from requestsretry import request_with_retry
from bs4 import BeautifulSoup
import re


def get_detail(url):
    response = request_with_retry(
        'get',
        url=url,
        cookies=cookies,
        headers=headers,
    )
    # 创建BeautifulSoup对象
    page_html = response.text
    soup = BeautifulSoup(page_html, "html.parser")
    detail_info = {
        "党派": "",
        "代表团": "",
        "工作单位": "",
        "职务": "",
        "代表建议内容": "",
        "建议答复单位": "",
        "代表建议答复": "",
        "答复日期": ""
    }

    # 1. 提取代表建议正文（问题分析 + 对策建议）
    content_div = soup.find("div", class_="lfzqkuang")
    if not content_div:
        return detail_info

    all_p = content_div.find_all("p")
    split_idx = None

    # 仅保留指定的3个分割关键字
    split_keywords = ["代表建议答复", "承办单位的答复", "结果反馈"]
    # 第一步：遍历查找任意一个分割关键字，找到第一个匹配的即可
    for i, p in enumerate(all_p):
        p_text = p.get_text(strip=True)
        # 检查当前p标签是否包含任意一个分割关键字
        if any(keyword in p_text for keyword in split_keywords):
            split_idx = i
            break

    # 代表建议内容：从开头到分割关键字之前
    if split_idx is not None:
        content_p_list = all_p[:split_idx]
        content_text = "\n".join(p.get_text(strip=True) for p in content_p_list)
        detail_info["代表建议内容"] = content_text.strip()

        # 答复部分：从分割关键字之后开始
        reply_p_list = all_p[split_idx:]
        reply_text_list = []
        # 记录“承办单位”所在的索引，用于后续取下行内容
        dept_p_index = None

        for idx, p in enumerate(reply_p_list):
            t = p.get_text(strip=True)
            if not t:
                continue

            # 【核心修改】先标记“承办单位”所在行的索引，不直接提取
            if "承办单位" in t:
                dept_p_index = idx  # 记录当前行在reply_p_list中的索引

            # 提取答复日期（仅匹配符合格式的日期）
            if re.match(r"\d{4}年\d{1,2}月\d{1,2}日", t):
                detail_info["答复日期"] = t

            # 收集答复正文（排除所有分割关键字行、承办单位行、日期行）
            exclude_conditions = [
                any(keyword in t for keyword in split_keywords),  # 排除3个分割关键字行
                "承办单位" in t,  # 排除“承办单位”行本身
                p.get("style") and "text-align: right" in p.get("style") and re.match(r"\d{4}年\d{1,2}月\d{1,2}日", t)
                # 排除日期行
            ]
            if not any(exclude_conditions):
                reply_text_list.append(t)

        # 【核心修改】从“承办单位”下一个p标签提取建议答复单位
        if dept_p_index is not None and (dept_p_index + 1) < len(reply_p_list):
            next_p = reply_p_list[dept_p_index + 1]
            detail_info["建议答复单位"] = next_p.get_text(strip=True)

        detail_info["代表建议答复"] = "\n".join(reply_text_list).strip()
    else:
        # 场景2：无分割关键字——所有内容归为代表建议内容，答复字段留空
        all_content_text = "\n".join(p.get_text(strip=True) for p in all_p)
        detail_info["代表建议内容"] = all_content_text.strip()
        # 答复相关字段强制留空
        detail_info["建议答复单位"] = ""
        detail_info["代表建议答复"] = ""
        detail_info["答复日期"] = ""

    # 2. 提取代表个人信息（兼容顿号/逗号拆分工作单位和职务）
    info_boxes = soup.find_all("div", class_="weiyuanhui-jiagou")
    for box in info_boxes:
        p_tags = box.find_all("p")
        for p in p_tags:
            p_text = p.get_text(strip=True)
            if not p_text:
                continue
            if "党派：" in p_text:
                detail_info["党派"] = p_text.replace("党派：", "").strip()
            elif "代表团：" in p_text:
                detail_info["代表团"] = p_text.replace("代表团：", "").strip()
            elif "工作单位和职务：" in p_text:
                work_info = p_text.replace("工作单位和职务：", "").strip()
                # 兼容顿号(、)和逗号(，)，只拆分第一次出现的分隔符
                if "、" in work_info:
                    split_result = work_info.split("、", 1)
                elif "，" in work_info:
                    split_result = work_info.split("，", 1)
                else:
                    # 无分隔符时，默认全部为职务，工作单位留空
                    split_result = ["", work_info]

                # 赋值（防止索引越界）
                detail_info["工作单位"] = split_result[0].strip() if len(split_result) > 0 else ""
                detail_info["职务"] = split_result[1].strip() if len(split_result) > 1 else work_info.strip()

    return detail_info

base_url = 'https://www.shrd.gov.cn/'
cookies = {
    'Hm_lvt_3bd83c7cf65d9651b52511ea2cdcdfd5': '1772456257',
    'HMACCOUNT': '221DCC5A65DE2271',
    '_pk_testcookie.149.5229': '1',
    '_pk_ses.149.5229': '1',
    '_pk_id.149.5229': '313efabd63864b94.1772456257.1.1772456358.1772456257.',
    'Hm_lpvt_3bd83c7cf65d9651b52511ea2cdcdfd5': '1772456358',
}

headers = {
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'Hm_lvt_3bd83c7cf65d9651b52511ea2cdcdfd5=1772456257; HMACCOUNT=221DCC5A65DE2271; _pk_testcookie.149.5229=1; _pk_ses.149.5229=1; _pk_id.149.5229=313efabd63864b94.1772456257.1.1772456358.1772456257.; Hm_lpvt_3bd83c7cf65d9651b52511ea2cdcdfd5=1772456358',
    'Pragma': 'no-cache',
    'Referer': 'https://www.shrd.gov.cn/shrd/2025n/2025n.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

csv_headers = [
    "年份","建议编号", "建议名称", "提出代表", "党派", "代表团",
    "工作单位", "职务", "代表建议内容", "主办单位",
    "建议答复单位", "代表建议答复", "答复日期",'链接'
]
# ===================== 第三步：写入CSV文件 =====================
csv_filename = "代表建议数据2.csv"
csvfile = open(csv_filename, 'w', encoding='utf-8-sig', newline='')
# 创建CSV写入器
writer = csv.writer(csvfile)
# 写入列头
writer.writerow(csv_headers)

columnIds = ['593f0397-04d7-44c3-8339-240a77a793ce','855a92bd-465f-4f48-aafd-567a2b19a150']
years = [2024,2025]
for index,axx in enumerate(columnIds):
    year = years[index]
    for page in range(1, 1000):
        params = {
            'startrecord': str(1 + (page-1)*10),
            'endrecord': str(page*10),
            'perpage': '10',
            'contentTemplate': '',
            'columnId': axx, # columnId  '593f0397-04d7-44c3-8339-240a77a793ce'
            '_': str(int(time.time()*1000)),
        }

        response = request_with_retry(
            'get',
            url = 'https://www.shrd.gov.cn/TrueCMS/messageController/getMessage.do',
            params=params,
            cookies=cookies,
            headers=headers,
        )

        result = json.loads(response.text)['result']
        # 第一步：解析外层XML结构，提取所有record标签
        xml_soup = BeautifulSoup(result, 'html.parser')
        records = xml_soup.find_all('record')

        if len(records) == 0:
            print(f'到末尾页面{page}')
            break
        # 存储所有提案信息的列表
        all_proposals = []
        print(f'第{page}页{len(records)}个--------------')
        # 第二步：遍历每个record，解析其中的CDATA内容
        for record in records:
            # 提取CDATA中的HTML内容（去除CDATA标记）
            cdata_content = record.text.strip()

            # 第三步：解析CDATA内的HTML片段
            html_soup = BeautifulSoup(cdata_content, 'html.parser')
            li_tag = html_soup.find('li')

            # 序号
            serial_number = li_tag.find('div', class_='yajytable2').get_text(strip=True)
            # 提案人
            proposer = li_tag.find('div', class_='yajytable3').get_text(strip=True)
            # 提案标题和链接
            a_tag = li_tag.find('div', class_='yajytable1').find('a')
            title = a_tag.get_text(strip=True)
            link = a_tag.get('href', '')
            # 承办单位
            undertaking_unit = li_tag.find('div', class_='yajytable4').get_text(strip=True)

            proposal_info = get_detail(base_url + link)
            print(serial_number, proposer, title, link, undertaking_unit)

            writer.writerow([year,serial_number,title,proposer,proposal_info['党派'],proposal_info['代表团'],proposal_info['工作单位'],proposal_info['职务'],proposal_info['代表建议内容'],undertaking_unit,proposal_info['建议答复单位'],proposal_info['代表建议答复'],proposal_info['答复日期'],base_url + link])
