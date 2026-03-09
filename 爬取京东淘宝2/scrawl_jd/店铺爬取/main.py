import requests
from bs4 import BeautifulSoup

cookies = {
    '__jdu': '866395081',
    'shshshfpa': '5dca2291-e9ab-b2da-182d-e0cd7bc31d0a-1754113913',
    'shshshfpx': '5dca2291-e9ab-b2da-182d-e0cd7bc31d0a-1754113913',
    'pinId': 'jR7vs-5qwu1odovT3ljAzg',
    'pin': 'jd_bRvIZDMpattP',
    'unick': 'ii41v7i22kupj2',
    'TrackID': '1hVuoyiTbMirmmCtm7NyD0Xb83lpnTNy0yI1v36dwdPH9UHX3fAPzHWCqhIk0WfmEILlAZCPX_XkdsTVkJampB52ILRErBGqFhvWOjRbPiz6IvFNNv-kDt8a79bpuY7Zf',
    'light_key': 'AASBKE7rOxgWQziEhC_QY6yayYO8ABT3yvm1-Q9Lce7vM_QtKro6xPSzSc6yCj645SvjJq7w',
    'unpl': 'JF8EAK5nNSttUE9TVhkCGUZAG14DWwkLHx9Xam8FBA9bTFMAHVITERN7XlVdWRRLFB9vYRRUXFNPVA4bCysSEXteXVdZDEsWC2tXVgQFDQ8VXURJQlZAFDNVCV9dSRZRZjJWBFtdT1xWSAYYRRMfDlAKDlhCR1FpMjVkXlh7VAQrCxwVEkNZVVddOEonBF9XNVdVWUpdBysDKxMgCQkIWVwPTx4LIm4CU19QT1UMGzIaIhM',
    '__jdv': '76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_956b313eaa2f4e2e9e491ac26647a922|1765939878711',
    'cn': '0',
    'mail_times': '4%2C1%2C1765939879547',
    'PCSYCityID': 'CN_420000_421000_0',
    'areaId': '17',
    'umc_count': '1',
    'thor': '13ABE4FC07154007D62B5628244819113782788DAA7D4C9DE81B9BB00752D8E0088C444352D602A98B3EFC00E02BAC375BAD8C5B2EEBBBE123EAABE94732FDF3A4B485B1BA6CA5230E324CB3C4524F407B60E681AB2FC484FFC5C52DD6F5AEF5DB029162C6B96CCCC367E82A19D8D4AD3BD7B40F5C5AA8031E773D85F532D15AAD05BF8941ABDE3594C937E32E3AE1266FA549067A804E7329DCB1DC8C03D610',
    'ipLoc-djd': '17-1413-1419-7573',
    'o2State': '',
    'hf_time': '1765957908956',
    'JSESSIONID': '5043281A02B31839104B5345D716A1FE.s1',
    '3AB9D23F7A4B3C9B': 'OPC5DL7KBFI2FMD7W2AI6JYVAQAKICJJ7F4KR22FZ5SSHYMQC65RMUK5HAO7PI7SEH5CA3G4VR6FZMUP77DODBRME4',
    '3AB9D23F7A4B3CSS': 'jdd03OPC5DL7KBFI2FMD7W2AI6JYVAQAKICJJ7F4KR22FZ5SSHYMQC65RMUK5HAO7PI7SEH5CA3G4VR6FZMUP77DODBRME4AAAAM3FI4NQEIAAAAACOJV4DZ32XTVY4X',
    'token': '971f1228547fd23b2134d56e1a1d1b6f,3,981077',
    '__jda': '181111935.866395081.1754113909.1765939806.1765939879.35',
    '__jdc': '181111935',
    '__jdb': '181111935.7.866395081|35.1765939879',
    'jsavif': '1',
    'flash': '3_F6DXSCOwXcymEE6MHNoUjacjtyhPcrekbXYk2lXl69WwAjW37Vqh2QbsZXzBFwktJcMDGGs8vt-eeM7o5gjx2ES6LF6e-lHvb9DDCFOTPz1mR-EGjhVJq97BAVuj_m2pAMl1D4f5cwBkGLshSUFxtRW_cjkhRqrzjldcVCyrAb0IAaD5SSEN',
    'shshshfpb': 'BApXW2LUxKf5APIyBG-xcbqrkibrABazQBhZQPjxh9xJ1PdZfQoTkhDPRqAbqMpJnQ6qfW6nnsaxkI71g6a1d4tx9YQ63rp1vhCM',
    'sdtoken': 'AAbEsBpEIOVjqTAKCQtvQu174lMj1w7OWiHh3ZONp4j8pi4OXX0WMqkConKDveL8ZDkwrBYUNC33qk3uqQ7EJD3YXsp3kj0knqA-_tqXLRUN9nSlNZs_hGTFzjr_cqxjk9rWhARsNzqHKyQ9IF7uVSC4V4dEi2UpyYSog2nBHi4',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': '__jdu=866395081; shshshfpa=5dca2291-e9ab-b2da-182d-e0cd7bc31d0a-1754113913; shshshfpx=5dca2291-e9ab-b2da-182d-e0cd7bc31d0a-1754113913; pinId=jR7vs-5qwu1odovT3ljAzg; pin=jd_bRvIZDMpattP; unick=ii41v7i22kupj2; TrackID=1hVuoyiTbMirmmCtm7NyD0Xb83lpnTNy0yI1v36dwdPH9UHX3fAPzHWCqhIk0WfmEILlAZCPX_XkdsTVkJampB52ILRErBGqFhvWOjRbPiz6IvFNNv-kDt8a79bpuY7Zf; light_key=AASBKE7rOxgWQziEhC_QY6yayYO8ABT3yvm1-Q9Lce7vM_QtKro6xPSzSc6yCj645SvjJq7w; unpl=JF8EAK5nNSttUE9TVhkCGUZAG14DWwkLHx9Xam8FBA9bTFMAHVITERN7XlVdWRRLFB9vYRRUXFNPVA4bCysSEXteXVdZDEsWC2tXVgQFDQ8VXURJQlZAFDNVCV9dSRZRZjJWBFtdT1xWSAYYRRMfDlAKDlhCR1FpMjVkXlh7VAQrCxwVEkNZVVddOEonBF9XNVdVWUpdBysDKxMgCQkIWVwPTx4LIm4CU19QT1UMGzIaIhM; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_956b313eaa2f4e2e9e491ac26647a922|1765939878711; cn=0; mail_times=4%2C1%2C1765939879547; PCSYCityID=CN_420000_421000_0; areaId=17; umc_count=1; thor=13ABE4FC07154007D62B5628244819113782788DAA7D4C9DE81B9BB00752D8E0088C444352D602A98B3EFC00E02BAC375BAD8C5B2EEBBBE123EAABE94732FDF3A4B485B1BA6CA5230E324CB3C4524F407B60E681AB2FC484FFC5C52DD6F5AEF5DB029162C6B96CCCC367E82A19D8D4AD3BD7B40F5C5AA8031E773D85F532D15AAD05BF8941ABDE3594C937E32E3AE1266FA549067A804E7329DCB1DC8C03D610; ipLoc-djd=17-1413-1419-7573; o2State=; hf_time=1765957908956; JSESSIONID=5043281A02B31839104B5345D716A1FE.s1; 3AB9D23F7A4B3C9B=OPC5DL7KBFI2FMD7W2AI6JYVAQAKICJJ7F4KR22FZ5SSHYMQC65RMUK5HAO7PI7SEH5CA3G4VR6FZMUP77DODBRME4; 3AB9D23F7A4B3CSS=jdd03OPC5DL7KBFI2FMD7W2AI6JYVAQAKICJJ7F4KR22FZ5SSHYMQC65RMUK5HAO7PI7SEH5CA3G4VR6FZMUP77DODBRME4AAAAM3FI4NQEIAAAAACOJV4DZ32XTVY4X; token=971f1228547fd23b2134d56e1a1d1b6f,3,981077; __jda=181111935.866395081.1754113909.1765939806.1765939879.35; __jdc=181111935; __jdb=181111935.7.866395081|35.1765939879; jsavif=1; flash=3_F6DXSCOwXcymEE6MHNoUjacjtyhPcrekbXYk2lXl69WwAjW37Vqh2QbsZXzBFwktJcMDGGs8vt-eeM7o5gjx2ES6LF6e-lHvb9DDCFOTPz1mR-EGjhVJq97BAVuj_m2pAMl1D4f5cwBkGLshSUFxtRW_cjkhRqrzjldcVCyrAb0IAaD5SSEN; shshshfpb=BApXW2LUxKf5APIyBG-xcbqrkibrABazQBhZQPjxh9xJ1PdZfQoTkhDPRqAbqMpJnQ6qfW6nnsaxkI71g6a1d4tx9YQ63rp1vhCM; sdtoken=AAbEsBpEIOVjqTAKCQtvQu174lMj1w7OWiHh3ZONp4j8pi4OXX0WMqkConKDveL8ZDkwrBYUNC33qk3uqQ7EJD3YXsp3kj0knqA-_tqXLRUN9nSlNZs_hGTFzjr_cqxjk9rWhARsNzqHKyQ9IF7uVSC4V4dEi2UpyYSog2nBHi4',
    'Pragma': 'no-cache',
    'Referer': 'https://mall.jd.com/index-1000000157.html?from=pc',
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

response = requests.get('https://mall.jd.com/index-1000000157.html', cookies=cookies, headers=headers)
# 1. 初始化BeautifulSoup对象
soup = BeautifulSoup(response.text, 'html.parser')  # 也可使用 'lxml' 解析器（需先安装：pip install lxml）

# 2. 方法1：精准匹配href以 //item.jd.com/ 开头且以 .html 结尾的a标签
# 使用CSS选择器（推荐，简洁高效）
target_links = soup.select('a[href^="//item.jd.com/"][href$=".html"]')

# 3. 方法2：正则表达式匹配（更灵活，可适配复杂规则）
import re

pattern = re.compile(r'^//item\.jd\.com/\d+\.html$')  # 匹配数字+html的京东商品链接
target_links_re = soup.find_all('a', href=pattern)

# 4. 提取结果处理
# print("=== 方法1（CSS选择器）提取结果 ===")
# for link in target_links:
#     # 获取href属性
#     href = link.get('href', '')
#     # 补全完整URL（可选）
#     full_url = f'https:{href}' if href.startswith('//') else href
#     # 获取商品价格（可选，提取示例中的价格）
#     price_span = link.find('span', {'preprice': True})
#     price = price_span.get('preprice', '无价格') if price_span else '无价格'
#
#     print(f'商品链接：{full_url}')
#     print(f'商品价格：{price}')
#     print('---')

print("=== 方法2（正则匹配）提取结果 ===")
for link in target_links_re:
    full_url = f'https:{link["href"]}'
    print(f'匹配到的链接：{full_url}')
