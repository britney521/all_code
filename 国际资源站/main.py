import requests
from bs4 import BeautifulSoup

from requestdp import get_discord_page_content, get_data
from requestsretry import request_with_retry
from loguru import logger
import csv
cookies = {
    'incap_ses_1512_2720266': 'd/yCPSKpLgNuEeHtCLT7FBzgMmkAAAAAgudhP2Ksx5dQ4IOh8QL85g==',
    'lang': 'enus',
    'bucket': 'a',
    'nlbi_2720266': 'LgJTVIdKHRyXxILnILKq9AAAAAC2VIreRkO0X9zZCClcvuLj',
    '_gcl_au': '1.1.886966978.1764941860',
    'nlbi_3095191': 'DCb/NSQF/25a4+jIi2R/zAAAAABcDZffdxaqSfRtZT9ZOwZp',
    'visid_incap_3095191': 'I3Q5ZPpZR0mzVobGWjtWeCPgMmkAAAAAQUIPAAAAAABK9vp/5Hon+aQkvm63LQwz',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2219aeebb8d59630-0a449e2a47c7408-17525637-2073600-19aeebb8d5a3ff2%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTlhZWViYjhkNTk2MzAtMGE0NDllMmE0N2M3NDA4LTE3NTI1NjM3LTIwNzM2MDAtMTlhZWViYjhkNWEzZmYyIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D',
    'sensorsdata2015jssdkchannel': '%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D',
    'cookiePrefs': '%7B%22analyticsChecked%22%3Atrue%2C%22functionalChecked%22%3Atrue%2C%22advertisingChecked%22%3Atrue%2C%22socialChecked%22%3Atrue%7D',
    'AGL_USER_ID': '1ca13294-bd99-4a8b-9505-7cc7102d5ae1',
    '_fbp': 'fb.1.1764941861206.868393722759515579.AQYBAQIA',
    '_ga': 'GA1.1.1678673699.1764941862',
    'nlbi_2815037': 'tvjHKN/haiQRZgQu0K/W+AAAAAAxx0COb38B0xoNDRxBT9El',
    'visid_incap_2815037': 'JTl3wQucTlCE/hl1k/2f+CXgMmkAAAAAQUIPAAAAAADOXsNLoSc78c6ULEJzkwe8',
    'incap_ses_138_2815037': 'OkorbuygfA1HwMv2dUbqASXgMmkAAAAAqmNgoY0lcjifxFkFmQltxA==',
    'nlbi_2920482': 'FeOYDjxDJDwbMH1COR7VlAAAAADfiWmH+qt31rdyjosEC5xx',
    'visid_incap_2920482': '9XaJ3hzESxWYKMtKPw867SXgMmkAAAAAQUIPAAAAAADieOQZEpl9ZS/+XGQLFR9m',
    'incap_ses_1512_2920482': 'HKD/Ns8rUgkAG+HtCLT7FCXgMmkAAAAAnC34mppYyPeFiG1mAk6kJQ==',
    'FPID': 'FPID2.2.sXDyl7oSZCAUAoL3%2B4Owu3X9f6Oky4cxZxj20oOODZY%3D.1764941862',
    'FPLC': 'wgaaejI2iPY5hWJc2Dkk5IkzXEj6ZwaOnJXtbCFOE2S1RsouEZWObzE207b5l6j5ledJJtHkmqWNSb1feinSZ99IvAfNv22ngPvFaGXiArnlV%2F5XgBFwOSxWSr8cGg%3D%3D',
    '_tt_enable_cookie': '1',
    '_ttp': '01KBQBQ9TBGKYQK3W13HWXTNEK_.tt.1',
    'incap_ses_138_3095191': 'xYXTC9ynhmz65NL2dUbqAUfiMmkAAAAAOL6WbfSVmjU62BZ12p+hQw==',
    'product_search_ranking-19aeebb8d59630-0a449e2a47c7408-17525637-2073600-19aeebb8d5a3ff2': '%7B%22layerCode%22%3A%22product_search_ranking%22%2C%22experimentCode%22%3A%22supply_quality_score_exp%22%2C%22groupName%22%3A%22supply_quality_score_exp1%22%2C%22groupCode%22%3A%22B%22%2C%22params%22%3A%7B%22PRODUCT_BASE_SCORE%22%3A%223%22%7D%7D',
    'GSFlag': '%7B%22hiddenCookieBanner%22%3A%221%22%7D',
    '_clck': '1vrxp48%5E2%5Eg1m%5E0%5E2165',
    'SiteVer': '2',
    '_gtmeec': 'eyJlbSI6IjY2ZmE3MTkzMjM4YmY2NzJkOGNmMTBmNDAyMDI4MGNiYzIzOTE5NDcxYzA1MjJiMjc0OGU4ZjAwMTBmYjJmZTEifQ%3D%3D',
    'incap_ses_138_2720266': 'puPdV5Jtnz81hUz5dUbqAW26M2kAAAAAyO/O4R1YJseiVu2CRLIX4Q==',
    'incap_ses_200_2815037': 'PdGHbzMJjjHBG8wYAYvGAm66M2kAAAAAzxkorB3RJ/ofvs+rV2mSTg==',
    'reese84': '3:CXhO3EKyaJ9f+gVO8Avbkw==:wLva8qvk92u6NTDY+OrWcm//Hz+pfJqprDxOTk4QSK+kq6U1l+2M7c6dQ+X4PCUew2u++tHcMaqv/EtvvqhcFv1idjdM2L0j0XIw00BDFnBn/UE5ZTaeJQkc7YmPjLiUKrFfb4T50YA3E3nxIC+b0gHUC7Bp8yZwOTX30TPiQYo9QYEeCmffr2rWt8lYHH0jZshmVmgxHBtgBVJN6a6rd/XNemvJcpe3cuMYxYbyCFjvnWHwLU/llpAW8iQlYxLS+Zi33QEbnhBO2J5d6RLP+Mr0BAKjhI56TX5sFEY9nkiIrA6lmGQMUhSmc6M4nmAjYxZOT57aaRANGoscnLVdqIKGw1VWFWF3g8uf/NlJi/T7Q9XyZAMaZ/N7DHAhVycr5gTD4KYhz7P8QTgpdxT65hiCGTTvW5XTmWOePbnIPlTZk8nwH8t6LfJDhjbH8/YBEO4GLxjf6nTmk1Wru8UV7Ji0yQ/EoeAZIXqJkNvd/Ac=:ruY0b9BOoL7z1FyTTz/9nxJK37m12fGrpOppkJyK1Do=',
    'incap_sh_2720266': 'dcMzaQAAAACCRgUkDAAI9YbPyQYQ/oXPyQYyrvVVeAzAjPlI/jsJX/eD',
    'visid_incap_2720266': 'N5cGLhnGQjSOB1pa6jqtdBzgMmkAAAAAQkIPAAAAAACA29zAAWc+MapsDpA1yzCW/RpRuUSbYoI+',
    'incap_ses_200_3095191': 'p0xzA4h+b3auotcYAYvGAnnDM2kAAAAA78l8xffiWUTFxPWSoB+2mQ==',
    'incap_ses_138_2920482': 'osJYJy6wYn4gKGz5dUbqAXvDM2kAAAAAKspj9T5LLnFMCXeF8nXUKQ==',
    'GsCookieFlag': '%7B%22pageCont%22%3A1%7D',
    'pageViewCount': '8',
    'nlbi_2720266_2147483392': '+1JnQSJuM2+zTn9TILKq9AAAAAAD/GGVU9AQLWQMIYp2HEe3',
    '_ga_6PQK2T3Q2Q': 'GS2.1.s1764997745$o3$g1$t1765000088$j32$l0$h0',
    '_ga_JK0ML7XE99': 'GS2.1.s1764997745$o3$g1$t1765000088$j32$l0$h0',
    '_uetsid': '93000b60d1df11f0ac063f5822c6235c',
    '_uetvid': '93001f20d1df11f085084368236ebd0e',
    '_clsk': '1arwp24%5E1765000099474%5E3%5E1%5Eh.clarity.ms%2Fcollect',
    '_ga_M0GFGLPMZ2': 'GS2.1.s1764997745$o3$g1$t1765000104$j16$l0$h891394202',
    'ttcsid': '1764997744563::-jo0WAvHKfPu5mM7FUwO.3.1765000105005.0',
    'ttcsid_CI42A6JC77U441D0RJCG': '1764997744562::l8xMirmi8Q67ZIimtEV-.3.1765000105005.1',
}

def get_company(webid):
    cookies = {
        'visid_incap_2720266': 'N5cGLhnGQjSOB1pa6jqtdBzgMmkAAAAAQUIPAAAAAAB0tWNVte2OL51LM6h6Mip6',
        'incap_ses_1512_2720266': 'd/yCPSKpLgNuEeHtCLT7FBzgMmkAAAAAgudhP2Ksx5dQ4IOh8QL85g==',
        'lang': 'enus',
        'bucket': 'a',
        'nlbi_2720266': 'LgJTVIdKHRyXxILnILKq9AAAAAC2VIreRkO0X9zZCClcvuLj',
        '_gcl_au': '1.1.886966978.1764941860',
        'nlbi_3095191': 'DCb/NSQF/25a4+jIi2R/zAAAAABcDZffdxaqSfRtZT9ZOwZp',
        'visid_incap_3095191': 'I3Q5ZPpZR0mzVobGWjtWeCPgMmkAAAAAQUIPAAAAAABK9vp/5Hon+aQkvm63LQwz',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2219aeebb8d59630-0a449e2a47c7408-17525637-2073600-19aeebb8d5a3ff2%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTlhZWViYjhkNTk2MzAtMGE0NDllMmE0N2M3NDA4LTE3NTI1NjM3LTIwNzM2MDAtMTlhZWViYjhkNWEzZmYyIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D',
        'sensorsdata2015jssdkchannel': '%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D',
        'cookiePrefs': '%7B%22analyticsChecked%22%3Atrue%2C%22functionalChecked%22%3Atrue%2C%22advertisingChecked%22%3Atrue%2C%22socialChecked%22%3Atrue%7D',
        '_fbp': 'fb.1.1764941861206.868393722759515579.AQYBAQIA',
        '_ga': 'GA1.1.1678673699.1764941862',
        'nlbi_2815037': 'tvjHKN/haiQRZgQu0K/W+AAAAAAxx0COb38B0xoNDRxBT9El',
        'visid_incap_2815037': 'JTl3wQucTlCE/hl1k/2f+CXgMmkAAAAAQUIPAAAAAADOXsNLoSc78c6ULEJzkwe8',
        'incap_ses_138_2815037': 'OkorbuygfA1HwMv2dUbqASXgMmkAAAAAqmNgoY0lcjifxFkFmQltxA==',
        'nlbi_2920482': 'FeOYDjxDJDwbMH1COR7VlAAAAADfiWmH+qt31rdyjosEC5xx',
        'visid_incap_2920482': '9XaJ3hzESxWYKMtKPw867SXgMmkAAAAAQUIPAAAAAADieOQZEpl9ZS/+XGQLFR9m',
        'incap_ses_1512_2920482': 'HKD/Ns8rUgkAG+HtCLT7FCXgMmkAAAAAnC34mppYyPeFiG1mAk6kJQ==',
        'FPID': 'FPID2.2.sXDyl7oSZCAUAoL3%2B4Owu3X9f6Oky4cxZxj20oOODZY%3D.1764941862',
        'FPLC': 'wgaaejI2iPY5hWJc2Dkk5IkzXEj6ZwaOnJXtbCFOE2S1RsouEZWObzE207b5l6j5ledJJtHkmqWNSb1feinSZ99IvAfNv22ngPvFaGXiArnlV%2F5XgBFwOSxWSr8cGg%3D%3D',
        '_tt_enable_cookie': '1',
        '_ttp': '01KBQBQ9TBGKYQK3W13HWXTNEK_.tt.1',
        'incap_ses_138_3095191': 'xYXTC9ynhmz65NL2dUbqAUfiMmkAAAAAOL6WbfSVmjU62BZ12p+hQw==',
        'product_search_ranking-19aeebb8d59630-0a449e2a47c7408-17525637-2073600-19aeebb8d5a3ff2': '%7B%22layerCode%22%3A%22product_search_ranking%22%2C%22experimentCode%22%3A%22supply_quality_score_exp%22%2C%22groupName%22%3A%22supply_quality_score_exp1%22%2C%22groupCode%22%3A%22B%22%2C%22params%22%3A%7B%22PRODUCT_BASE_SCORE%22%3A%223%22%7D%7D',
        'GSFlag': '%7B%22hiddenCookieBanner%22%3A%221%22%7D',
        'incap_ses_1512_2720266': 'WPIIEWXZkHx8hTPuCLT7FLw/M2kAAAAAccsusLj8CdCbECSXQVYLIg==',
        'incap_ses_138_2720266': 'JOOmaVIpVz+XW2L4dUbqAUZ2M2kAAAAAij6BD0zvM5i8dDzAs8YvgA==',
        '_clck': '1vrxp48%5E2%5Eg1m%5E0%5E2165',
        'incap_ses_200_2815037': 'J46HSfnK4kgMC4MYAYvGArB9M2kAAAAAKHOaGDJ5EsEKeTPSlFzIog==',
        'SiteVer': '2',
        'incap_ses_138_2720266': 'GpJ1Cmh1YijMXnz4dUbqAbB9M2kAAAAAwhd8Sw5Jp2x8yEFAKpYP9w==',
        'incap_ses_200_3095191': 'zVOpUK8UGlDPA48YAYvGAu6HM2kAAAAAjEkfFVx74MB9JR4IyIdYzg==',
        'incap_ses_138_2920482': '8B9HQdST+hsnaL/4dUbqAfyQM2kAAAAAhAn9t/G25pI0AnJkyq/qPg==',
        '_gtmeec': 'eyJlbSI6IjY2ZmE3MTkzMjM4YmY2NzJkOGNmMTBmNDAyMDI4MGNiYzIzOTE5NDcxYzA1MjJiMjc0OGU4ZjAwMTBmYjJmZTEifQ%3D%3D',
        'nlbi_2720266_2147483392': '2lBSf1iQ7WQjVfokILKq9AAAAAARofLxmmRAyYiDHEIsOibu',
        'AGL_USER_ID': '954a8397-0ef1-42ac-9367-661ee9dc86bc',
        'pageViewCount': '2',
        '_ga_6PQK2T3Q2Q': 'GS2.1.s1764982187$o2$g1$t1764988283$j60$l0$h0',
        '_ga_JK0ML7XE99': 'GS2.1.s1764982187$o2$g1$t1764988283$j60$l0$h0',
        '_clsk': '17172xa%5E1764988287923%5E15%5E1%5Eh.clarity.ms%2Fcollect',
        'nlbi_2720266_2147483392': 'OZRBVK6CUAGiy0UiILKq9AAAAAAD9kMj9Ij9N0Fm2wlUIHiv',
        'reese84': '3:LL4HQnSypSlN3fQZZ+rkIQ==:+Zvaky6jx7/OEV9mGC3Zp4jsnrj2dQ534agabAcytlmnqLCfotru3+R4Xo28q3bYHRCaC/9KJxsDjvZjv5WPVRs2OJxoAyPuFZEI2qyuB+qL+7kg2hV6D5Eq2ECHVWArphqjLKqnwfUmdtzXOC2owt2fnzaQPS+Y8bcblfy4PxuukrxlsgYcmVXmENgQbI69bd+5cj9Wpwa8tHITKKqIEkofsPaXwwMuE10g0jTbTHyEUfASNIBmb04d3YsJYiNPRuTnJq3TNVExxA+iw3GiB6+sKQ+v1j2YGFiexgFiGbxRRYYa+Is5IoLjq68BWix5fD8I3QOmEsp4+zrn2Up/duVLrMSHuddiS4bsU3siQvgnJ2vAqzd0rU7XeDb2gLB3Zb0Nw5YAraiFbGjfTGaMHOA35Ra5k4KSqLOdr1mxtU/wYt5XNsx1upeuTm0NNJFBHUThFNWFOKcM6ClG7kW0w2SJH15YjxtmJVaIx4f3tNs=:EJKZUpf9Q+6ANAzJIlRRt1z7/1/rQ7W+u+CweP4rGTI=',
        '_ga_M0GFGLPMZ2': 'GS2.1.s1764982187$o2$g1$t1764988334$j6$l0$h934878212',
        'ttcsid': '1764982187607::_1TFHV21dXIbkEZWGv-t.2.1764988463451.0',
        'ttcsid_CI42A6JC77U441D0RJCG': '1764982187607::mbvm43WWqSOq2Es0QwzP.2.1764988463451.1',
        'GsCookieFlag': '%7B%22pageCont%22%3A1%7D',
        '_uetsid': '93000b60d1df11f0ac063f5822c6235c',
    }
    # response = request_with_retry(
    #     'GET',
    #     f'https://tangmai.manufacturer.globalsources.com/company-profile_{webid}.htm',
    #     cookies=cookies,
    #     headers=headers,
    # )

    response = get_discord_page_content(f'https://tangmai.manufacturer.globalsources.com/company-profile_{webid}.htm',delay=1)
    # 解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    # 1. 找到article-title为"Business Registration Details"的article-table
    article_table = None
    for table in soup.find_all('div', class_='article-table'):
        title = table.find('h3', class_='article-title')
        if title and 'Business Registration Details' in title.text:
            article_table = table
            break

    if article_table:
        # 2. 在article-table内找到table-label为"Registered Company"的元素
        for table_item in article_table.find_all('div', class_='table-item'):
            label = table_item.find('div', class_='table-label')
            if label and label.text == 'Registered Company':
                # 3. 提取对应的table-value-long的值
                value_div = table_item.find('div', class_='table-value-long')
                if value_div:
                    value = value_div.text.strip()
                    logger.success(f"Registered Company: {value}")
                    return value
    else:
        logger.error("未找到符合条件的article-table")
        return ''

def get_details(webid):
    cookies = {
        'visid_incap_2720266': 'N5cGLhnGQjSOB1pa6jqtdBzgMmkAAAAAQUIPAAAAAAB0tWNVte2OL51LM6h6Mip6',
        'incap_ses_1512_2720266': 'd/yCPSKpLgNuEeHtCLT7FBzgMmkAAAAAgudhP2Ksx5dQ4IOh8QL85g==',
        'lang': 'enus',
        'bucket': 'a',
        'nlbi_2720266': 'LgJTVIdKHRyXxILnILKq9AAAAAC2VIreRkO0X9zZCClcvuLj',
        '_gcl_au': '1.1.886966978.1764941860',
        'nlbi_3095191': 'DCb/NSQF/25a4+jIi2R/zAAAAABcDZffdxaqSfRtZT9ZOwZp',
        'visid_incap_3095191': 'I3Q5ZPpZR0mzVobGWjtWeCPgMmkAAAAAQUIPAAAAAABK9vp/5Hon+aQkvm63LQwz',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2219aeebb8d59630-0a449e2a47c7408-17525637-2073600-19aeebb8d5a3ff2%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTlhZWViYjhkNTk2MzAtMGE0NDllMmE0N2M3NDA4LTE3NTI1NjM3LTIwNzM2MDAtMTlhZWViYjhkNWEzZmYyIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D',
        'sensorsdata2015jssdkchannel': '%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D',
        'cookiePrefs': '%7B%22analyticsChecked%22%3Atrue%2C%22functionalChecked%22%3Atrue%2C%22advertisingChecked%22%3Atrue%2C%22socialChecked%22%3Atrue%7D',
        '_fbp': 'fb.1.1764941861206.868393722759515579.AQYBAQIA',
        '_ga': 'GA1.1.1678673699.1764941862',
        'nlbi_2815037': 'tvjHKN/haiQRZgQu0K/W+AAAAAAxx0COb38B0xoNDRxBT9El',
        'visid_incap_2815037': 'JTl3wQucTlCE/hl1k/2f+CXgMmkAAAAAQUIPAAAAAADOXsNLoSc78c6ULEJzkwe8',
        'incap_ses_138_2815037': 'OkorbuygfA1HwMv2dUbqASXgMmkAAAAAqmNgoY0lcjifxFkFmQltxA==',
        'nlbi_2920482': 'FeOYDjxDJDwbMH1COR7VlAAAAADfiWmH+qt31rdyjosEC5xx',
        'visid_incap_2920482': '9XaJ3hzESxWYKMtKPw867SXgMmkAAAAAQUIPAAAAAADieOQZEpl9ZS/+XGQLFR9m',
        'incap_ses_1512_2920482': 'HKD/Ns8rUgkAG+HtCLT7FCXgMmkAAAAAnC34mppYyPeFiG1mAk6kJQ==',
        'FPID': 'FPID2.2.sXDyl7oSZCAUAoL3%2B4Owu3X9f6Oky4cxZxj20oOODZY%3D.1764941862',
        'FPLC': 'wgaaejI2iPY5hWJc2Dkk5IkzXEj6ZwaOnJXtbCFOE2S1RsouEZWObzE207b5l6j5ledJJtHkmqWNSb1feinSZ99IvAfNv22ngPvFaGXiArnlV%2F5XgBFwOSxWSr8cGg%3D%3D',
        '_tt_enable_cookie': '1',
        '_ttp': '01KBQBQ9TBGKYQK3W13HWXTNEK_.tt.1',
        'incap_ses_138_3095191': 'xYXTC9ynhmz65NL2dUbqAUfiMmkAAAAAOL6WbfSVmjU62BZ12p+hQw==',
        'product_search_ranking-19aeebb8d59630-0a449e2a47c7408-17525637-2073600-19aeebb8d5a3ff2': '%7B%22layerCode%22%3A%22product_search_ranking%22%2C%22experimentCode%22%3A%22supply_quality_score_exp%22%2C%22groupName%22%3A%22supply_quality_score_exp1%22%2C%22groupCode%22%3A%22B%22%2C%22params%22%3A%7B%22PRODUCT_BASE_SCORE%22%3A%223%22%7D%7D',
        'GSFlag': '%7B%22hiddenCookieBanner%22%3A%221%22%7D',
        'incap_ses_1512_2720266': 'WPIIEWXZkHx8hTPuCLT7FLw/M2kAAAAAccsusLj8CdCbECSXQVYLIg==',
        'incap_ses_138_2720266': 'JOOmaVIpVz+XW2L4dUbqAUZ2M2kAAAAAij6BD0zvM5i8dDzAs8YvgA==',
        '_clck': '1vrxp48%5E2%5Eg1m%5E0%5E2165',
        'incap_ses_200_2815037': 'J46HSfnK4kgMC4MYAYvGArB9M2kAAAAAKHOaGDJ5EsEKeTPSlFzIog==',
        'SiteVer': '2',
        'incap_ses_138_2720266': 'GpJ1Cmh1YijMXnz4dUbqAbB9M2kAAAAAwhd8Sw5Jp2x8yEFAKpYP9w==',
        'incap_ses_200_3095191': 'zVOpUK8UGlDPA48YAYvGAu6HM2kAAAAAjEkfFVx74MB9JR4IyIdYzg==',
        'incap_ses_138_2920482': '8B9HQdST+hsnaL/4dUbqAfyQM2kAAAAAhAn9t/G25pI0AnJkyq/qPg==',
        '_gtmeec': 'eyJlbSI6IjY2ZmE3MTkzMjM4YmY2NzJkOGNmMTBmNDAyMDI4MGNiYzIzOTE5NDcxYzA1MjJiMjc0OGU4ZjAwMTBmYjJmZTEifQ%3D%3D',
        'nlbi_2720266_2147483392': '2lBSf1iQ7WQjVfokILKq9AAAAAARofLxmmRAyYiDHEIsOibu',
        'AGL_USER_ID': '954a8397-0ef1-42ac-9367-661ee9dc86bc',
        'reese84': '3:LL4HQnSypSlN3fQZZ+rkIQ==:+Zvaky6jx7/OEV9mGC3Zp4jsnrj2dQ534agabAcytlmnqLCfotru3+R4Xo28q3bYHRCaC/9KJxsDjvZjv5WPVRs2OJxoAyPuFZEI2qyuB+qL+7kg2hV6D5Eq2ECHVWArphqjLKqnwfUmdtzXOC2owt2fnzaQPS+Y8bcblfy4PxuukrxlsgYcmVXmENgQbI69bd+5cj9Wpwa8tHITKKqIEkofsPaXwwMuE10g0jTbTHyEUfASNIBmb04d3YsJYiNPRuTnJq3TNVExxA+iw3GiB6+sKQ+v1j2YGFiexgFiGbxRRYYa+Is5IoLjq68BWix5fD8I3QOmEsp4+zrn2Up/duVLrMSHuddiS4bsU3siQvgnJ2vAqzd0rU7XeDb2gLB3Zb0Nw5YAraiFbGjfTGaMHOA35Ra5k4KSqLOdr1mxtU/wYt5XNsx1upeuTm0NNJFBHUThFNWFOKcM6ClG7kW0w2SJH15YjxtmJVaIx4f3tNs=:EJKZUpf9Q+6ANAzJIlRRt1z7/1/rQ7W+u+CweP4rGTI=',
        'pageViewCount': '3',
        'nlbi_2720266_2147483392': 'uWuRIZ0ni3pw2tilILKq9AAAAABheTl9SYdEYiE2fs4Ose5W',
        '_ga_6PQK2T3Q2Q': 'GS2.1.s1764982187$o2$g1$t1764988471$j53$l0$h0',
        '_ga_JK0ML7XE99': 'GS2.1.s1764982187$o2$g1$t1764988471$j53$l0$h0',
        '_clsk': '17172xa%5E1764988475995%5E16%5E1%5Eh.clarity.ms%2Fcollect',
        '_ga_M0GFGLPMZ2': 'GS2.1.s1764982187$o2$g1$t1764988499$j25$l0$h934878212',
        'ttcsid': '1764982187607::_1TFHV21dXIbkEZWGv-t.2.1764988535967.0',
        'ttcsid_CI42A6JC77U441D0RJCG': '1764982187607::mbvm43WWqSOq2Es0QwzP.2.1764988535967.1',
        'GsCookieFlag': '%7B%22pageCont%22%3A1%7D',
        '_uetsid': '93000b60d1df11f0ac063f5822c6235c',
        '_uetvid': '93001f20d1df11f085084368236ebd0e',
    }
    response = get_discord_page_content(f'https://tangmai.manufacturer.globalsources.com/contact-us_{webid}.htm')
    # response = request_with_retry(
    #     'GET',
    #     f'https://tangmai.manufacturer.globalsources.com/contact-us_{webid}.htm',
    #     cookies=cookies,
    #     headers=headers,
    # )
    soup = BeautifulSoup(response.text, 'html.parser')

    # 使用封装函数获取文本
    def get_safe_text(soup, selector, default=""):
        elem = soup.select_one(selector)
        if elem:
            return elem.get_text(strip=True)
        else:
            return ""

    # 获取数据
    contact_name = get_safe_text(soup, ".contact-name")
    worker = get_safe_text(soup, ".contact-worker")


    # 定义要查找的标签
    target_labels = [
        "Homepage website:",
        "Other homepage website:"  # 注意：这个标签在提供的HTML中不存在，可能是输入错误
    ]
    links = []
    # 遍历所有contact-item元素
    for contact_item in soup.find_all('div', class_='contact-item'):
        # 获取contact-label文本
        label = contact_item.find('div', class_='contact-label')
        if label:
            label_text = label.text.strip()
            # 检查是否是目标标签
            if label_text in target_labels:
                # 获取对应的contact-value
                value = contact_item.find('div', class_='contact-value').text.strip()
                logger.success(f"{label_text}: {value}")
                links.append(value)

    return contact_name,worker,links
cookies = {
    'incap_ses_1512_2720266': 'd/yCPSKpLgNuEeHtCLT7FBzgMmkAAAAAgudhP2Ksx5dQ4IOh8QL85g==',
    'lang': 'enus',
    'bucket': 'a',
    'nlbi_2720266': 'LgJTVIdKHRyXxILnILKq9AAAAAC2VIreRkO0X9zZCClcvuLj',
    '_gcl_au': '1.1.886966978.1764941860',
    'nlbi_3095191': 'DCb/NSQF/25a4+jIi2R/zAAAAABcDZffdxaqSfRtZT9ZOwZp',
    'visid_incap_3095191': 'I3Q5ZPpZR0mzVobGWjtWeCPgMmkAAAAAQUIPAAAAAABK9vp/5Hon+aQkvm63LQwz',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2219aeebb8d59630-0a449e2a47c7408-17525637-2073600-19aeebb8d5a3ff2%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTlhZWViYjhkNTk2MzAtMGE0NDllMmE0N2M3NDA4LTE3NTI1NjM3LTIwNzM2MDAtMTlhZWViYjhkNWEzZmYyIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D',
    'sensorsdata2015jssdkchannel': '%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D',
    'cookiePrefs': '%7B%22analyticsChecked%22%3Atrue%2C%22functionalChecked%22%3Atrue%2C%22advertisingChecked%22%3Atrue%2C%22socialChecked%22%3Atrue%7D',
    'AGL_USER_ID': '1ca13294-bd99-4a8b-9505-7cc7102d5ae1',
    '_fbp': 'fb.1.1764941861206.868393722759515579.AQYBAQIA',
    '_ga': 'GA1.1.1678673699.1764941862',
    'nlbi_2815037': 'tvjHKN/haiQRZgQu0K/W+AAAAAAxx0COb38B0xoNDRxBT9El',
    'visid_incap_2815037': 'JTl3wQucTlCE/hl1k/2f+CXgMmkAAAAAQUIPAAAAAADOXsNLoSc78c6ULEJzkwe8',
    'incap_ses_138_2815037': 'OkorbuygfA1HwMv2dUbqASXgMmkAAAAAqmNgoY0lcjifxFkFmQltxA==',
    'nlbi_2920482': 'FeOYDjxDJDwbMH1COR7VlAAAAADfiWmH+qt31rdyjosEC5xx',
    'visid_incap_2920482': '9XaJ3hzESxWYKMtKPw867SXgMmkAAAAAQUIPAAAAAADieOQZEpl9ZS/+XGQLFR9m',
    'incap_ses_1512_2920482': 'HKD/Ns8rUgkAG+HtCLT7FCXgMmkAAAAAnC34mppYyPeFiG1mAk6kJQ==',
    'FPID': 'FPID2.2.sXDyl7oSZCAUAoL3%2B4Owu3X9f6Oky4cxZxj20oOODZY%3D.1764941862',
    'FPLC': 'wgaaejI2iPY5hWJc2Dkk5IkzXEj6ZwaOnJXtbCFOE2S1RsouEZWObzE207b5l6j5ledJJtHkmqWNSb1feinSZ99IvAfNv22ngPvFaGXiArnlV%2F5XgBFwOSxWSr8cGg%3D%3D',
    '_tt_enable_cookie': '1',
    '_ttp': '01KBQBQ9TBGKYQK3W13HWXTNEK_.tt.1',
    'incap_ses_138_3095191': 'xYXTC9ynhmz65NL2dUbqAUfiMmkAAAAAOL6WbfSVmjU62BZ12p+hQw==',
    'product_search_ranking-19aeebb8d59630-0a449e2a47c7408-17525637-2073600-19aeebb8d5a3ff2': '%7B%22layerCode%22%3A%22product_search_ranking%22%2C%22experimentCode%22%3A%22supply_quality_score_exp%22%2C%22groupName%22%3A%22supply_quality_score_exp1%22%2C%22groupCode%22%3A%22B%22%2C%22params%22%3A%7B%22PRODUCT_BASE_SCORE%22%3A%223%22%7D%7D',
    'GSFlag': '%7B%22hiddenCookieBanner%22%3A%221%22%7D',
    '_clck': '1vrxp48%5E2%5Eg1m%5E0%5E2165',
    'SiteVer': '2',
    '_gtmeec': 'eyJlbSI6IjY2ZmE3MTkzMjM4YmY2NzJkOGNmMTBmNDAyMDI4MGNiYzIzOTE5NDcxYzA1MjJiMjc0OGU4ZjAwMTBmYjJmZTEifQ%3D%3D',
    'incap_ses_138_2720266': 'puPdV5Jtnz81hUz5dUbqAW26M2kAAAAAyO/O4R1YJseiVu2CRLIX4Q==',
    'incap_ses_200_2815037': 'PdGHbzMJjjHBG8wYAYvGAm66M2kAAAAAzxkorB3RJ/ofvs+rV2mSTg==',
    'incap_sh_2720266': 'dcMzaQAAAACCRgUkDAAI9YbPyQYQ/oXPyQYyrvVVeAzAjPlI/jsJX/eD',
    'visid_incap_2720266': 'N5cGLhnGQjSOB1pa6jqtdBzgMmkAAAAAQkIPAAAAAACA29zAAWc+MapsDpA1yzCW/RpRuUSbYoI+',
    'incap_ses_200_3095191': 'p0xzA4h+b3auotcYAYvGAnnDM2kAAAAA78l8xffiWUTFxPWSoB+2mQ==',
    'reese84': '3:Ku4wRZGSf6XgNLMSt+iszA==:w5l01QCqHFyR5uFE1B0eLzQICP+wpkU2BmfccEY8GrJ7xgc9zOl6R7i7GHgmfxu5BVb75DIhAm7C8++GLCRGVOidxhnIuCQn+I5WdvFtybu4Y+2ejlLn05Fp6OuH6LakFEoPzNprHSrZsd9slAcCP9W8duQNe9BdQ/I1EiDaTi1ea4I6vMpAR8ltCFf23M49rrUlwPelvoJ8wu99Y2NV4XbUaQlkHyPaCdmGz+X8bcYtCfGtl1rmzOVaGxwk6TDnE4AxMk94aEYBhS4gKkBSVaotiGiOgmPEBWOQcoDZjwTt0g+JwHuZRjuuG9UgyZCPBSyKE5lNB9VGdpxfctdFcG0RFzkqaWQALAJmrp3w4mIsemIjPhMG2bCT7t4c1JyZl5VV5/7cq0j6tMmNp+ZHMxjYB5hdG9ebBoq+MZXXWjW650v63VwNLuGqaTVbYEvBt1ccr6AEU7JLROHgYnOKTbxDvFEie/DPgFjz6d8rx8Skj65xGE+1BABsKmLeRbEkD/wGiFacMg+r+S+OcGXlAw==:Irsrxji/vL8gjuql3tGtqaftAbTqDTH6Yidy6DMvor8=',
    'GsCookieFlag': '%7B%22pageCont%22%3A1%7D',
    'pageViewCount': '9',
    'incap_ses_138_2920482': 'WmjZe8N7/XKvcH/5dUbqAWXJM2kAAAAAQCfmp+tDCOIAqWzee0RQzQ==',
    'nlbi_2720266_2147483392': 'Y9TaXiaM4AoAuFIlILKq9AAAAABTk8SGJYH4BCL7R+Z4+SDl',
    '_uetsid': '93000b60d1df11f0ac063f5822c6235c',
    '_uetvid': '93001f20d1df11f085084368236ebd0e',
    '_clsk': '1arwp24%5E1765001589788%5E7%5E1%5Eh.clarity.ms%2Fcollect',
    '_ga_6PQK2T3Q2Q': 'GS2.1.s1764997745$o3$g1$t1765001589$j43$l0$h0',
    '_ga_JK0ML7XE99': 'GS2.1.s1764997745$o3$g1$t1765001589$j43$l0$h0',
    'ttcsid': '1764997744563::-jo0WAvHKfPu5mM7FUwO.3.1765001591167.0',
    'ttcsid_CI42A6JC77U441D0RJCG': '1764997744562::l8xMirmi8Q67ZIimtEV-.3.1765001591168.1',
    '_ga_M0GFGLPMZ2': 'GS2.1.s1764997745$o3$g1$t1765001603$j29$l0$h891394202',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'baggage': 'sentry-environment=production,sentry-release=2025-12-05%2011%3A30%3A40,sentry-public_key=67c53096d260aef41cd00bceedab261a,sentry-trace_id=c115aa1257a14c06ac8484f2bb3f503d,sentry-sample_rate=0.2,sentry-transaction=searchList-suppliers,sentry-sampled=false',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    # 'cookie': 'visid_incap_2720266=N5cGLhnGQjSOB1pa6jqtdBzgMmkAAAAAQUIPAAAAAAB0tWNVte2OL51LM6h6Mip6; incap_ses_1512_2720266=d/yCPSKpLgNuEeHtCLT7FBzgMmkAAAAAgudhP2Ksx5dQ4IOh8QL85g==; lang=enus; bucket=a; nlbi_2720266=LgJTVIdKHRyXxILnILKq9AAAAAC2VIreRkO0X9zZCClcvuLj; _gcl_au=1.1.886966978.1764941860; nlbi_3095191=DCb/NSQF/25a4+jIi2R/zAAAAABcDZffdxaqSfRtZT9ZOwZp; visid_incap_3095191=I3Q5ZPpZR0mzVobGWjtWeCPgMmkAAAAAQUIPAAAAAABK9vp/5Hon+aQkvm63LQwz; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219aeebb8d59630-0a449e2a47c7408-17525637-2073600-19aeebb8d5a3ff2%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTlhZWViYjhkNTk2MzAtMGE0NDllMmE0N2M3NDA4LTE3NTI1NjM3LTIwNzM2MDAtMTlhZWViYjhkNWEzZmYyIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D; sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; cookiePrefs=%7B%22analyticsChecked%22%3Atrue%2C%22functionalChecked%22%3Atrue%2C%22advertisingChecked%22%3Atrue%2C%22socialChecked%22%3Atrue%7D; AGL_USER_ID=1ca13294-bd99-4a8b-9505-7cc7102d5ae1; _fbp=fb.1.1764941861206.868393722759515579.AQYBAQIA; _ga=GA1.1.1678673699.1764941862; nlbi_2815037=tvjHKN/haiQRZgQu0K/W+AAAAAAxx0COb38B0xoNDRxBT9El; visid_incap_2815037=JTl3wQucTlCE/hl1k/2f+CXgMmkAAAAAQUIPAAAAAADOXsNLoSc78c6ULEJzkwe8; incap_ses_138_2815037=OkorbuygfA1HwMv2dUbqASXgMmkAAAAAqmNgoY0lcjifxFkFmQltxA==; nlbi_2920482=FeOYDjxDJDwbMH1COR7VlAAAAADfiWmH+qt31rdyjosEC5xx; visid_incap_2920482=9XaJ3hzESxWYKMtKPw867SXgMmkAAAAAQUIPAAAAAADieOQZEpl9ZS/+XGQLFR9m; incap_ses_1512_2920482=HKD/Ns8rUgkAG+HtCLT7FCXgMmkAAAAAnC34mppYyPeFiG1mAk6kJQ==; FPID=FPID2.2.sXDyl7oSZCAUAoL3%2B4Owu3X9f6Oky4cxZxj20oOODZY%3D.1764941862; _gtmeec=e30%3D; FPLC=wgaaejI2iPY5hWJc2Dkk5IkzXEj6ZwaOnJXtbCFOE2S1RsouEZWObzE207b5l6j5ledJJtHkmqWNSb1feinSZ99IvAfNv22ngPvFaGXiArnlV%2F5XgBFwOSxWSr8cGg%3D%3D; _tt_enable_cookie=1; _ttp=01KBQBQ9TBGKYQK3W13HWXTNEK_.tt.1; incap_ses_138_3095191=xYXTC9ynhmz65NL2dUbqAUfiMmkAAAAAOL6WbfSVmjU62BZ12p+hQw==; product_search_ranking-19aeebb8d59630-0a449e2a47c7408-17525637-2073600-19aeebb8d5a3ff2=%7B%22layerCode%22%3A%22product_search_ranking%22%2C%22experimentCode%22%3A%22supply_quality_score_exp%22%2C%22groupName%22%3A%22supply_quality_score_exp1%22%2C%22groupCode%22%3A%22B%22%2C%22params%22%3A%7B%22PRODUCT_BASE_SCORE%22%3A%223%22%7D%7D; GSFlag=%7B%22hiddenCookieBanner%22%3A%221%22%7D; _clck=1vrxp48%5E2%5Eg1m%5E0%5E2165; incap_ses_200_2815037=J46HSfnK4kgMC4MYAYvGArB9M2kAAAAAKHOaGDJ5EsEKeTPSlFzIog==; SiteVer=2; incap_ses_138_2720266=GpJ1Cmh1YijMXnz4dUbqAbB9M2kAAAAAwhd8Sw5Jp2x8yEFAKpYP9w==; incap_ses_138_2920482=g96QbStFJW6beHz4dUbqAbh9M2kAAAAADoekiw2eXz5l3xWndaAnYA==; pageViewCount=4; nlbi_2720266_2147483392=KGeCbeQhcTajSblHILKq9AAAAAAU6+nKjP6eMdqWAXr7m8fT; _clsk=1otd27o%5E1764982289323%5E3%5E1%5Ej.clarity.ms%2Fcollect; ttcsid=1764982187607::_1TFHV21dXIbkEZWGv-t.2.1764982485307.0; ttcsid_CI42A6JC77U441D0RJCG=1764982187607::mbvm43WWqSOq2Es0QwzP.2.1764982485307.1; reese84=3:8R4fq5NKJhV/II6IkrpqTg==:kwgoVZp7tNjFP//sG0+9tJWmWkxAjUt5v6DxHyv3kwdqOc7I8PqvgybCePKLOM07P9sclNhnMkVegRGM6xSVp+OXjWUHMPp1tJUTs94LthBV1OxVubE0esnyU5c2JKGdTAHOmF5VW69aNyvHMrZTQN9zFXhEej9pQZfislWlevplER5tU6LCvJeNeqP6/ErKFhY9tHd+VXsRt/PsR0WBFQJam3daXn9pTdBaYcPUTpmjGewrCbi8aEUOd80TibI6Hq40RrdodrGWafNaky2urUYRPiyUIFMY5qsLMJLzBEJr/TOvyaI8QOSFZNH5P71XPF6mKZQ3JHP7FfvU+s0b9mnaq8I8b0CN4cND5AwhlJgy6qOcAMoRq2IiiA4jGtEqfzzDxUaVUq3SlUGMs1s1PmncSm+tG+Mk1KqiTJhTkknS92BMu9A3UwWIBPYSolbRly+e1f3oHDDmHlim5ZwCGhp69AHVjZHYLYJTadc9uFo=:5j1OPfD0/miWk5GlqfmSEuMy6g7lfRbpyPtlUQYn/ug=; GsCookieFlag=%7B%22pageCont%22%3A1%7D; _uetsid=93000b60d1df11f0ac063f5822c6235c; _uetvid=93001f20d1df11f085084368236ebd0e; _ga_6PQK2T3Q2Q=GS2.1.s1764982187$o2$g1$t1764982689$j34$l0$h0; _ga_JK0ML7XE99=GS2.1.s1764982187$o2$g1$t1764982689$j34$l0$h0; _ga_M0GFGLPMZ2=GS2.1.s1764982187$o2$g1$t1764982689$j34$l0$h934878212',
    'lang': 'enus',
    'origin': 'https://www.globalsources.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.globalsources.com/searchList/suppliers?keyWord=china&pageNum=2',
    'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sensorsid': '$device_id=19aeebb8d59630-0a449e2a47c7408-17525637-2073600-19aeebb8d5a3ff2',
    'sentry-trace': 'c115aa1257a14c06ac8484f2bb3f503d-9e946f8e12abed79-0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

f = open("data.csv", "a",encoding="utf-8",newline="")
writer = csv.writer(f)
# writer.writerow(['公司名',"中文名","联系人","职位","主页","官网"])
for page in range(8, 300):
    json_data = {
        'pageNum': page,
        'pageSize': 20,
        'query': 'china',
    }

    # response = request_with_retry(
    #     method='POST',
    #     url='https://www.globalsources.com/api/agg-search/DESKTOP/v3/supplier/search',
    #     cookies=cookies,
    #     headers=headers,
    #     json=json_data,
    # )
    url = f"https://www.globalsources.com/searchList/suppliers?keyWord=china&pageNum={page}"
    response = get_data(url=url,lanjieurl="v3/supplier/search")
    logger.info(f"正在爬取第{page}页")
    # print(response.json())
    datas = response['data']['list']
    if len(datas) == 0:
        break
    for item in datas:
        orgId = item['orgId']
        webid = str(orgId).replace('200', '600')
        supplier = item['supplier']
        websiteName = supplier['websiteName']
        logger.info(f"id{orgId}名称{websiteName}")
        chinese_name = get_company(webid)
        contact_name,worker,links = get_details(webid)
        logger.success("获取到数据{}".format("".join([websiteName,chinese_name,contact_name,worker,*links])))
        writer.writerow([websiteName,chinese_name,contact_name,worker,*links])

f.close()