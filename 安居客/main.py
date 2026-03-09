import requests
from bs4 import BeautifulSoup

cookies = {
    'SECKEY_ABVK': 'Ntp2xxhYvHjffb7vZtcNg6tOcZrnEPZancJTajbOAe8i/IaiCqJckxMaDXfQupUx/DRGuCnceCt6Roy5j5Qb3A%3D%3D',
    'BMAP_SECKEY': 'Ntp2xxhYvHjffb7vZtcNg6tOcZrnEPZancJTajbOAe_JDOBtRmKO8kCzZCOVXXg7x-jSLoIp872KKfGPdHOjYxFzUTQNFMx13ChephAsAKufUtefYG9UyEW7nPP2o0mUDhHAYKRIoQLLTiMCxjOxus33Idly9yyGVpQk9kf1P9TiR3kt0PowWTMFkXMeJVcI0ZFAmIPX7PSICyWcBZj37A',
    'xxzlclientid': '562e5da6-d921-44cf-a1cd-1740225682374',
    'xxzlxxid': 'pfmxmoY1lcQrkUhPz4yUM5pAFTpAaVxJgeDzywclqcIjmeRPxn5pxNm33F+qLWhBV6J2',
    'id58': 'dx6yyWfRaG+h2aGEBNNLAg==',
    'sessid': '9DA93950-8E98-B5A2-CF27-EA09557B4493',
    'aQQ_ajkguid': 'C896030D-9916-C0C9-FD18-F21983F6DBF8',
    'twe': '2',
    'id58': 'dzfKlmfRaIWe/VXdBMXvAg==',
    '58tj_uuid': '106c81ab-3fb5-4a46-9685-63b9273cbb71',
    'new_session': '1',
    'init_refer': 'https%253A%252F%252Fcn.bing.com%252F',
    'new_uv': '1',
    '_ga': 'GA1.2.1727734397.1741777029',
    '_gid': 'GA1.2.1989352947.1741777029',
    '_gat': '1',
    'als': '0',
    '_ga_DYBJHZFBX2': 'GS1.2.1741777030.1.0.1741777030.0.0.0',
    'ajk-appVersion': '',
    'ctid': '14',
    'fzq_h': '49f2b5985d8143ed34f73a475449545c_1741777038709_bb10ef60a8294584aea0f271c9df624a_47924969134346565870534546843061381792',
    'obtain_by': '2',
    'lps': 'https%3A%2F%2Fbj.zu.anjuke.com%2F%3Ffrom%3DHomePage_TopBar%7Chttps%3A%2F%2Fbeijing.anjuke.com%2F',
    'cmctid': '1',
    'wmda_session_id_6289197098934': '1741777040553-bbd693a0-4061-a0d3',
    'wmda_visited_projects': '%3B6289197098934',
    'wmda_uuid': '1a9eeccbdc626e8412911bb70460dd2f',
    'wmda_new_uuid': '1',
    'xxzlbbid': 'pfmbM3wxMDM1MXwxLjEwLjF8MTc0MTc3NzA0NjAyMTI3MTgxNHxLZlAxUWZldFllZWhPeW1GeTIwL2F6Q2pGYVJsTTNvV3FPRHRBY1J0UEdBPXw4MDE3Y2QyMWM0YTc0MThiZmNmZDM3NjJmOGQwYzUzZV8xNzQxNzc3MDQ2NTg5XzQ0ZTlhZGI0MmRhNDRmNTBiMzI1YTA1NThkNzJkNTU2XzQ3OTI0OTY5MTM0MzQ2NTY1ODcwNTM0NTQ2ODQzMDYxMzgxNzkyfGVlZjg4ZDViYTE1YzBmMWFjNDM4NDZlMjExMDk4NzkxXzE3NDE3NzcwNDU3NTJfMjU0',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://bj.zu.anjuke.com/?from=HomePage_TopBar',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'SECKEY_ABVK=Ntp2xxhYvHjffb7vZtcNg6tOcZrnEPZancJTajbOAe8i/IaiCqJckxMaDXfQupUx/DRGuCnceCt6Roy5j5Qb3A%3D%3D; BMAP_SECKEY=Ntp2xxhYvHjffb7vZtcNg6tOcZrnEPZancJTajbOAe_JDOBtRmKO8kCzZCOVXXg7x-jSLoIp872KKfGPdHOjYxFzUTQNFMx13ChephAsAKufUtefYG9UyEW7nPP2o0mUDhHAYKRIoQLLTiMCxjOxus33Idly9yyGVpQk9kf1P9TiR3kt0PowWTMFkXMeJVcI0ZFAmIPX7PSICyWcBZj37A; xxzlclientid=562e5da6-d921-44cf-a1cd-1740225682374; xxzlxxid=pfmxmoY1lcQrkUhPz4yUM5pAFTpAaVxJgeDzywclqcIjmeRPxn5pxNm33F+qLWhBV6J2; id58=dx6yyWfRaG+h2aGEBNNLAg==; sessid=9DA93950-8E98-B5A2-CF27-EA09557B4493; aQQ_ajkguid=C896030D-9916-C0C9-FD18-F21983F6DBF8; twe=2; id58=dzfKlmfRaIWe/VXdBMXvAg==; 58tj_uuid=106c81ab-3fb5-4a46-9685-63b9273cbb71; new_session=1; init_refer=https%253A%252F%252Fcn.bing.com%252F; new_uv=1; _ga=GA1.2.1727734397.1741777029; _gid=GA1.2.1989352947.1741777029; _gat=1; als=0; _ga_DYBJHZFBX2=GS1.2.1741777030.1.0.1741777030.0.0.0; ajk-appVersion=; ctid=14; fzq_h=49f2b5985d8143ed34f73a475449545c_1741777038709_bb10ef60a8294584aea0f271c9df624a_47924969134346565870534546843061381792; obtain_by=2; lps=https%3A%2F%2Fbj.zu.anjuke.com%2F%3Ffrom%3DHomePage_TopBar%7Chttps%3A%2F%2Fbeijing.anjuke.com%2F; cmctid=1; wmda_session_id_6289197098934=1741777040553-bbd693a0-4061-a0d3; wmda_visited_projects=%3B6289197098934; wmda_uuid=1a9eeccbdc626e8412911bb70460dd2f; wmda_new_uuid=1; xxzlbbid=pfmbM3wxMDM1MXwxLjEwLjF8MTc0MTc3NzA0NjAyMTI3MTgxNHxLZlAxUWZldFllZWhPeW1GeTIwL2F6Q2pGYVJsTTNvV3FPRHRBY1J0UEdBPXw4MDE3Y2QyMWM0YTc0MThiZmNmZDM3NjJmOGQwYzUzZV8xNzQxNzc3MDQ2NTg5XzQ0ZTlhZGI0MmRhNDRmNTBiMzI1YTA1NThkNzJkNTU2XzQ3OTI0OTY5MTM0MzQ2NTY1ODcwNTM0NTQ2ODQzMDYxMzgxNzkyfGVlZjg4ZDViYTE1YzBmMWFjNDM4NDZlMjExMDk4NzkxXzE3NDE3NzcwNDU3NTJfMjU0',
}

params = {
    'isauction': '2',
    'shangquan_id': '6906',
    'legoFeeUrl': 'https://legoclick.58.com/jump?target=pZwY0ZnlsztdraOWUvYKuadBPjw-rj6BmiYOnvubsHwWPhNVryDQniYvmHFbuh7Wn1nzP19KP19kPWmOrjbLPj0OP1cKTHn3P10LnjcOPHnLrj9YnHbKnH0YnjTKnH0YnjTKnikQnTDQTHDLPjDLP10kPjTLnHNKnE7AEzdEEzdKib_VOlXxOCB4sXhehrB8Gryc-SB6Jrh6VEDQTHDKTiYQTEDQrjbOP1NYrH0Ln1m1njcdrHckTHmKTHDKPvFbmhFWrHmVm1bdnBYYn1cQsy7WuWEVuAm3Pyc3nADkujDzTHD3rHbLPHEOP19vPHE3P1bLPjNKnH9OrH0dPjbLrjmOnWmQPWDOn9DKnikQnTDKTEDVTEDKTNn3rHmkn1KDsHbOnHmVE1KjridAwjD3sNmznHb3nYmvwDFArTDzPjK-rWnvrjC3mWwbrhFWmHTlrHb1P1GhPj9vrW0LnWG-myDkTHTKnTDKnikQn97exEDQnjT1P9DQnjTQPWmYTH0OP1u-PjmOsHE3nH9VPAnOPiYOrjmdsHKbrj9kPHTLnANYPEDKPTDKTHTKnikvrjT3sjmOnjmKnE78IyQ_THPWPhwBmH9dm1FbP1I-PWb',
    # 'psid': 'dd59ced3f99cbc11be6fed8365b62499',
}

response = requests.get('https://bj.zu.anjuke.com/fangyuan/3877702953788419?isauction=2&shangquan_id=6906&legoFeeUrl=https%3A%2F%2Flegoclick.58.com%2Fjump%3Ftarget%3DpZwY0ZnlsztdraOWUvYKuaYvnvEkPHEYuiYzm193sHwbPAEVryNdnzY1m191nvR6uADQuj0KP19kPWmOrjbLPj0OP1cKTHn3P10LnjcOPHnLrj9YnHbKnH0YnjTKnH0YnjTKnikQnTDQTHDLPjDLP101rj9LPWcKnE7AEzdEEzdKib_VOlXxOCB4sXhehrB8Gryc-SB6Jrh6VEDQTHDKTiYQTEDQrjbOP1NYrH0Ln1m1njcdrHckTHmKTHDKPyEvuyw6uWDVmHEkriYYuW9Ysy7hPjbVrHPbnHbvPjK-nWTzTHD3rHbLPHEOP19vPHE3P1bLPjNKnH9OrH0dPjbLrjmOnWmQPWDOn9DKnikQnTDKTEDVTEDKTNn3rHmkn1KDsHbOnHmVE1KjridAwjD3sNmznHb3nYmvwDFArTDzPjK-rWnvrjC3mWwbrhFWmHTlrHb1P1GhPj9vrW0LnWG-myDkTHTKnTDKnikQn97exEDQnjT1P9DQnjTQPWmYTycQPjbLmWb1sH--mhcVPjcOmzYOPvnksynLuyEQPHcvrjnOmEDKPTDKTHTKnikvrjT3sjmOnjmKnE78IyQ_Tyn1PjDQmhFWnWbYPWNQPvn&lego_tid=b1497b93-9ebb-429c-97c0-c7ed1526839a&psid=2fd4e9c15124243152a48e1dbe4e8ab1', cookies=cookies, headers=headers)
# print(response.text)
# https://bj.zu.anjuke.com/fangyuan/3877702953788419?isauction=2&shangquan_id=6906&legoFeeUrl=https%3A%2F%2Flegoclick.58.com%2Fjump%3Ftarget%3DpZwY0ZnlsztdraOWUvYKuaYvnvEkPHEYuiYzm193sHwbPAEVryNdnzY1m191nvR6uADQuj0KP19kPWmOrjbLPj0OP1cKTHn3P10LnjcOPHnLrj9YnHbKnH0YnjTKnH0YnjTKnikQnTDQTHDLPjDLP101rj9LPWcKnE7AEzdEEzdKib_VOlXxOCB4sXhehrB8Gryc-SB6Jrh6VEDQTHDKTiYQTEDQrjbOP1NYrH0Ln1m1njcdrHckTHmKTHDKPyEvuyw6uWDVmHEkriYYuW9Ysy7hPjbVrHPbnHbvPjK-nWTzTHD3rHbLPHEOP19vPHE3P1bLPjNKnH9OrH0dPjbLrjmOnWmQPWDOn9DKnikQnTDKTEDVTEDKTNn3rHmkn1KDsHbOnHmVE1KjridAwjD3sNmznHb3nYmvwDFArTDzPjK-rWnvrjC3mWwbrhFWmHTlrHb1P1GhPj9vrW0LnWG-myDkTHTKnTDKnikQn97exEDQnjT1P9DQnjTQPWmYTycQPjbLmWb1sH--mhcVPjcOmzYOPvnksynLuyEQPHcvrjnOmEDKPTDKTHTKnikvrjT3sjmOnjmKnE78IyQ_Tyn1PjDQmhFWnWbYPWNQPvn&lego_tid=b1497b93-9ebb-429c-97c0-c7ed1526839a&psid=2fd4e9c15124243152a48e1dbe4e8ab1
soup = BeautifulSoup(response.text,'html.parser')
title = soup.select_one('.tit-rest').text.strip()
print(title)