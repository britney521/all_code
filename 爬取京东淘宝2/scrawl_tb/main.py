import json
import re
from bs4 import BeautifulSoup

import requests
from DrissionPage import ChromiumOptions, Chromium,errors

keyword = '低GI'


headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 'cookie': 'cna=vq8TIfzK3AMBASQOA2i7Jciv; xlly_s=1; lid=%E5%B8%83%E5%85%B0%E5%A6%AEgreat; wk_cookie2=194dcd8e95ff959d2bbda300592b4f2f; wk_unb=UonciUrwAhKNfw%3D%3D; isg=BNTUg2d5QAsoQNRH33J5n-0apRRGLfgXv07a0W61YN_iWXSjlj3Ip4paWVFBoTBv; mtop_partitioned_detect=1; _m_h5_tk=bc72069d97e839ae142c0fc3e9598734_1754065768349; _m_h5_tk_enc=fca74003e1fd0da8e002fa9222174ce3; dnk=%5Cu5E03%5Cu5170%5Cu59AEgreat; tracknick=%5Cu5E03%5Cu5170%5Cu59AEgreat; _l_g_=Ug%3D%3D; unb=1870847194; lgc=%5Cu5E03%5Cu5170%5Cu59AEgreat; cookie1=WvLEeeU9JXBlLInRXvpZ94RiEx71uUnjqWq3%2Fv35U3c%3D; login=true; cookie17=UonciUrwAhKNfw%3D%3D; cookie2=101835a9cb571f4df4c2304695f65ee0; _nk_=%5Cu5E03%5Cu5170%5Cu59AEgreat; sgcookie=E1006x0JgV3At8pnL%2Bz%2BacZdO%2BAJYsEHb9nzulnzWNJH341YMPQBFhRz8LNywUWDZ%2BXbpkmcy7Qh3ToBARmKlenU%2Feu%2BVtyxJYA%2FjLnFiQAmmUZW7y%2Fhy1Y5t0aqXlr0%2FRkp; cancelledSubSites=empty; t=7f97de656ec4a80ab62f27c4dacbc64e; sg=t49; sn=; _tb_token_=e131e8fe55a88; havana_sdkSilent=1754085652862; uc1=cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&cookie14=UoYbz9uNDNB3Vw%3D%3D&pas=0&cookie21=VFC%2FuZ9aiKcVcS5M9%2B3X&existShop=true&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D; uc3=nk2=0X7nDn%2BDuaAbsDo%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D&vt3=F8dD2fnvn8QjqBA0puE%3D&id2=UonciUrwAhKNfw%3D%3D; uc4=id4=0%40UOE2TvRA9Gq834g%2FIDxy3KA2ptVe&nk4=0%4000Z7ohQnczaLBI7JbMQ4CLlZDqKwzQ%3D%3D; havana_lgc_exp=1785160852862; csg=4858f08f; tfstk=gm5jh3XIvGCzPZdt5K4rOrbbXQOsfzPUhVTO-NhqWIdv5f_hfZRNWh561gjJBsRVugN1-M92B1-N1qf5Afl4m-bt1CRTYkPUTZ4DsCEF9UGqKmY9RAFwWEQJiF7XukG8TZbmyqiT8TFE5Pcm_dKOXKp-wFKJkfhvBz9J8FdtMdhxe0Kk2CL9HnhRyeYwWcI96zOJqeh96KI9ezTi_F3B5-tclyZCge8nAY_2VfhONUEMAZMi1U5Jldtdksa_5EYXhHQvVoKLZkJ1cK1zGDYfews2lGVniIp1H9dA1kNXwwXPDUsTAAtRdsf6LsZIKnCDjMOAFuhX6Q1fLpA_dqYPGaCHCsqjwnsly9Rc9uc1va7FiLf_A0KG3eAJlTatenpO4LleAZ-ECoRK1UtUPzMiI8tOmuUI2J2vHUYXUzaSDOvvrUObPzMilKLkzSz7PvAG.',
    'referer': 'https://detail.tmall.com/',
    'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

co = ChromiumOptions().set_browser_path(r'/Applications/GPT Chrome.app/Contents/MacOS/GptBrowser')
tab = Chromium(co)
page = tab.get_tab()
page.get('https://www.taobao.com/')
# print(page.html)
page.wait.doc_loaded()
page.wait.ele_displayed('css:.search-suggest-combobox input')
# 搜索
input_ele = page.ele('css:.search-suggest-combobox input')
btn_ele = page.ele('css:.search-button button')
input_ele.clear()
input_ele.input(keyword)
btn_ele.click()
page.wait.doc_loaded()
page.wait(2)
page.close()

with open(f'{keyword}tb.txt', 'a', encoding='utf-8') as output:
    for i in range(1,3):
        page.wait(2)
        print(f'第{i}页------------------------------------')
        newpage = tab.latest_tab
        newpage.wait.doc_loaded()
        newpage.ele("text=销量").click()
        newpage.wait.doc_loaded()
        newpage.scroll.to_bottom()
        # innerPriceWrapper - -aAJhHXD4
        lists = newpage.eles('css:.search-content-col')
        hrefs = []
        for list in lists:
            if list.ele('@tag()=a'):
                href = 'https://'+list.ele('@tag()=a').attr('href')
                price = list.ele('css:.innerPriceWrapper--aAJhHXD4').text
                salecount = list.ele('css:.realSales--XZJiepmt').text
                shopname = list.ele('css:.shopNameText--DmtlsDKm').text
                print(price, salecount, shopname)
        # for href in hrefs:
        #     output.write(href+'\n')
        next_ele = newpage.ele('css:button[aria-label*="下一页"]')
        next_ele.click()
        newpage.wait.doc_loaded()
        newpage.wait(2)


def close_all(tab):
    # 关闭页面
    for item in tab.get_tabs():
        item.close()

close_all(tab)