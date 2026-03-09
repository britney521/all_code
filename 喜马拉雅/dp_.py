# 多线程并发的
import base64
import io
import json
import re
import time
from datetime import datetime

import requests
from DrissionPage import Chromium,ChromiumOptions
from concurrent.futures import ThreadPoolExecutor
from loguru import logger
from PIL import Image
from matplotlib import pyplot as plt

ALL_DATA  = {}
# 点击分类
def get_subcate():
    # tab.get('https://www.ximalaya.com/top/2/100077')
    # tab.wait.doc_loaded()
    # cate_btn = tab.ele('css:.sub-category .rank')
    # cate_btn.click()
    links = tab.eles('css:.subbar-wrapper .sub-link')
    for link in links:
        href = link.attr('href')
        name = link.text
        new_tab = browser.new_tab()
        new_tab.get(href)
        new_tab.wait.doc_loaded()
        logger.info('点击{}分类==========='.format(name))

        get_notes(new_tab, name)  # 把 name 传进去
        new_tab.close()


# 获取小说
def get_notes(new_tab, cate_name):
    items = new_tab.eles('css:.album-item')
    logger.info(f'分类 {cate_name} 捕获到 {len(items)} 本小说')

    # 该分类的容器
    if cate_name not in ALL_DATA:
        ALL_DATA[cate_name] = []

    for item in items:
        tab.wait(5)
        href = item.ele('css:a.album-right').attr('href')
        title = item.ele('css:.title').text
        novel_tab = browser.new_tab()
        novel_tab.listen.start(['album/v1/simple',
                                'revision/user/basic',
                                'album/v1/getTracksList'])
        novel_tab.get(href)
        logger.info(f'  采集小说：{title}')
        try:
            get_detail_apis(novel_tab, cate_name)   # 把分类名继续往下传
        except Exception as e:
            logger.error(f'{title}{e}')
            continue



def get_ablum_detail(data_packet):

    res = data_packet.response.body
    data = res['data']['albumPageMainInfo']
    title = data['albumTitle']
    anchorName = data['anchorName']
    cover = data['cover']
    createDate = data['createDate']
    updateDate = data['updateDate']
    playCount = data['playCount']
    categoryId = data['categoryId']
    logger.info('ablum_detail {}'.format( {
        'title': title,
        'cover': cover,
        'anchorName': anchorName,
        'createDate': createDate,
        'updateDate': updateDate,
        'playCount': playCount,
        'categoryId': categoryId,
    }))
    return {
        'title': title,
        'cover': cover,
        'anchorName': anchorName,
        'createDate': createDate,
        'updateDate': updateDate,
        'playCount': playCount,
        'categoryId': categoryId,
    }

def get_userinfo(data_packet):

    res = data_packet.response.body
    data = res['data']
    nickName = data.get('nickName')
    fansCount = data['fansCount']
    logger.info('userinfo {}'.format({
        'nickName': nickName,
        'fansCount': fansCount,
    }))

    return {
        'nickName': nickName,
        'fansCount': fansCount,
    }

def get_getTracksList(data_packet):

    res = data_packet.response.body
    datas = res['data']['tracks'][2:]
    all_TracksList = []
    for data in datas:
        albumTitle = data['albumTitle']
        title = data['title']
        anchorName = data['anchorName']
        createDateFormat = data['createDateFormat']
        playCount = data['playCount']
        all_TracksList.append({
            'albumTitle': albumTitle,
            'title': title,
            'createDateFormat': createDateFormat,
            'playCount': playCount,
            'anchorName': anchorName

        })
    logger.info('TracksList {}'.format(all_TracksList))

    return all_TracksList

def get_detail_apis(new_tab,cate_name):
    data_packets = new_tab.listen.wait(count=3)
    logger.info('捕获到包个数{}'.format(len(data_packets)))
    if len(data_packets) == 3:
        album = get_ablum_detail(data_packets[0])
        user = get_userinfo(data_packets[1])
        tracks = get_getTracksList(data_packets[2])

        # 组装成一本小说的完整信息
        novel_info = {
            'album': album,
            'user': user,
            'tracks': tracks
        }
        ALL_DATA[cate_name].append(novel_info)
        logger.info(f'  已入库 {album["title"]}，当前分类{cate_name}共 {len(ALL_DATA[cate_name])} 本')


    new_tab.close()
    # playcount = new_tab.ele('css:.info .count').text
    # author = new_tab.ele('css:.xui-card .nick-name').text
    # fans_count = new_tab.ele('css:.xui-card .anchor-stats a:nth-child(3)').text
    # fans_count = new_tab.ele('css:.xui-card .anchor-stats a:nth-child(3)').text




def check_login():
    login_btn = tab.ele('css:.login-btn')
    return login_btn

# tab.close()
if __name__ == '__main__':
    op = ChromiumOptions().set_paths('/Applications/GPT Chrome.app/Contents/MacOS/GptBrowser')
    # 创建页面对象
    browser = Chromium(op)

    tab = browser.new_tab()
    tab.get("https://www.ximalaya.com/top/2/100077")

    tab.wait.doc_loaded()
    get_subcate()
    # ---------- 写 JSON ----------
    file_name = f'ximalaya_full_{datetime.now():%Y%m%d_%H%M%S}.json'
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(ALL_DATA, f, ensure_ascii=False, indent=2)
    logger.info(f'全部完成，已写入 {file_name} 共 {len(ALL_DATA)} 个分类')
