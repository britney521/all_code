import pandas as pd
from DrissionPage import ChromiumOptions, Chromium, errors,SessionPage
# 酷派 oppo 小米 华为 飞利浦
import csv
keyword = '华为p70'
#
# df = pd.read_csv('data/{}.csv'.format(keyword))
# datas = df.iloc[:,0].tolist()
datas = []

f = open('data/{}.csv'.format('华为p70skus'), 'a', newline='', encoding='utf-8')
csvfile = csv.writer(f)

co = ChromiumOptions().set_browser_path(r'/Applications/GPT Chrome.app/Contents/MacOS/GptBrowser')
tab = Chromium(co)
page = tab.get_tab()

page.get('https://search.jd.com/Search?keyword={}&enc=utf-8&spm=a.0.0&pvid=64f3cb4157ed4195ab83e20c78b7fe65'.format(f'{keyword}'))
page.wait.doc_loaded()
page.wait(2)

page.scroll.to_bottom()
page.wait.doc_loaded()
# input_ele = page.ele('css:.include_jingyan input:first-child')
# input_ele.clear()
# input_ele.input('酷派老年智能机')
#
#
btn_ele = page.ele('css:._sort-tag_3m6t1_2')
btn_ele.click()

page.wait.doc_loaded()
for i in range(1,17):
    items = page.eles('css:.plugin_goodsContainer .plugin_goodsCardWrapper')
    for item in items:
        sku = item.attr('data-sku')

        if sku not in datas:
            print(sku)
            csvfile.writerow([sku])
    page.ele('._pagination_next_1jczn_8').click()
    page.wait.doc_loaded()
    page.wait(2)
    page.scroll.to_bottom()





