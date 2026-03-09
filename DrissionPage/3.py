# 可以启动两个互不相干的全新的浏览器，auto_port会生成随机的端口和临时用户文件夹
from DrissionPage import ChromiumPage, ChromiumOptions
co = ChromiumOptions()
co.auto_port(True)
page1 = ChromiumPage(co)
print("page1要控制的浏览器地址", co.address)
print("page1浏览器默认可执行文件的路径", co.browser_path)
print("page1用户数据文件夹路径", co.user_data_path)
print("page1用户配置文件夹名称", co.user, "\n")
page2 = ChromiumPage(co)
print("page2要控制的浏览器地址", co.address)
print("page2浏览器默认可执行文件的路径", co.browser_path)
print("page2用户数据文件夹路径", co.user_data_path)
print("page2用户配置文件夹名称", co.user)
# 每个页面对象控制一个浏览器
page1.get('https://www.baidu.com')
page2.get('http://www.163.com')


# 可以指定固定的端口和用户目录，来创建两个全新的浏览器
# # 创建多个配置对象，每个指定不同的端口号和用户文件夹路径
# do1 = ChromiumOptions().set_paths(local_port=9111, user_data_path=r'D:\data1')
# do2 = ChromiumOptions().set_paths(local_port=9223, user_data_path=r'D:\data2')
#
# # 创建多个页面对象
# page1 = ChromiumPage(addr_or_opts=do1)
# print("page1要控制的浏览器地址", do1.address)
# print("page1浏览器默认可执行文件的路径", do1.browser_path)
# print("page1用户数据文件夹路径", do1.user_data_path)
# print("page1用户配置文件夹名称", do1.user, "\n")
# page2 = ChromiumPage(addr_or_opts=do2)
# print("page2要控制的浏览器地址", do2.address)
# print("page2浏览器默认可执行文件的路径", do2.browser_path)
# print("page2用户数据文件夹路径", do2.user_data_path)
# print("page2用户配置文件夹名称", do2.user)
# # 每个页面对象控制一个浏览器
# page1.get('https://www.baidu.com')
# page2.get('http://www.163.com')