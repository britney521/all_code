import requests
from DrissionPage import ChromiumOptions, ChromiumPage,errors



co = ChromiumOptions()
page = ChromiumPage(co)
page.listen.start('detail?nodeId=')
page.get('https://www.nmpa.gov.cn/datasearch/search-result.html')
print(page.html)
data_packet = page.listen.wait()
print(data_packet)