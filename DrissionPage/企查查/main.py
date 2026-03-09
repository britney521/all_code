import re
import csv
import time

import requests
from DrissionPage import ChromiumOptions, ChromiumPage,errors

# params = {
#             'city': '',
#             'companyscale': '',
#             'education': '',
#             'experience': '',
#             'fromTime': '',
#             'industry': '',
#             'isFromSingleApp': True,
#             'isSortAsc': False,
#             'pageIndex': str(i),
#             'pageSize': 20,
#             'salary': '',
#             'searchKey': '电话销售',
#             'sortField': 'publishtime',
#             'toTime': '',
#         }
# url = 'https://www.qcc.com/api/bigsearch/recruit?city=&companyscale=&education=&experience=&fromTime=&industry=&isFromSingleApp=true&isSortAsc=false&pageIndex=1&pageSize=20&salary=&searchKey=%E7%94%B5%E8%AF%9D%E9%94%80%E5%94%AE&sortField=publishtime&toTime='
# resurl = packet.url + '&pageIndex=1'

# new_url = re.sub(r'pageIndex=\d+', f'pageIndex={i}', url)
# print(new_url)

co = ChromiumOptions()
page = ChromiumPage(co)
page.listen.start('api/bigsearch/recruit')
page.get('https://www.qcc.com/web/bigsearch/recruit?searchKey=%E7%94%B5%E8%AF%9D%E9%94%80%E5%94%AE')

cookies = page.cookies()

cookies_data = {

}
for i in cookies:
    cookies_data [i['name']] = i['value']
print(cookies_data)
page.wait.ele_displayed('css:ul.pagination', timeout=3)
lis = page.eles('css:ul.pagination li')

f = open('shishi.csv','w',encoding='utf-8',newline='')
csv_f = csv.writer(f)
csv_f.writerow(['公司KeyNo', '公司名称', '职位名称', '省份', '薪水', '学历', '工作经验', '发布时间'])
for i in range(1,3):
    time.sleep(3)
    print('第{}页数据-------------------------------'.format(i))
    # li.ele('css:a').click()
    page.ele('tag:a@text():>').click()
    # print(f'第{i}页数据')
    packet = page.listen.wait(count=1)
    print(packet.url)  # 打印数据包url
    print(packet.request.headers)  # 打印数据包header

    headers = packet.request.headers
    # 三、使用 requests库 获取网页响应的结果文件
    response = requests.get(packet.url, headers=headers,cookies=cookies_data)
    # print(response.text)
    datas = response.json()['Result']
    for data in datas:
        CompanyKeyNo = data['CompanyKeyNo']
        CompanyName = data['CompanyName']
        name = data['PositionName'].replace('<em>', '').replace('</em>', '')
        Province = data['Province']
        Salary = data['Salary']
        Education = data['Education']
        Experience = data['Experience']
        PublishTime = data['PublishTime']
        print(CompanyKeyNo, CompanyName, name, Province, Salary, Education, Experience, PublishTime)
        csv_f.writerow([CompanyKeyNo, CompanyName, name, Province, Salary, Education, Experience, PublishTime])



