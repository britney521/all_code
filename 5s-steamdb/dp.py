# 多线程并发的
import time
from DrissionPage import Chromium,ChromiumOptions


op = ChromiumOptions().set_paths('/Applications/GPT Chrome.app/Contents/MacOS/GptBrowser')
#创建页面对象
browser = Chromium(op)
id= 'NNbwm6'
tab=browser.new_tab()
tab.get("https://steamdb.info/app/730/charts/#max")# 打开网址

tab.wait.doc_loaded()
time.sleep(5)
# print(tab.html)
div_ele = tab.ele(f'x://*[@id="{id}"]/div/div')
iframe = div_ele.shadow_root.ele("x://iframe")
body = iframe.ele("t:body")
input = body.shadow_root.ele(f"css:#content #{id} input")
if input:
    input.click()
