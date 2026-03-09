import requests

cookies = {
    '_xmLog': 'h5&6f501645-1a36-447e-ab2d-a2bac9ff6085&process.env.sdkVersion',
    'wfp': 'ACM4MjdlYTExMWI4N2ZiMDc5XQIGu3GKBpZ4bXdlYl93d3c',
    'web_login': '1757216803460',
    'HWWAFSESID': 'a192e15aeb11bd6c14c',
    'HWWAFSESTIME': '1757216997092',
    'DATE': '1757211553689',
    'crystal': 'U2FsdGVkX1+x/d6TMZw451upXt9UxKkrR0O5/6FrjkLefN/jNYThMo0u+jOQrvNi3G9bgA0B+5NDmCbQwUM3ZwGJesc84sbpKrCZ42sfpZ1sr+3u0nENj1Gf7dfNFNm2UHU0pb5FVLlHc9nveWi3o4jZXs60KNyeAiAE182hyMa/Wj07j3xY1xvjDIIZOEJRW+2/QkOAv0E9lxIe3JAR24PNLFiBWTC6bDIDbYzzglyWMF/CU+lpR8AzF8cYj4GQ',
    'xm-page-viewid': 'ximalaya-web',
    'Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070': '1757214327,1757216957,1757216983,1757216999',
    'HMACCOUNT': '85193C6041AF0AE8',
    'impl': 'www.ximalaya.com.login',
    'vmce9xdq': 'U2FsdGVkX1+w70MjVc7FHzur/i6+p6WqGR80utZysmtQZrO2UC0QblDLJRDwiuxVqnMCoJX4ybUBwJUzDewJwn74wk3cnNr7XOk+rH3ikdEikSU+r2wBNqoDJ+qARsngC80XjEgGHPq02yVUyLm2pUqp/xxh/4yrDdxDSDjqQpI=',
    'cmci9xde': 'U2FsdGVkX19kDkzWukvUA9kg3LTx+yt+uhZftZf0BoZ9m6cPbEiEj65FSeToKTLVwUsaKl1bsffxn0nkb72fGw==',
    'pmck9xge': 'U2FsdGVkX18yeYBPMwRMLbiqymFSTVZvkDvjCs6A548=',
    'assva6': 'U2FsdGVkX1828OSj0idlbdDp4ukdt/95kAeNVpcCMhc=',
    'assva5': 'U2FsdGVkX1+qJ3RCpI16elHdIZdA8R15x+PwTpL8xe6DGRJ5k+ZUBHY/8hh9B/mdYgtzhOzYw6iH5W+JuGtn7w==',
    'Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070': '1757217013',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    # 'Cookie': '_xmLog=h5&6f501645-1a36-447e-ab2d-a2bac9ff6085&process.env.sdkVersion; wfp=ACM4MjdlYTExMWI4N2ZiMDc5XQIGu3GKBpZ4bXdlYl93d3c; web_login=1757216803460; HWWAFSESID=a192e15aeb11bd6c14c; HWWAFSESTIME=1757216997092; DATE=1757211553689; crystal=U2FsdGVkX1+x/d6TMZw451upXt9UxKkrR0O5/6FrjkLefN/jNYThMo0u+jOQrvNi3G9bgA0B+5NDmCbQwUM3ZwGJesc84sbpKrCZ42sfpZ1sr+3u0nENj1Gf7dfNFNm2UHU0pb5FVLlHc9nveWi3o4jZXs60KNyeAiAE182hyMa/Wj07j3xY1xvjDIIZOEJRW+2/QkOAv0E9lxIe3JAR24PNLFiBWTC6bDIDbYzzglyWMF/CU+lpR8AzF8cYj4GQ; xm-page-viewid=ximalaya-web; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1757214327,1757216957,1757216983,1757216999; HMACCOUNT=85193C6041AF0AE8; impl=www.ximalaya.com.login; vmce9xdq=U2FsdGVkX1+w70MjVc7FHzur/i6+p6WqGR80utZysmtQZrO2UC0QblDLJRDwiuxVqnMCoJX4ybUBwJUzDewJwn74wk3cnNr7XOk+rH3ikdEikSU+r2wBNqoDJ+qARsngC80XjEgGHPq02yVUyLm2pUqp/xxh/4yrDdxDSDjqQpI=; cmci9xde=U2FsdGVkX19kDkzWukvUA9kg3LTx+yt+uhZftZf0BoZ9m6cPbEiEj65FSeToKTLVwUsaKl1bsffxn0nkb72fGw==; pmck9xge=U2FsdGVkX18yeYBPMwRMLbiqymFSTVZvkDvjCs6A548=; assva6=U2FsdGVkX1828OSj0idlbdDp4ukdt/95kAeNVpcCMhc=; assva5=U2FsdGVkX1+qJ3RCpI16elHdIZdA8R15x+PwTpL8xe6DGRJ5k+ZUBHY/8hh9B/mdYgtzhOzYw6iH5W+JuGtn7w==; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1757217013',
    'Referer': 'https://www.ximalaya.com/album/61310701',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

params = {
    'albumId': '61310701',
}

response = requests.get('https://www.ximalaya.com/revision/album/v1/simple', params=params, headers=headers)
print(response.json())

# def login():
#     logger.info(f'检测需要登入')
#     login_btn.click()
#     tab.wait(2)
#     scran_img = tab.ele('css:.qrcode-login__qrcode')
#     s_style = scran_img.attr('style') or ''
#
#     m = re.search(r'background-image:\s*url\(["\']?(.*?)["\']?\)', s_style)
#     if m:
#         data_uri = m.group(1)               # 整段 data:image/...;base64,xxxxx
#         logger.info(f'获取图片二维码')
#         header, b64 = data_uri.split(',', 1)  # 只要逗号后面的纯 base64
#         img_bytes = base64.b64decode(b64)
#
#         img = Image.open(io.BytesIO(img_bytes))
#         plt.imshow(img)
#         plt.axis('off')
#         plt.show()
#         while check_login():
#             tab.wait(5)
#             logger.info(f'请扫码登入')