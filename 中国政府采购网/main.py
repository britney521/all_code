
import requests

cookies = {
    'HMF_CI': '22b4f4cadbf130c491186a2c4643995b263ca688f0281813aa00b87311ca1437db9fa6a95e24a80945e5f1301bde8cfe2b91e572db472a50d60d468ef96723266f',
    'Hm_lvt_9459d8c503dd3c37b526898ff5aacadd': '1766577439',
    'HMACCOUNT': '359E67092891F7A4',
    'JSESSIONID': 'TyVQfHe0lsNpU1AzA0efFE2CZ6Uw8v0y7S5IJuWIuYyprI98LJF3!-61981476',
    'HMY_JC': '17623cad7a8c5f167d334c7b03470c357832a9f563f7c5ae4154a0498284280047,',
    'HBB_HC': 'dfc11011563587ed9483414cb8e098b27ede55c3d615406477eaaf627606f8a693844e87cb47d93722f62c7961f0f8b0fa',
    'Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd': '1766581916',
    'CSH_DF': '1WFDZU0D0pBooeED8rE1LLcOWTxUaIF3wRcMXoYKVbe9H/ZYpfRUIMv8ADO14mIg10',
    'CSH_UF': 'fe0673f2a48d047b912b27e2a0c02f9f',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'HMF_CI=22b4f4cadbf130c491186a2c4643995b263ca688f0281813aa00b87311ca1437db9fa6a95e24a80945e5f1301bde8cfe2b91e572db472a50d60d468ef96723266f; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1766577439; HMACCOUNT=359E67092891F7A4; JSESSIONID=TyVQfHe0lsNpU1AzA0efFE2CZ6Uw8v0y7S5IJuWIuYyprI98LJF3!-61981476; HMY_JC=17623cad7a8c5f167d334c7b03470c357832a9f563f7c5ae4154a0498284280047,; HBB_HC=dfc11011563587ed9483414cb8e098b27ede55c3d615406477eaaf627606f8a693844e87cb47d93722f62c7961f0f8b0fa; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1766581916; CSH_DF=1WFDZU0D0pBooeED8rE1LLcOWTxUaIF3wRcMXoYKVbe9H/ZYpfRUIMv8ADO14mIg10; CSH_UF=fe0673f2a48d047b912b27e2a0c02f9f',
    'Pragma': 'no-cache',
    'Referer': 'https://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=2&bidSort=&buyerName=&projectId=&pinMu=&bidType=&dbselect=bidx&kw=&start_time=2025%3A06%3A25&end_time=2025%3A12%3A24&timeType=5&displayZone=&zoneId=&pppStatus=0&agentName=',
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

params = {
    'searchtype': '1',
    'page_index': '1',
    'bidSort': '',
    'buyerName': '',
    'projectId': '',
    'pinMu': '',
    'bidType': '',
    'dbselect': 'bidx',
    'kw': '',
    'start_time': '2025:06:25',
    'end_time': '2025:12:24',
    'timeType': '5',
    'displayZone': '',
    'zoneId': '',
    'pppStatus': '0',
    'agentName': '',
}

response = requests.get('https://search.ccgp.gov.cn/bxsearch', params=params, cookies=cookies, headers=headers)
print(response.text)