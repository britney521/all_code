# 多线程并发的
import time
from DrissionPage import Chromium,ChromiumOptions
from concurrent.futures import ThreadPoolExecutor

op = ChromiumOptions().set_paths('/Applications/GPT Chrome.app/Contents/MacOS/GptBrowser')
#创建页面对象
browser = Chromium(op)

def search(word):
    tab=browser.new_tab( )
    tab.get("https://www.baidu.com/")# 打开百度
    time.sleep(2)#等待1秒
    tab.ele("tag:input@@id=kw").input(word)# 输入搜索词tab.ele("tag:input@@id=su").click()# 点击搜索按钮
    tab.close()
name_list=["衣服","蛋糕","水果"]
with ThreadPoolExecutor(max_workers=3)as executor:
    for name in name_list:
        executor.submit(search, name)




