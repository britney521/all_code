
# 多线程并发的
import time
from DrissionPage import Chromium,ChromiumOptions
from concurrent.futures import ThreadPoolExecutor

op = ChromiumOptions().set_paths('/Applications/GPT Chrome.app/Contents/MacOS/GptBrowser')
#创建页面对象
browser = Chromium(op)


tab=browser.new_tab( )
tab.get("https://icode.best")# 打开百度
tab.wait.doc_loaded()
tab.wait(5)

btn_ele = tab.ele('css:.cb-lb input')
if btn_ele:
    print('1111111111')
    btn_ele.click()
