import os
import re
import requests
from bs4 import BeautifulSoup
import csv
import time
from loguru import logger

# 配置日志
logger.add("logs/mafenwo_spider.log", rotation="100 MB", compression="zip")

# 下载图片的函数
def download_images(image_urls, folder="福建武夷山国家公园"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    for idx, url in enumerate(image_urls):
        try:
            response = requests.get(url, headers=headers, cookies=cookies)
            if response.status_code == 200:
                with open(os.path.join(folder, f"image_{idx + 1}_{time.time()}.jpg"), "wb") as f:
                    f.write(response.content)
                logger.info(f"图片 {url} 下载成功")
            else:
                logger.error(f"下载图片 {url} 失败，状态码：{response.status_code}")
        except Exception as e:
            logger.error(f"下载图片 {url} 时出错：{e}")

def scraw_all_detail(new_iid_value, seq, id):
    global all_content
    params = {
        'id': id,
        'iid': new_iid_value,
        'seq': seq,
        'back': '0',
    }
    try:
        response = requests.get('https://www.mafengwo.cn/note/ajax/detail/getNoteDetailContentChunk', params=params,
                                cookies=cookies, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()
        html = data['data']['html']
        has_more = data['data']['has_more']
        soup = BeautifulSoup(html, 'html.parser')

        content = soup.get_text(strip=True).strip('\n').strip(' ')
        image_urls = [img['data-src'] for img in soup.find_all('img', {'data-src': True})]
        if image_urls:
            download_images(image_urls)

        seq_items = soup.find_all(attrs={"data-seq": True})
        last_seq = seq_items[-1]['data-seq'] if seq_items else None

        all_content += content
        logger.info(f"获取到更多内容，当前seq: {seq}, 新seq: {last_seq}")
        return has_more, last_seq
    except requests.RequestException as e:
        logger.error(f"请求失败：{e}")
    except KeyError as e:
        logger.error(f"解析失败，缺少关键字段：{e}")
    except Exception as e:
        logger.error(f"未知错误：{e}")
    return False, None

def get_detail(url, id):
    global all_content
    try:
        response = session.get(url, headers=headers, cookies=cookies, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        title_element = soup.select_one('.view_info .headtext')
        title = title_element.get_text(strip=True) if title_element else None

        content_element = soup.select_one('._j_master_content')
        content = (content_element.get_text(strip=True).replace('\n', '').replace(' ', '')) if content_element else ''
        all_content += content

        time_ele = soup.select_one('.time')
        create_time = time_ele.get_text() if time_ele else ''

        image_urls = [img['data-src'] for img in soup.find_all('img', {'data-src': True})]
        if image_urls:
            download_images(image_urls)

        match = re.search(r'"new_iid":\s*"([^"]+)"', response.text)
        new_iid_value = match.group(1) if match else None
        logger.info(f"提取到 new_iid: {new_iid_value}")

        seq_element = soup.select_one('div._j_seqitem:last-child')
        seq = seq_element.get('data-seq') if seq_element else None
        logger.info(f"提取到 seq: {seq}")

        has_more = True
        while has_more:
            has_more, seq = scraw_all_detail(new_iid_value, seq, id)

        csv_f.writerow([title, url, create_time, all_content])
        logger.info(f"成功处理攻略：{title}")
    except requests.RequestException as e:
        logger.error(f"请求失败：{e}")
    except KeyError as e:
        logger.error(f"解析失败，缺少关键字段：{e}")
    except Exception as e:
        logger.error(f"未知错误：{e}")

# 主程序
if __name__ == "__main__":
    f = open('国家公园马蜂窝.csv', 'w', encoding='utf-8', newline='')
    csv_f = csv.writer(f)
    csv_f.writerow(['标题', '链接', '发布时间', '内容'])

    cookies = {
        'PHPSESSID': 'dg8ieegn6uo4c2kgmfrif5ohe7',
        'mfw_uuid': '68551be8-f3a8-f276-d93f-f9976f908d2c',
        'oad_n': 'a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222025-06-20+16%3A29%3A28%22%3B%7D',
        'Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0': '1750408172',
        'HMACCOUNT': 'E59D6732DDD9D88D',
        'uva': 's%3A130%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1750408173%3Bs%3A10%3A%22last_refer%22%3Bs%3A62%3A%22https%3A%2F%2Fwww.mafengwo.cn%2Ftravel-scenic-spot%2Fmafengwo%2F10039.html%22%3Bs%3A5%3A%22rhost%22%3BN%3B%7D%22%3B',
        '__mfwurd': 'a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1750408173%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D',
        '__mfwuuid': '68551be8-f3a8-f276-d93f-f9976f908d2c',
        'bottom_ad_status': '0',
        '__omc_chl': '',
        '__mfwothchid': 'referrer%7Copen.weixin.qq.com',
        '__mfwc': 'referrer%7Copen.weixin.qq.com',
        '__mfwa': '1750408171491.73829.6.1750479376332.1750513409457',
        '__mfwlv': '1750513409',
        '__mfwvn': '4',
        'login': 'mafengwo',
        'mafengwo': 'cbdfd9807efdf82eec02d85703765a60_41304171_6856b83ce7ab41.44447843_6856b83ce7aba5.10835560',
        'uol_throttle': '41304171',
        'mfw_uid': '41304171',
        '__omc_r': '',
        '__mfwb': '993db846cdae.19.direct',
        '__mfwlt': '1750513774',
        'Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0': '1750513774',
        'w_tsfp': 'ltvuV0MF2utBvS0Q7KrslUipETwmczo4h0wpEaR0f5thQLErU5mA0YN7vczwNHHd5Mxnvd7DsZoyJTLYCJI3dwMcRp2ZIIAXiVuSloAgiY9HBBgzFJLVUFRKI7whuGRGe3hCNxS00jA8eIUd379yilkMsyN1zap3TO14fstJ019E6KDQmI5uDW3HlFWQRzaLbjcMcuqPr6g18L5a5TmN41ytL1gmVbJG2UzEhi8fCnon4EC7c+EPNEitJZqtSqA=',
    }

    headers = {
        'referer': 'https://www.mafengwo.cn/search/q.php?q=%E7%A5%9E%E5%86%9C%E6%9E%B6%E6%99%AF%E5%8C%BA&t=notes&seid=7DF2C827-840A-4840-8AC6-582E08982BDD',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
    }
    # 武夷山国家森林公园
    params = {
        'q': '武夷山国家森林公园',
        't': 'notes',
        'seid': '4B0D5453-EBA3-48F9-9270-3ED8FE090C09',
    }

    session = requests.session()
    response = session.get('https://www.mafengwo.cn/search/q.php', params=params, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    lists = soup.select('.att-list li')

    for item in lists:
        time.sleep(2)
        if item.select_one('.ct-text'):
            title = item.select_one('.ct-text h3 a').get_text()
            href = item.select_one('.ct-text h3 a').get('href')
            logger.info(f"处理攻略：{title} - {href}")
            match = re.search(r'/i/(\d+)\.html', href)
            if match:
                id = match.group(1)
                logger.info(f"提取到攻略ID：{id}")
            else:
                logger.error(f"未找到匹配的数字")
                continue
            all_content = ''
            get_detail(href, id)

    f.close()
    logger.info("所有攻略处理完成")