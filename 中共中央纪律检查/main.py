import os
import re

import requests
from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

cookies = {
    'HMF_CI': 'f88889522e6fd9c69ac7618c7c46d319d9792b481fecbd7a9c0c53d95f057963ff9a6473605de2d5ce97275e72fed5dc8be86a6978f9fa716cf09e015302559e45',
    'HMY_JC': '17492a92dee67d480ad423606b34ed378de46fb80fe542e421e99da73031f0aa0e,',
    '_gscu_1507282980': '60339397tyj9qm21',
    '_gscbrs_1507282980': '1',
    'HBB_HC': 'f303a99eea2bfd4bd06c7264bfe1aef222ff379f5c5bc134a483a1e1c624f293aa98f3dd285af0219be61da9d5cdbff9fb',
    '_trs_uv': 'mgosn5vz_5312_fhqk',
    '_trs_ua_s_1': 'mgosn5vy_5312_im0x',
    '_gscs_1507282980': '60339397qg17s021|pv:5',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'HMF_CI=f88889522e6fd9c69ac7618c7c46d319d9792b481fecbd7a9c0c53d95f057963ff9a6473605de2d5ce97275e72fed5dc8be86a6978f9fa716cf09e015302559e45; HMY_JC=17492a92dee67d480ad423606b34ed378de46fb80fe542e421e99da73031f0aa0e,; _gscu_1507282980=60339397tyj9qm21; _gscbrs_1507282980=1; HBB_HC=f303a99eea2bfd4bd06c7264bfe1aef222ff379f5c5bc134a483a1e1c624f293aa98f3dd285af0219be61da9d5cdbff9fb; _trs_uv=mgosn5vz_5312_fhqk; _trs_ua_s_1=mgosn5vy_5312_im0x; _gscs_1507282980=60339397qg17s021|pv:5',
    'Pragma': 'no-cache',
    'Referer': 'https://www.ccdi.gov.cn/llxx/index_1.html',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}
from bs4 import BeautifulSoup, NavigableString
response = requests.get('https://www.ccdi.gov.cn/llxx/202509/t20250911_446754.html', cookies=cookies, headers=headers)
response.encoding = 'utf-8'
print(response.text)
with open('your.html','w', encoding='utf-8') as f:
    f.write(response.text)
soup = BeautifulSoup(response.text, 'html.parser')
article_div = soup.select_one('div.Article_61')
from htmldocx import HtmlToDocx

# ---------- 关键：Tag → 字符串 ----------
html_fragment = str(article_div)          # 或者 article_div.prettify()
# 包一层根节点（可选，但推荐）
html_whole = f'<body>{html_fragment}</body>'

# ---------- 转换 ----------
new_parser = HtmlToDocx()
new_parser.parse_html_string(html_whole)
new_parser.doc.save('htmldoc.docx')
print('已保存 → htmldoc.docx')

# from html2docx import html2docx
# with open('your.html','r', encoding='utf-8') as f:
#     html = f.read()
# docx_bytes = html2docx(html, title='转Word')
# with open('out.docx', 'wb') as f:
#     f.write(docx_bytes.getvalue())
