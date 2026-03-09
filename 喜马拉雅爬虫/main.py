import base64
import json
import sys
import time

from save_to_db import logger
import requests
import execjs

from save_to_db import DbSaver


saver = DbSaver()          # 全局实例
saver.init_database()
logger.info('初始化数据库')

ctx = execjs.compile(open('js/1.js','r',encoding='utf-8').read())
# ---------- 工具函数 ----------
def safe_get_json(resp: requests.Response, default=None):
    """防 json 解析炸掉"""
    try:
        return resp.json()
    except Exception as e:
        logger.warning(f'JSON 解析失败: {e}  url={resp.url}')
        return default or {}

def get_key(uid):
    if not ctx:
        return {}
    try:
        uuid = ctx.call('generate')
        params = {'v': '1.2.0', 'e': '1', 'c': '1', 'r': uuid}
        timestr = int(time.time()*1000)
        data = ctx.call('get_buffer',timestr,uid)

        resp = requests.post('https://hdaa.shuzilm.cn/report',
                             params=params, headers=headers,
                             data=base64.b64decode(data), timeout=10)
        return json.loads(ctx.call('aesDecrypt', resp.text, "m9ZtRrz:qujT8@da"))
    except Exception as e:
        logger.error(f'get_key 失败: {e}')
        return {}

def update_headers(uid):
    """失败不影响主流程"""
    try:
        json_data = get_key(uid)
        xm_sign = 'D2U9qkIfZDRb6kI0MdFy/2ME2YDNkmugkYSmw2YoM5OggXa5&&' + json_data.get('sid', '')
        headers['xm-sign'] = xm_sign
    except Exception as e:
        logger.warning(f'更新 xm-sign 失败: {e}')

# ---------- 业务接口 ----------
def get_album(album_id: int):
    try:
        resp = requests.get('https://www.ximalaya.com/revision/album/v1/simple',
                            params={'albumId': album_id},
                            cookies=cookies, headers=headers, timeout=10)
        data = safe_get_json(resp, {}).get('data', {}).get('albumPageMainInfo', {})
        return {
            'updateDate': data.get('updateDate'),
            'createDate': data.get('createDate'),
            'anchorUid': data.get('anchorUid'),
            'playCount': data.get('playCount', 0),
        }
    except Exception as e:
        logger.error(f'get_album 失败 album_id={album_id}: {e}')
        return {}

def get_anchor(anchor_uid: int):
    try:
        resp = requests.get('https://www.ximalaya.com/revision/user/basic',
                            params={'uid': anchor_uid, 'needRealCount': 'true'},
                            cookies=cookies, headers=headers, timeout=10)
        data = safe_get_json(resp, {}).get('data', {})
        return {
            'nickName': data.get('nickName', ''),
            'fansCount': data.get('fansCount', 0),
        }
    except Exception as e:
        logger.error(f'get_anchor 失败 anchor_uid={anchor_uid}: {e}')
        return {'nickName': '', 'fansCount': 0}

def get_ablum_comment(ablum_uid: int):
    try:
        params = {
            'albumId': ablum_uid,
            'order': 'content-score-desc',
            'pageId': '1',
            'pageSize': '10',
        }

        resp= requests.get(
            'https://mobile.ximalaya.com/album-comment-mobile/web/album/comment/list/query/{}'.format(int(time.time()*1000)),
            params=params,
            headers=headers,
        )
        data = safe_get_json(resp, {}).get('data', {})
        return {
            'comments_count': data.get('allCommentsCount'),
            'score': data.get('recScoreSummary',{}).get('score',0),
        }
    except Exception as e:
        logger.error(f'get_album comment 失败 album_id={album_id}: {e}')
        return {}

def getTracksList(album_id: int):
    try:
        resp = requests.get('https://www.ximalaya.com/revision/album/v1/getTracksList',
                            params={'albumId': album_id, 'pageNum': 1, 'pageSize': 30},
                            cookies=cookies, headers=headers, timeout=10)
        print(resp.json())
        return safe_get_json(resp, {}).get('data', {}).get('tracks', [])
    except Exception as e:
        logger.error(f'getTracksList 失败 album_id={album_id}: {e}')
        return []

def getdescTracksList(album_id: int):
    try:
        resp = requests.get('https://www.ximalaya.com/revision/album/v1/getTracksList',
                            params={'albumId': album_id, 'pageNum': 1, 'sort':1,'pageSize': 30},
                            cookies=cookies, headers=headers, timeout=10)
        print(resp.json())
        return safe_get_json(resp, {}).get('data', {}).get('tracks', [])
    except Exception as e:
        logger.error(f'getTracksList 失败 album_id={album_id}: {e}')
        return []

cookies = {
    '_xmLog': 'h5&5636fee6-36c8-42d0-85d0-bad665de84dd&process.env.sdkVersion',
    'Qs_lvt_476196': '1756633866',
    'Qs_pv_476196': '1089799915938283900',
    'wfp': 'ACM4MjdlYTExMWI4N2ZiMDc5XQIGu3GKBpZ4bXdlYl93d3c',
    'HWWAFSESID': 'abd6f1425c0cc04dec5',
    'HWWAFSESTIME': '1757561303998',
    'DATE': '1756633864988',
    'crystal': 'U2FsdGVkX19vuJiJbV2/gsCCRa5c9mvSS989uUeG9fsXGtU8M+/FipflCNQnGnsokZytynC6U7TZ+URtpSoNxRuFUibrAK+2/a04F0zMKsfoPnziPMtsYsFudIm9Oid3sL4mxY11arI1PBxmmICrSc+sQ/tkiVuwIi7RGi7D+ddpInUxbo6Py419Wfvl3QQi7LD/HWGoTC4a6DRjwI+XxRv0tkjsvO8eLf4DiAth4O7nQVgnQcNFOAp4JoZcJhc9',
    'xm-page-viewid': 'ximalaya-web',
    'impl': 'www.ximalaya.com.login',
    'Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070': '1756634342,1757561307',
    'HMACCOUNT': 'BE226A4D7F526496',
    '1&remember_me': 'y',
    '1&_token': '504055208&8A9BE9C0140N79CFE682AA5F59905DBAE5BFCBB966632983A897B9866A835F7A723AFF4485CE158M88AED0480C6DC46_',
    '1_l_flag': '504055208&8A9BE9C0140N79CFE682AA5F59905DBAE5BFCBB966632983A897B9866A835F7A723AFF4485CE158M88AED0480C6DC46__2025-09-1612:39:58',
    'web_login': '1758092042314',
    'Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070': '1758092042',
    'cmci9xde': 'U2FsdGVkX19V8QAbj/wFqWHk0xLnFwY6b2KIqex9rY/sOdHm+5eWAGF9L4iYvpMqNyIvSFT4jeDzkNuhZpaILw==',
    'pmck9xge': 'U2FsdGVkX19W04hHp0fneSbqXMy6u+oQWrUQjaZb6EM=',
    'assva6': 'U2FsdGVkX1+qnI25xlgdhmKHgp0+61AzTNSTHXfiMR0=',
    'assva5': 'U2FsdGVkX1/OmxxPvz74p2yAs1PVwWC4tLW+w9L//e9s4aSf0oiBl3jsPdY0S3lwaz3m8bLj8d90Tl8oQQ97ng==',
    'vmce9xdq': 'U2FsdGVkX1+nBgsHnPu0jEAynqgqUzlLYjcSv8uesUS39v4SKTR3l0k56UACXCK6YUoGLVww7vZdz7XfQXUUeFrxtNhnPdmGvZW4mP6HxseyF5kiqKyBsKQYDTfztci73hJuW1s7sfw+mvkuNvDybxxzCTzKgSsnzMkQ7NyMMSM=',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    # 'Cookie': 'HWWAFSESID=a69522cbc04a53b2f7e; HWWAFSESTIME=1756633860884; _xmLog=h5&5636fee6-36c8-42d0-85d0-bad665de84dd&process.env.sdkVersion; DATE=1756633864988; crystal=U2FsdGVkX19vuJiJbV2/gsCCRa5c9mvSS989uUeG9fsXGtU8M+/FipflCNQnGnsokZytynC6U7TZ+URtpSoNxRuFUibrAK+2/a04F0zMKsfoPnziPMtsYsFudIm9Oid3sL4mxY11arI1PBxmmICrSc+sQ/tkiVuwIi7RGi7D+ddpInUxbo6Py419Wfvl3QQi7LD/HWGoTC4a6DRjwI+XxRv0tkjsvO8eLf4DiAth4O7nQVgnQcNFOAp4JoZcJhc9; impl=www.ximalaya.com.login; Qs_lvt_476196=1756633866; Qs_pv_476196=1089799915938283900; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1756634342; HMACCOUNT=9D4C89992E46B08A; xm-page-viewid=ximalaya-web; wfp=ACM4MjdlYTExMWI4N2ZiMDc5XQIGu3GKBpZ4bXdlYl93d3c; 1&remember_me=y; 1&_token=504055208&45202170240NEC27ADAD017DF49FE356A1031A4B7AC2395B17C616A6D6DED36573ECDDFF1B5836M03F7096405AD772_; 1_l_flag=504055208&45202170240NEC27ADAD017DF49FE356A1031A4B7AC2395B17C616A6D6DED36573ECDDFF1B5836M03F7096405AD772__2025-09-0408:55:28; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1756947332; web_login=1756947338834; cmci9xde=U2FsdGVkX1+qPSYilbxylJECPkSXQo6mGujhwN9ulT6/aGUS4eMXUM9wY1sWZgUKFnfpLdFXjc3GtauUc9VZGQ==; pmck9xge=U2FsdGVkX1+ZOtZI1OkK34GyU1xGcodK5YsNTMexx88=; assva6=U2FsdGVkX18xPtJxvNchnDvyYjnR51a2xThtdylsVXA=; assva5=U2FsdGVkX19MpxHDTTpef1xLsXuA2xO8Js/VCPDBYFcrsXsX2n1zomCduf327kSOF/cLbrtpB/+uEvhVi5YP+Q==; vmce9xdq=U2FsdGVkX1/H8seZqvDIodL6VDcdpZHVU7T2BhICR30sN6trsoGkhw4ZFci1iANMBcnIGAhjMJGTfl+ZismzDhN/iLDxo30+17iromg37mrMp7RY5OJ/6YXv46RpmXn4zZN7NYElYUShe96OZFY3Ep1dtF6u+ijc3t7c+tk047A=',
    'Pragma': 'no-cache',
    'Referer': 'https://www.ximalaya.com/top/1/100150/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}
# 全局：待补章节的集合
pending_album_ids = set()          # 只存 album_id
pending_meta = {}
lists = [
  {
    "tabId": 2,
    "id": 2,
    "name": "热门",
    "position": 1,
    "rankingId": 100077
  },
  {
    "tabId": 2,
    "id": 283,
    "name": "新品",
    "position": 2,
    "rankingId": 100157
  },
  {
    "tabId": 2,
    "id": 325,
    "name": "免费",
    "position": 3,
    "rankingId": 100224
  },
  {
    "tabId": 2,
    "id": 304,
    "name": "口碑",
    "position": 4,
    "rankingId": 100191
  },
  {
    "tabId": 2,
    "id": 329,
    "name": "月票",
    "position": 6,
    "rankingId": 100332
  },
  {
    "tabId": 2,
    "id": 331,
    "name": "男生",
    "position": 7,
    "rankingId": 100330
  },
  {
    "tabId": 2,
    "id": 80,
    "name": "都市",
    "position": 10,
    "rankingId": 100078
  },
  {
    "tabId": 2,
    "id": 81,
    "name": "玄幻",
    "position": 11,
    "rankingId": 100079
  },
  {
    "tabId": 2,
    "id": 82,
    "name": "悬疑",
    "position": 12,
    "rankingId": 100080
  },
  {
    "tabId": 2,
    "id": 83,
    "name": "历史",
    "position": 13,
    "rankingId": 100081
  },
  {
    "tabId": 2,
    "id": 84,
    "name": "科幻",
    "position": 14,
    "rankingId": 100082
  },
  {
    "tabId": 2,
    "id": 85,
    "name": "游戏",
    "position": 15,
    "rankingId": 100083
  },

]

fengkong_flag = False
_exception_time = None               # 异常发生时刻
for abluml_item in lists:
    rankingId = abluml_item['rankingId']
    params = {
        'rankingId': rankingId,
    }
    update_headers(rankingId)
    response = requests.get('https://www.ximalaya.com/revision/rank/v4/element', params=params, cookies=cookies, headers=headers)

    category_name = abluml_item['name']
    print(f"榜单{category_name}===============")
    category_id = saver.get_or_create_category(category_name)
    rankList = response.json()['data']['rankList'][0]['albums']
    # 榜单循环内部
    for index, item in enumerate(rankList):
        time.sleep(2)
        album_id = item['id']
        albumTitle = item['albumTitle']
        print(f'排名{index + 1}', albumTitle, '===============================')

        update_headers(album_id)
        time.sleep(1)
        album_data = get_album(album_id)  # 你自己的函数
        album_datacomment = get_ablum_comment(album_id)  # 你自己的函数
        album_data.update(album_datacomment)
        if not album_data:
            continue
        update_headers(album_id)
        time.sleep(1)
        anchor_data = get_anchor(album_data['anchorUid'])
        album_data['albumTitle'] = albumTitle  # 补全字段
        album_data['anchorName'] = anchor_data['nickName']
        album_data['fansCount'] = anchor_data['fansCount']
        album_data['playCount'] = album_data.get('playCount', 0)
        album_data['commentCount'] = item.get('commentCount', 0)
        album_data['trackCount'] = item.get('trackCount', 0)
        album_data['albumId'] = album_id

        logger.info('小说信息{}'.format(album_data))

        # 1. 写/更新小说详情
        note_id = saver.save_album(
            category_id=category_id,
            rank_position=index + 1,
            album_data=album_data,
            anchor_data=anchor_data)

        # 没有封控 或者 封控时间 过了 20分钟
        if not fengkong_flag or time.time() - _exception_time > 20 * 60:
            time.sleep(1)
            update_headers(album_id)
            # 2. 写/更新章节
            tracks = getTracksList(album_id)
            desctracks = getdescTracksList(album_id)
            if len(tracks) == 0:  # 触发滑块
                logger.warning(f'封控出现，专辑 {album_id} 章节稍后补爬')
                fengkong_flag = True
                _exception_time = time.time()
                # 把补课时需要的元数据也暂存下来
                pending_meta[album_id] = {
                    'note_id': note_id,
                    'albumTitle': albumTitle,
                    'nickName': anchor_data['nickName'],
                    'category_id': category_id
                }
                pending_album_ids.add(album_id)
                continue
                # 有封控 加入待做列表
        else:
            logger.warning(f'封控出现，专辑 {album_id} 章节稍后补爬')
            # 把补课时需要的元数据也暂存下来
            pending_meta[album_id] = {
                'note_id': note_id,
                'albumTitle': albumTitle,
                'nickName': anchor_data['nickName'],
                'category_id': category_id
            }
            pending_album_ids.add(album_id)
            continue
        saver.save_tracks(
            note_id=note_id,
            albumTitle=albumTitle,
            nickName=anchor_data['nickName'],
            category_id=category_id,
            tracks=tracks,
        chapter_order_type='ASC')

        saver.save_tracks(
            note_id=note_id,
            albumTitle=albumTitle,
            nickName=anchor_data['nickName'],
            category_id=category_id,
            tracks=desctracks,
            chapter_order_type='DESC')

        logger.info(f'《{albumTitle}》 榜单={category_name} 排名={index + 1} 章节数={len(tracks)} 已入库')


# ------------------------------------------------------------------
# 2. 所有榜单扫完后，集中补课
# ------------------------------------------------------------------
if pending_album_ids:
    logger.info(f'共有 {len(pending_album_ids)} 张专辑需要补爬章节')
    for album_id in pending_album_ids:
        time.sleep(1)
        update_headers(album_id)
        meta = pending_meta[album_id]
        logger.info(f'开始补爬 《{meta["albumTitle"]}》 章节')

        # 过滑块/验证码，拿到章节
        tracks = getTracksList(album_id)
        update_headers(album_id)
        desctracks = getdescTracksList(album_id)
                  # 你自己的破解函数
        # if not tracks:                        # 还是拿不到就人工或重试
        #     tracks = crack_one(album_id)
        if not tracks:  # 还是拿不到就人工或重试
            logger.error(f'专辑 {album_id} 补爬仍失败，请手动处理')
            continue

        # 写库
        saver.save_tracks(
            note_id=meta['note_id'],
            albumTitle=meta['albumTitle'],
            nickName=meta['nickName'],
            category_id=meta['category_id'],
            tracks=tracks,
        chapter_order_type='ASC')

        saver.save_tracks(
            note_id=meta['note_id'],
            albumTitle=meta['albumTitle'],
            nickName=meta['nickName'],
            category_id=meta['category_id'],
            tracks=tracks,
        chapter_order_type='DESC')


        logger.info(f'补课完成 《{meta["albumTitle"]}》 章节数={len(tracks)}')


