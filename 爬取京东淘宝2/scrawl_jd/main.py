
import json
import re
from bs4 import BeautifulSoup
import requests
from DrissionPage import ChromiumOptions, Chromium,errors

keyword = '冷吃三拼'

co = ChromiumOptions().set_browser_path(r'/Applications/GPT Chrome.app/Contents/MacOS/GptBrowser')
tab = Chromium(co)
page = tab.get_tab()

page.get('https://www.jd.com/')
page.wait.doc_loaded()

page.ele('css:input[aria-label="搜索"]').input(keyword)
page.ele('css:button[aria-label="搜索"]').click()

page.wait.doc_loaded()
if page.wait.ele_displayed('._quick-num_1tu5u_47'):
    with open(f'{keyword}jd.txt', 'a', encoding='utf-8') as output:
        for i in range(1,100):
            soup = BeautifulSoup(page.html,'html.parser')
            lists = soup.select('.plugin_goodsCardWrapper')
            ids = [item['data-sku'] for item in lists]
            print(ids)
            for id in ids:
                output.write(id+'\n')
            ele_btn = page.eles('._quick-num_1tu5u_47')[1]
            ele_btn.click()
            page.wait.doc_loaded()
            page.wait(2)


def close_all(tab):
    # 关闭页面
    for item in tab.get_tabs():
        item.close()

close_all(tab)