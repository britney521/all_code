from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions().set_paths()
page = ChromiumPage(co)
# 开始监听，指定获取包含该文本的数据包
page.listen.start('detail?nodeId=')  # 默认不启动正则匹配，这里代表url包含该字符串，启动正则匹配需要配置 is_regex=True
page.get('https://ygp.gdzwfw.gov.cn/#/44/new/jygg/v3/A?noticeId=dc240acc-d8a3-48ab-b16a-bad2e64a1ff7&projectCode=E4401000002400710001&bizCode=3C51&siteCode=440100&publishDate=20240302000028&source=%E5%B9%BF%E4%BA%A4%E6%98%93%E6%95%B0%E5%AD%97%E4%BA%A4%E6%98%93%E5%B9%B3%E5%8F%B0&titleDetails=%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE&classify=A02&nodeId=1762040444150657029')  # 访问网址
data_packet = page.listen.wait()
print(">>>>本标签页id与框架id    ", data_packet.tab_id, data_packet.frameId)
print(">>>>数据包请求网址    ", data_packet.method, data_packet.url)
print(">>>>响应文本    ", data_packet.response.body,  data_packet.response.raw_body)
print(">>>>响应头    ", data_packet.response.headers)
print(">>>>请求头信息    ", data_packet.request.headers)
for key, value in data_packet.request.headers.items():
    print(f"\t【name】 {key} 【value】 {value}")
print(">>>>请求头表单信息    ", data_packet.request.postData)
print(">>>>连接失败信息    ", data_packet.fail_info.errorText)