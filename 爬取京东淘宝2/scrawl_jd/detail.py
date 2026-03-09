import json
import time
import requests
import execjs

ctx = execjs.compile(open('js/reverse.js', 'r', encoding='utf-8').read())

cookies = {
    '__jdu': '866395081',
    'shshshfpa': '5dca2291-e9ab-b2da-182d-e0cd7bc31d0a-1754113913',
    'shshshfpx': '5dca2291-e9ab-b2da-182d-e0cd7bc31d0a-1754113913',
    'jcap_dvzw_fp': '9iBIHlm8x7lQIsr5UGmusDlLzaDCPAE7dHSHlIbE7-iqdZEAKwvCZ1owHHAt-xs4pfEIXlxk97lAoTJgMzJ3tKMewv0=',
    'unpl': 'JF8EAK5nNSttD0kBUhtVSxNDT1RcWwoIGB5XamRRV1wMTlVVTFJMGkR7XlVdWRRKHh9sZhRUWVNPXA4ZBCsSEXteXVdZDEsWC2tXVgQFDQ8VXURJQlZAFDNVCV9dSRZRZjJWBFtdT1xWSAYYRRMfDlAKDlhCR1FpMjVkXlh7VAQrCxwVEkNZVVddOEonBF9XNVZeUENdASsDKxMgCQkIWl0OTREDIm4CU19QT1UMGzIaIhM',
    '__jdv': '181111935|direct|-|none|-|1757997791605',
    'areaId': '17',
    'wlfstk_smdl': 'lg267uivd10sybm86x9wfsqzkhuyt2ff',
    'TrackID': '1THOyx3Xn8L40hmZUFbg2KmuW_aA0qnYf73LWaYI4GbJTh93t-MkXUZUkOi80hv1whP7dkWNfowl0O-_QD54QUcHoyuM6-iyAK6r03BqOz_uxa3laxdTrW3mRHGqgQ2W6',
    'thor': '13ABE4FC07154007D62B5628244819113782788DAA7D4C9DE81B9BB00752D8E05AD63ECAF12DEFEADB0A33D17A03937084EFCBDD1D55B4802F7E8E2E0D664F9530117CAF1929986B258B11631A0D1AFCB217AD467CED19E823FD229776CBC908BF2F1EBDA646CCD6B465BAE539FC0F9B9FF4187F97ECF1F61A2E1E5877E2D4FB413C185DDF07CE68A5DB26D2B9642DC047AE23D8DE1AC4BAE9CAE2E74C4E7113',
    'light_key': 'AASBKE7rOxgWQziEhC_QY6yahVGhHZG7MjSxPMES1WXOFgUTUOXzSV333CJR8ugJQr64pioY',
    'pinId': 'jR7vs-5qwu1odovT3ljAzg',
    'pin': 'jd_bRvIZDMpattP',
    'unick': 'ii41v7i22kupj2',
    'ceshi3.com': '000',
    '_tp': '37euN3SqNS%2FLFYMMmHAsnw%3D%3D',
    '_pst': 'jd_bRvIZDMpattP',
    'ipLoc-djd': '17-1413-1419-7573',
    'mail_times': '4%2C1%2C1757997917904',
    'PCSYCityID': 'CN_420000_421000_0',
    'umc_count': '1',
    'cn': '0',
    '3AB9D23F7A4B3C9B': 'OPC5DL7KBFI2FMD7W2AI6JYVAQAKICJJ7F4KR22FZ5SSHYMQC65RMUK5HAO7PI7SEH5CA3G4VR6FZMUP77DODBRME4',
    'jsavif': '1',
    'flash': '3_flKxGpEQWwCP5D-XBVaNd9MqcrxJD6JaVxziIvfghVypdmjzlZ62q6ToM2Rb-c6hkPbv2wFgFsE60HBaDcb8xLf_nlsgbPi0G2Cc5SxAICn9M1f-GVQa23u3E-svRAZONBSEoytv-ZFHpz5VXgsqkwNveedWEgo1XQrXshs4QpxodceS3TPY',
    '__jda': '181111935.866395081.1754113909.1757997792.1758003011.21',
    '__jdc': '181111935',
    'token': '94f9ded8722f313829a79688a5893110,3,976669',
    '3AB9D23F7A4B3CSS': 'jdd03OPC5DL7KBFI2FMD7W2AI6JYVAQAKICJJ7F4KR22FZ5SSHYMQC65RMUK5HAO7PI7SEH5CA3G4VR6FZMUP77DODBRME4AAAAMZKE5FIIYAAAAADPWYDOGQVYUMPUX',
    '_gia_d': '1',
    '__jdb': '181111935.13.866395081|21.1758003011',
    'shshshfpb': 'BApXSSsIyUvxAPIyBG-xcbqrkibrABazQBhZQPjxs9xJ1MsOckI62',
    'sdtoken': 'AAbEsBpEIOVjqTAKCQtvQu178e2-XxD7RIhSG8QKoTIxXIc_bjXw2lv6Ey6lTA0ryyT2aBunN1E1ZHZ5kY_EXwzRmKNBz9mmJE9909xGMUUMupOq4J8WcVgvq3oj0Q6JPytnajAQKzuY9w',
}
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://item.jd.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://item.jd.com/',
    'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'x-referer-page': 'https://item.jd.com/10108300980915.html',
    'x-rp-client': 'h5_1.0.0',
}
sku = '6235768'
page = "2"
body = {"requestSource":"pc","shopComment":0,"sameComment":0,"channel":'',"extInfo":{"isQzc":"0","spuId":sku,"commentRate":"1","needTopAlbum":"1","bbtf":"","userGroupComment":"1"},"num":"10","pictureCommentType":"A","scval":'',"shadowMainSku":"0","shopType":"0","shopId":"1000282702","firstCommentGuid":"15237c519dcba6e1eab4a876884305f1","sku":sku,"category":"737;752;761","shieldCurrentComment":"1","pageSize":"10","isFirstRequest":False,"isCurrentSku":True,"sortType":"5","tagId":"","tagType":"","type":"0","pageNum":page}


# body = {"requestSource":"pc","shopComment":0,"sameComment":0,"channel":'',"extInfo":{"isQzc":"0","spuId":sku,"commentRate":"1","needTopAlbum":"1","bbtf":"","userGroupComment":"1"},"num":"10","pictureCommentType":"A","scval":'',"shadowMainSku":"0","shopType":"0","firstCommentGuid":"15237c519dcba6e1eab4a876884305f1","sku":sku,"category":"36574;36575;36576","shieldCurrentComment":"1","pageSize":"10","isFirstRequest":False,"style":"1","isCurrentSku":True,"sortType":"5","tagId":"","tagType":"","type":"0","pageNum":page}
body_json = json.dumps(body, ensure_ascii=False,separators=(',', ':'))
print(body_json)
time_str = str(time.time()*1000)
res = ctx.call('getH5st', body_json,time_str)
print(res['h5st'])


data = {
    'appid': 'pc-rate-qa',
    'body': body_json,
    'client': 'pc',
    'clientVersion': '1.0.0',
    'functionId': 'getCommentListPage',
    'h5st': res['h5st'],
    'loginType': '3',
    't': time_str,
    'uuid': '866395081',
}

response = requests.post('https://api.m.jd.com/client.action', cookies=cookies, headers=headers, data=data)

print(response.status_code)
print(response.json())
if response.status_code == 200:
    json_data = response.json().get('result')
    if json_data:
        # 遍历所有floors
        for floor in json_data['floors']:
            # 检查是否是评论列表的floor
            if floor.get('mId') == 'commentlist-list' and 'data' in floor:
                # 遍历每条评论
                for item in floor['data']:
                    if 'commentInfo' in item and 'commentData' in item['commentInfo']:
                        print(item['commentInfo']['commentData'])
    else:
        print('报错了')
