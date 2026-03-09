
import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm

cookies = {
    'lang': 'zh',
    'PHPSESSID': '787nq3mhomdnmcsfkcf89c74i5',
    'Hm_lvt_b39c8daefe867a19aec651fe9bb57881': '1740623327',
    'Hm_lpvt_b39c8daefe867a19aec651fe9bb57881': '1740623327',
    'HMACCOUNT': '9BC8D8BA73ECF89B',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://www.chinakaoyan.com/tiaoji/schoollist.shtml',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'lang=zh; PHPSESSID=787nq3mhomdnmcsfkcf89c74i5; Hm_lvt_b39c8daefe867a19aec651fe9bb57881=1740623327; Hm_lpvt_b39c8daefe867a19aec651fe9bb57881=1740623327; HMACCOUNT=9BC8D8BA73ECF89B',
}
# 获取详情
def get_detail(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.select_one('.student-body').get_text().strip()
    return content


f = open('data.csv','w',encoding='utf-8',newline='')
csv_f = csv.writer(f)
csv_f.writerow(['学校','专业','标题','时间','内容','链接'])
for i in tqdm(range(1,1410)):
    response = requests.get('https://www.chinakaoyan.com/tiaoji/schoollist/pagenum/{}.shtml'.format(i),headers=headers)
    # print(response.text)

    soup = BeautifulSoup(response.text,'html.parser')
    items = soup.select('div.info-item')
    print('正在爬取第{}页数据'.format(i))
    if len(items) >0:
        for item in items:
            school = item.select_one('.school').get_text().strip()
            major_name = item.select_one('.name').get_text().strip()
            title = item.select_one('.title a').get_text().strip()
            href = 'https://www.chinakaoyan.com/'+item.select_one('.title a').get('href').strip()
            time = item.select_one('.time').get_text().strip()
            content = get_detail(href)
            print(school,major_name,title,href,time)
            csv_f.writerow([school,major_name,title,time,content,href])
    else:
        print('第{}页没有数据了，退出'.format(i))
        break

f.close()