import json
import re
import hashlib
import time
import json

import requests
from DrissionPage import ChromiumOptions, Chromium,errors



def get_commnets(page,url):
    page.get(url)
    page.wait.doc_loaded()
    if page.wait.ele_displayed('.ShowButton--hHO0rKRu'):
        page.ele('.ShowButton--hHO0rKRu').click()
    while True:
        # comments_ele = page.ele('.UNJvGJk4hh--Comments--cc29f3ef')
        page.wait(2)
        page.run_js("let element = document.getElementsByClassName('comments--a9Uyym1a beautify-scroll-bar')[1];element.scrollTo({top: element.scrollHeight,behavior: 'smooth'});")
        # page.actions.scroll()
        # page.actions.scroll(delta_y=100, delta_x=0,on_ele=comments_ele)
        page.listen.start('/mtop.taobao.rate.detaillist.get/6.0/')
        data_packet = page.listen.wait()
        url = data_packet.url

        pattern = r'\{.*\}'  # 匹配最外层的大括号内容
        text = data_packet.response.body
        match = re.search(pattern, text)

        if match:
            json_str = match.group(0)

            data = json.loads(json_str)  # 转换为 Python 字典
            # print(data)
            datas = data['data']['rateList']
            for item in datas:
                print(item['feedback'])
        page.wait(2)

if __name__ == '__main__':
    co = ChromiumOptions().set_browser_path(r'/Applications/GPT Chrome.app/Contents/MacOS/GptBrowser')
    tab = Chromium(co)
    page = tab.get_tab()
    url = 'https://item.taobao.com/item.htm?id=677276144260&ns=1&detail_redpacket_pop=true&query=熟驴肉&xxc=ad_ztc&mi_id=kP9O3GXpKkjkTuY5U6zFbWeO1QFa-58ZdPCrWY_kLygrYDcKW56TNdTAopBSr-h1hLBnitVDQKKBhSMfgl4bzxOzmlifOWEuGEdWxGWfg44&skuId=4867868005915&utparam=%7B%22aplus_abtest%22%3A%2277f04c0f575075d39bd7463b42a00c3d%22%7D&spm=a21n57.1.item.1'
    get_commnets(page, url)