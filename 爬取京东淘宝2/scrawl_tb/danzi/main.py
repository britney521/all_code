import json
import re

import pandas as pd
from bs4 import BeautifulSoup
import csv
from DrissionPage import ChromiumOptions, Chromium,errors
from loguru import logger

keyword = '全麦'

f = open('{}关键词.csv'.format(keyword),'a',encoding='utf-8',newline='')
f2 = open('{}评论.csv'.format(keyword),'a',encoding='utf-8',newline='')
csv_f = csv.writer(f)
csv_f2 = csv.writer(f2)
csv_f.writerow(['产品名称','价格','销量','店铺','链接'])
csv_f2.writerow(['产品名称','评论'])
def extract_item_ids_from_file(line):
    """å
    从文本文件中读取淘宝/天猫链接，提取所有商品ID并去重
    :return: 去重后的商品ID列表
    """


    # 匹配淘宝/天猫商品ID的正则表达式
    id_pattern = re.compile(r'[?&]id=(\d+)')


    # 方法1：使用正则表达式直接提取
    match = id_pattern.search(line)
    if match:
        itemid = match.group(1)

        return itemid

def get_commnets(page,title,url):
    page.get(url)
    page.wait.doc_loaded()
    if page.wait.ele_displayed('.ShowButton--hHO0rKRu'):
        page.ele('.ShowButton--hHO0rKRu').click()
    page_s = 1
    while page_s < 30:
        # comments_ele = page.ele('.UNJvGJk4hh--Comments--cc29f3ef')
        page.wait(4)
        page.run_js("let element = document.getElementsByClassName('comments--a9Uyym1a beautify-scroll-bar')[1];element.scrollTo({top: element.scrollHeight,behavior: 'smooth'});")
        # page.actions.scroll()
        # page.actions.scroll(delta_y=100, delta_x=0,on_ele=comments_ele)
        page.listen.start('/mtop.taobao.rate.detaillist.get/6.0/')
        data_packet = page.listen.wait(timeout=5)
        url = data_packet.url

        pattern = r'\{.*\}'  # 匹配最外层的大括号内容
        text = data_packet.response.body
        match = re.search(pattern, text)

        if match:
            json_str = match.group(0)

            data = json.loads(json_str)  # 转换为 Python 字典
            # print(data)
            datas = data['data'].get('rateList')
            if datas:
                logger.info('{}商品第{}页共计{}评论'.format(title,page_s,len(datas)))
                for item in datas:
                    comment = item['feedback']
                    csv_f2.writerow([title,comment])
            else:
                break
        page.wait(2)
        page_s += 1
    page.close()

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
# page = tab.get_tab()
# page.get('https://www.taobao.com/')
# # print(page.html)
# page.wait.doc_loaded()
# page.wait.ele_displayed('css:.search-suggest-combobox input')
# # 搜索
# input_ele = page.ele('css:.search-suggest-combobox input')
# btn_ele = page.ele('css:.search-button button')
# input_ele.clear()
# input_ele.input(keyword)
# btn_ele.click()
# page.wait.doc_loaded()
# page.wait(2)
# page.close()
#
#
#
# page.wait(2)
#
# newpage = tab.latest_tab
# newpage.wait.doc_loaded()
# newpage.ele("text=销量").click()
# newpage.wait.doc_loaded()
# newpage.wait(2)
#
# soup = BeautifulSoup(newpage.html, 'html.parser')
# lists = soup.select('.search-content-col')
# logger.info(f'一共爬取到{len(lists)}商品')
# hrefs = []
# for list in lists:
#     if list.select_one('a'):
#         href = list.select_one('a').get('href')
#         title = list.select_one('.title--qJ7Xg_90').get_text()
#         hrefs.append({'href': href, 'title': title})
#         itemid = extract_item_ids_from_file(href)
#         price = list.select_one('.innerPriceWrapper--aAJhHXD4').text
#         salecount = list.select_one('.realSales--XZJiepmt').text
#         shopname = list.select_one('.shopNameText--DmtlsDKm').text
#         logger.info('商品{}价格{}销量{}商店{}'.format(title,price, salecount, shopname))
#         csv_f.writerow([title,price,salecount,shopname,href])

# df = pd.read_csv('全麦关键词.csv')
# for idx in df.index:
#     items = df.loc[idx]
href = 'https://detail.tmall.com/item.htm?id=673871187949&ns=1&abbucket=3&xxc=taobaoSearch&umpChannel=bybtqdyh&u_channel=bybtqdyh&fpChannel=101&fpChannelSig=2e0e7c45b6080749c05668aa4d7a982b9e95582f&mi_id=00003FCgLjg0nxYxlK35WWsZlf2zGSWb_b02onilVwxZpQk&skuId=6069622622083&priceTId=2150480617578965987001838e2652&utparam=%7B%22aplus_abtest%22%3A%2216649f55367db9f092ab25832730bc3b%22%7D&spm=a21n57.1.item.30'
# href = items['链接'] if 'https:' in items['链接'] else 'https:' + items['链接']
# title = items['产品名称']
title = '良品铺子黑麦低脂全麦面包吐司片饱腹健身代早餐营养饱腹粗粮整箱'
twopage = tab.new_tab()
logger.info('{}个{}'.format(1,title))
get_commnets(twopage, title, href)






