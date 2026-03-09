import csv
import time
import requests
from bs4 import BeautifulSoup
import os
from loguru import logger

session = requests.session()
# spot_lists = ['三江源国家公园','大熊猫国家公园','东北虎国家公园','海南热带雨林国家公园','福建武夷山国家公园','浙江钱江源国家公园','湖南南山国家公园','云南普达措国家公园'
#               ,'祁连山国家公园']
# 当前景区
spot_lists = ['神农架']

# 配置日志
logger.add("logs/travel_spider.log", rotation="100 MB")

# 下载图片的函数
def download_images(image_urls, spot_name):
    if not os.path.exists(spot_name):
        os.makedirs(spot_name)
    for idx, url in enumerate(image_urls):
        time.sleep(1)
        try:
            response = session.get(url, headers=headers)
            if response.status_code == 200:
                with open(os.path.join(spot_name, f"image_{idx + 1}_{int(time.time())}.jpg"), "wb") as f:
                    f.write(response.content)
                logger.info(f"图片 {url} 下载成功")
            else:
                logger.error(f"下载图片 {url} 失败，状态码：{response.status_code}")
        except Exception as e:
            logger.error(f"下载图片 {url} 时出错：{e}")

# 获取详情页内容
def get_detail(url,spot_name):
    try:
        logger.info(f"正在获取详情页 {url}")
        response = session.post(url, params=params, headers=headers)
        if response.status_code != 200:
            logger.error(f"获取详情页 {url} 失败，状态码：{response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.select_one('.ctd_content')

        if content:
            # 提取图片
            # images = content.find_all('img')
            # image_urls = [img.get('data-original') for img in images]
            # download_images(image_urls,spot_name)
            # logger.info(f"提取到图片 URL：{image_urls}")

            # 提取文字内容
            text_content = content.get_text(strip=True)
        else:
            logger.warning("未找到 .ctd_content 元素")
            text_content = None

        return text_content
    except Exception as e:
        logger.error(f"解析详情页 {url} 时出错：{e}")
        return None

# 主程序
if __name__ == "__main__":
    headers = {
        'referer': 'https://you.ctrip.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
    }
    for spot_name in spot_lists:
        params = {
            'keyword': spot_name,
        }

        res = session.get('https://you.ctrip.com/globalsearch/', params=params, headers=headers)
        guid = res.cookies.get('GUID')
        if guid:
            logger.info(f"爬取{spot_name}提取的 GUID 值：{guid}")
        params = {
            '_fxpcqlniredt': guid,
            'x-traceID': f'{guid}-{int(time.time() * 1000)}-7424549',
        }

        with open(f'csv/{spot_name}.csv', 'w', encoding='utf-8', newline='') as f:
            csv_f = csv.writer(f)
            csv_f.writerow(['标题', '链接', '发布时间', '内容'])
            i = 0
            while i < 20:
                time.sleep(2)
                logger.info(f"正在处理第 {i + 1} 页")
                json_data = {
                    'keyword': spot_name,
                    'pageIndex': i,
                    'pageSize': 12,
                    'tab': 'travelnotes',
                    'profile': False,
                    'head': {
                        'cid': guid,
                        'ctok': '',
                        'cver': '1.0',
                        'lang': '01',
                        'sid': '8888',
                        'syscode': '09',
                        'auth': '',
                        'xsid': '',
                        'extension': [],
                    },
                }

                response = session.post(
                    'https://m.ctrip.com/restapi/soa2/20591/getGsOnlineResult',
                    params=params,
                    headers=headers,
                    json=json_data,
                )

                if response.status_code != 200:
                    logger.error(f"请求第 {i + 1} 页失败，状态码：{response.status_code}")
                    break

                datas = response.json().get('items')
                if not datas:
                    logger.info("未找到更多数据，退出循环")
                    break

                for item in datas:
                    logger.info(f"处理攻略：{item['subTitle']}")
                    subTitle = item['subTitle']
                    titlesoup = BeautifulSoup(subTitle, 'html.parser')
                    subTitle = titlesoup.get_text(strip=True)
                    publishTimeText = item['publishTimeText']
                    url = item['url']
                    text_content = get_detail(url,spot_name)
                    if text_content:
                        csv_f.writerow([subTitle, url, publishTimeText, text_content])
                    else:
                        logger.warning(f"未获取到内容，跳过：{subTitle}")

                i += 1