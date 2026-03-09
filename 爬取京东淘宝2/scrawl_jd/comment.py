import json
import re
from bs4 import BeautifulSoup
import requests
import time
from DrissionPage import ChromiumOptions, Chromium, errors,SessionPage
import pandas as pd
import csv

from torch import init_num_threads
# 酷派 oppo 小米 华为 飞利浦
keyword = '华为'
# 写入CSV文件
f = open('data/{}.csv'.format(keyword), 'a', newline='', encoding='utf-8')
csvfile = csv.writer(f)
# fieldnames = ['id', 'comment']
# csvfile.writerow(fieldnames)

co = ChromiumOptions().set_browser_path(r'/Applications/GPT Chrome.app/Contents/MacOS/GptBrowser')
tab = Chromium(co)
page = tab.get_tab()
page.set.timeouts(3)
stars = {
    'd9d3747bae39b392.png': 5,
    '17fa37516a580e1e.png': 1,
}
# 100081225483
datas = ['https://item.jd.com/10125696245302.html']
for index, row in enumerate(datas[:2]):
    sku = re.search(r'/(\d+)\.html',row).group(1)
    page.get(row)
    page.wait.doc_loaded()
    try:
        if page.wait.ele_displayed('css:.all-btn'):
            commnet_btn = page.ele('css:.all-btn')
            commnet_btn.click()
            page.wait.doc_loaded()
            if page.wait.ele_displayed('css:._title_1ygkr_22'):
                for type in ['图/视频','追评','回头客','好评','中评','差评']:
                    try:
                        page.ele(f'xpath://*[contains(@class,"_tags_rgt47_12")]//*[contains(@class,"_tag-name_rgt47_38") and text()="{type}"]').click()
                    except:
                        print('没有评论跳过')
                        continue
                    # print(page.html）
                    last_content = ''
                    for i in range(1,1000):
                        print(f'{sku}第{i}页')
                        page.wait(2)
                        page.actions.move(10, 10)
                        page.actions.move(-10, -10)
                        soup = BeautifulSoup(page.html,'html.parser')
                        # lists = soup.select('.jdc-pc-rate-card-main-desc')
                        lists = soup.select('._listItem_1ygkr_73')
                        current_page_last_item = None
                        for item in lists:
                            content = item.select_one('.jdc-pc-rate-card-main-desc')
                            nickname = item.select_one('.jdc-pc-rate-card-nick')
                            safe_text = content.get_text().encode('utf-8', errors='replace').decode('utf-8')
                            # if safe_text not in comments:
                            csvfile.writerow([sku, safe_text])
                            print(safe_text)
                            current_page_last_item = safe_text  # 记录当前页最后一项

                            # 检测重复逻辑
                        if current_page_last_item and current_page_last_item == last_content:
                            break
                        last_content = current_page_last_item  # 更新最后一项记录
                        # page.actions.key_down('END')  # 输入按键名称
                        scroll_result = page.run_js('''
                        const element = document.querySelector('div._rateListContainer_1ygkr_45');
                        if (!element) return false;
        
                        // 检查元素是否可滚动
                        const canScroll = element.scrollHeight > element.clientHeight;
                        if (!canScroll) return false;
        
                        // 检查是否已经到底部
                        const isAtBottom = element.scrollTop + element.clientHeight >= element.scrollHeight - 5;
                        if (isAtBottom) return false;
        
                        // 尝试滚动到底部
                        const initialPos = element.scrollTop;
                        element.scrollTo({ top: element.scrollHeight, behavior: 'smooth' });
        
                        // 短暂等待后检查是否滚动成功
                        return new Promise(resolve => {
                          setTimeout(() => {
                            const scrolled = element.scrollTop > initialPos;
                            resolve(scrolled);
                          }, 300); // 等待300ms足够平滑滚动发生
                        });
                        ''')
                        page.actions.move(10, 10)
                        page.actions.move(-10, -10)
                        if not scroll_result:
                            break
                        page.wait.doc_loaded()

        else:
            print(f'{index+1}个{sku}没找到按钮')
            continue
    except Exception as e:
        print(f'{index + 1} 个{sku}报错了{e}')
        break

