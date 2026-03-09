import requests

cookies = {
    'ASP.NET_SessionId': 'wwoad5cqt4fltd11hjcnlw3m',
    'Hm_lvt_72b68c351b528b0e3406619a64d8f8d0': '1757393073',
    'HMACCOUNT': '626E2BA61144DD71',
    'lsjgcxToken': '6E50054E357C53F305D2DD93260D1BCA79DFC0E811AA08183BB05699FCC8BAD19FCE04049AD36BE2EBCA6A56DF326A71AD9E3B3EB7298055C4E969B06C89288D',
    'lsjgcxToken': '6E50054E357C53F305D2DD93260D1BCA79DFC0E811AA08183BB05699FCC8BAD19FCE04049AD36BE2EBCA6A56DF326A71AD9E3B3EB7298055C4E969B06C89288D',
    '69a1a_mmbuser': 'V09xQG5HBVJ4cGhEQFlAU1UwQmd6SG98Ly5%2fADkAVlMFU1VVAABQBQ0HUgBTDAhQBgNVB1FXDl0AVw8IBTg%3d',
    'auth_token': 'bggNSWl3Vi5zYnoHUXBYdDIiVHlhAG1HMgtVAmN0Cw98SFZLeXxfcG5cLiBkBWZlc3ZyYCE1CHBhVnpkJydZZXJUfGFyACU8fFQEcG5HWy9zYFcO',
    'lsjgcx_userdev': '%7b%22FirstDate%22%3a%222025-09-09+12%3a44%3a32%22%2c%22FirstLoginDate%22%3a%222025-09-09+12%3a45%3a13%22%2c%22LastLoginDate%22%3a%222025-09-09+12%3a45%3a13%22%2c%22DevNum%22%3a%2276a9f859e51747b489a7715ce2ff8864%22%7d',
    'Hm_lpvt_72b68c351b528b0e3406619a64d8f8d0': '1757393296',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': 'ASP.NET_SessionId=wwoad5cqt4fltd11hjcnlw3m; Hm_lvt_72b68c351b528b0e3406619a64d8f8d0=1757393073; HMACCOUNT=626E2BA61144DD71; lsjgcxToken=6E50054E357C53F305D2DD93260D1BCA79DFC0E811AA08183BB05699FCC8BAD19FCE04049AD36BE2EBCA6A56DF326A71AD9E3B3EB7298055C4E969B06C89288D; lsjgcxToken=6E50054E357C53F305D2DD93260D1BCA79DFC0E811AA08183BB05699FCC8BAD19FCE04049AD36BE2EBCA6A56DF326A71AD9E3B3EB7298055C4E969B06C89288D; 69a1a_mmbuser=V09xQG5HBVJ4cGhEQFlAU1UwQmd6SG98Ly5%2fADkAVlMFU1VVAABQBQ0HUgBTDAhQBgNVB1FXDl0AVw8IBTg%3d; auth_token=bggNSWl3Vi5zYnoHUXBYdDIiVHlhAG1HMgtVAmN0Cw98SFZLeXxfcG5cLiBkBWZlc3ZyYCE1CHBhVnpkJydZZXJUfGFyACU8fFQEcG5HWy9zYFcO; lsjgcx_userdev=%7b%22FirstDate%22%3a%222025-09-09+12%3a44%3a32%22%2c%22FirstLoginDate%22%3a%222025-09-09+12%3a45%3a13%22%2c%22LastLoginDate%22%3a%222025-09-09+12%3a45%3a13%22%2c%22DevNum%22%3a%2276a9f859e51747b489a7715ce2ff8864%22%7d; Hm_lpvt_72b68c351b528b0e3406619a64d8f8d0=1757393296',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://p.zwjhl.com/price.aspx?url=https://detail.tmall.com/item.htm?id=673981586940&skuId=5096413143473&idays=6',
    'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

params = {
    'url': 'https://detail.tmall.com/item.htm?ali_refid=a3_420434_1006%3A1313280142%3AH%3A1xjsVODqXvwv82PI8ktdLA%3D%3D%3Af10fc6c5016b4724c78caa55ec92918c&ali_trackid=282_f10fc6c5016b4724c78caa55ec92918c&id=790650834799&mi_id=0000BFaMOIHGK01zRPdzhtQlQyiHNVxtjTUJY7Kl6OhNtkk&mm_sceneid=1_0_1232900106_0&skuId=5816083405219&spm=a21n57.1.item.3&utparam=%7B%22aplus_abtest%22%3A%22743049b2a3a7b22bd7ecf186f19a2fb6%22%7D&xxc=ad_ztc',
    'event': 'searchPrice',
}

response = requests.get('https://p.zwjhl.com/price.aspx', params=params, cookies=cookies, headers=headers)
print(response.text)