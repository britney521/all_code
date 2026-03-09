import time
import requests
import csv
import re
from loguru import logger
import os

session = requests.session()

headers = {
    'referer': 'https://you.ctrip.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
}



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


def get_poid(href):
    try:
        response = session.get(href, headers=headers, timeout=10)
        response.raise_for_status()  # 检查响应状态码是否为 200
        # 使用正则表达式提取 poiId 的值
        match = re.search(r'"poiId":(\d+)', response.text)
        guid = response.cookies.get('GUID')  # 假设 cookies 中的键是 'GUID'
        if guid:
            logger.info(f"提取的 GUID 值：{guid}")
        if match:
            poi_id = match.group(1)  # 提取匹配的数字部分
            logger.info(f"提取的 poiId 值：{poi_id}")
            return poi_id, guid
        else:
            logger.warning("未找到 poiId")
            return None, None
    except requests.RequestException as e:
        logger.error(f"请求 {href} 时发生错误: {e}")
        return None, None


dataset = [
    # {"name": "神农架景区", "value": "https://you.ctrip.com/sight/shennongjia147/136351.html",'spot_name':'神龙架'},
    # {"name": "神农顶", "value": "https://you.ctrip.com/sight/shennongjia147/9288.html",'spot_name':'神龙架'},
    # {"name": "大九湖国家湿地公园", "value": "https://you.ctrip.com/sight/shennongjia147/136247.html",'spot_name':'神龙架'},
    {"name": "神农架国际滑雪场", "value": "https://you.ctrip.com/sight/shennongjia147/142062.html",'spot_name':'神龙架'},
    {"name": "天燕旅游区", "value": "https://you.ctrip.com/sight/shennongjia147/136366.html?renderPlatform=",'spot_name':'神龙架'},
    {"name": "官门山", "value": "https://you.ctrip.com/sight/shennongjia147/136260.html",'spot_name':'神龙架'}, {"name": "沱沱河",
                                                                                            "value": "https://you.ctrip.com/sight/golmud332/147295.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
                                                                                            "spot_name": "三江源国家公园"},
    {"name": "错那湖",
     "value": "https://you.ctrip.com/sight/amdocounty120385/109941.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "三江源国家公园"},
    {"name": "扎陵湖与鄂陵湖",
     "value": "https://you.ctrip.com/sight/madoi120480/133386.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "三江源国家公园"},
    {"name": "昂赛大峡谷",
     "value": "https://you.ctrip.com/sight/zadoi1446310/5713542.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "三江源国家公园"},
    {"name": "青海省三江源玛多国家公园",
     "value": "https://you.ctrip.com/sight/madoi120480/5718131.html?renderPlatform=", "spot_name": "三江源国家公园"},
    {"name": "三江源国家级自然保护区", "value": "https://you.ctrip.com/sight/chindu1446316/50054.html?renderPlatform=",
     "spot_name": "三江源国家公园"},
    {"name": "可可西里自然保护区",
     "value": "https://you.ctrip.com/sight/zhidoicounty1446321/2499293.html?renderPlatform=",
     "spot_name": "三江源国家公园"},
    {"name": "大熊猫国家公园整体", "value": "https://you.ctrip.com/sight/yaan917/5718125.html?renderPlatform=",
     "spot_name": "大熊猫国家公园"},
    {"name": "四川王朗自然保护区",
     "value": "https://you.ctrip.com/sight/pingwu3134/61304.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "大熊猫国家公园"},
    {"name": "都江堰熊猫谷", "value": "https://you.ctrip.com/sight/dujiangyan911/1700731.html?renderPlatform=",
     "spot_name": "大熊猫国家公园"},
    {"name": "二郎山喇叭河景区",
     "value": "https://you.ctrip.com/sight/tianquan2056/63907.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "大熊猫国家公园"},
    {"name": "红河谷森林公园",
     "value": "https://you.ctrip.com/sight/meicounty2776/55213.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "大熊猫国家公园"},
    {"name": "卧龙唐家河",
     "value": "https://you.ctrip.com/sight/qingchuan1446240/75802.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "大熊猫国家公园"},
    {"name": "佛坪熊猫谷", "value": "https://you.ctrip.com/sight/fopingcounty2051/1731170.html", "spot_name": "大熊猫国家公园"},
    {"name": "黑龙江洪河国家级自然保护区",
     "value": "https://you.ctrip.com/sight/tongjiang1446004/17460.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "东北虎国家公园"},
    {"name": "东北虎豹国家公园", "value": "https://you.ctrip.com/sight/jilin267/5718130.html?renderPlatform=",
     "spot_name": "东北虎国家公园"},
    {"name": "五指山水满河热带雨林风景区",
     "value": "https://you.ctrip.com/sight/wuzhishan982/110178.html?renderPlatform=", "spot_name": ""},
    {"name": "海南热带雨林国家公园",
     "value": "https://you.ctrip.com/sight/wuzhishan982/3211.html?renderPlatform=", "spot_name": ""},
    {"name": "五指山大峡谷漂流", "value": "https://you.ctrip.com/sight/wuzhishan982/132025.html?renderPlatform=",
     "spot_name": "海南热带雨林国家公园"},
    {"name": "太平山瀑布", "value": "https://you.ctrip.com/sight/wuzhishan982/3208.html?renderPlatform=",
     "spot_name": "海南热带雨林国家公园"},
    {"name": "水满毛纳生态旅游区", "value": "https://you.ctrip.com/sight/wuzhishan982/148914415.html?renderPlatform=",
     "spot_name": "海南热带雨林国家公园"},
    {"name": "吊罗山国家森林公园",
     "value": "https://you.ctrip.com/sight/lingshui1509/21835.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "海南热带雨林国家公园"},
    {"name": "五指山方诺寨热带雨林", "value": "https://you.ctrip.com/sight/wuzhishan982/148892455.html?renderPlatform=",
     "spot_name": "海南热带雨林国家公园"},
    {"name": "水满乡", "value": "https://you.ctrip.com/sight/wuzhishan982/5068582.html?renderPlatform=",
     "spot_name": "海南热带雨林国家公园"},
    {"name": "黎母山国家森林公园",
     "value": "https://you.ctrip.com/sight/qiongzhong844/18195.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "海南热带雨林国家公园"},
    {"name": "武夷山国家公园", "value": "https://you.ctrip.com/sight/wuyishan22/126481.html?renderPlatform=",
     "spot_name": "福建武夷山国家公园"},
    {"name": "武夷山国家森林公园", "value": "https://you.ctrip.com/sight/wuyishan22/140526.html?renderPlatform=",
     "spot_name": "福建武夷山国家公园"},
    {"name": "九曲溪竹筏漂流",
     "value": "https://you.ctrip.com/sight/wuyishan22/1407533.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "福建武夷山国家公园"},
    {"name": "天游峰",
     "value": "https://you.ctrip.com/sight/wuyishan22/4383.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "福建武夷山国家公园"},
    {"name": "大红袍景区",
     "value": "https://you.ctrip.com/sight/wuyishan22/4375.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "福建武夷山国家公园"},
    {"name": "一线天",
     "value": "https://you.ctrip.com/sight/emeishan24/55026.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "福建武夷山国家公园"},
    {"name": "虎啸岩片区",
     "value": "https://you.ctrip.com/sight/wuyishan22/4151.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "福建武夷山国家公园"},
    {"name": "月亮湾",
     "value": "https://you.ctrip.com/sight/wuyishan22/147150521.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "福建武夷山国家公园"},
    {"name": "龙川峡谷",
     "value": "https://you.ctrip.com/sight/wuyishan22/18086.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "福建武夷山国家公园"},
    {"name": "浙江钱江源国家公园", "value": "https://you.ctrip.com/sight/kaihua1001/135778.html?renderPlatform=",
     "spot_name": "浙江钱江源国家公园"},
    {"name": "莲花塘景区",
     "value": "https://you.ctrip.com/sight/kaihua1001/144516.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "浙江钱江源国家公园"},
    {"name": "南山牧场", "value": "https://you.ctrip.com/sight/chengbu2814/135002.html?renderPlatform=",
     "spot_name": "湖南南山国家公园"},
    {"name": "南山风景名胜区",
     "value": "https://you.ctrip.com/sight/chengbu2814/141353.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "湖南南山国家公园"},
    {"name": "属都湖",
     "value": "https://you.ctrip.com/sight/shangrila106/12296.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "云南普达措国家公园"},
    {"name": "碧塔海",
     "value": "https://you.ctrip.com/sight/shangrila106/4212.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "云南普达措国家公园"},
    {"name": "普达措国家公园",
     "value": "https://you.ctrip.com/sight/shangrila106/56571.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "云南普达措国家公园"},
    {"name": "仙米国家森林公园",
     "value": "https://you.ctrip.com/sight/menyuan1446317/1695501.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "祁连山国家公园"},
    {"name": "岗什卡雪峰",
     "value": "https://you.ctrip.com/sight/menyuan1446317/1713881.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "祁连山国家公园"},
    {"name": "卓尔山", "value": "https://you.ctrip.com/sight/qilian120123/147838.html?renderPlatform=",
     "spot_name": "祁连山国家公园"},
    {"name": "祁连山草原",
     "value": "https://you.ctrip.com/sight/qilian120123/1713861.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "祁连山国家公园"},
    {"name": "黑河大峡谷（祁连县）",
     "value": "https://you.ctrip.com/sight/qilian120123/1942478.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "祁连山国家公园"},
    {"name": "哈拉湖（青海德令哈）",
     "value": "https://you.ctrip.com/sight/delingha891/1713871.html?renderPlatform=#ctm_ref=www_hp_bs_lst",
     "spot_name": "祁连山国家公园"}
]

f = open('携程点评.csv', 'a', encoding='utf-8', newline='')
csv_f = csv.writer(f)
csv_f.writerow(['景区', '链接', '发布时间', '内容'])

for item_ in dataset:
    name = item_['name']
    spot_name = item_['spot_name']
    logger.info(f'正在处理景点 {name}')
    value = item_['value']
    poi_id, guid = get_poid(value)

    if not poi_id or not guid:
        logger.warning(f"跳过 {name}，未获取到必要的信息")
        continue

    params = {
        '_fxpcqlniredt': guid,
        'x-traceID': f'{guid}-{int(time.time() * 1000)}-7424549',
    }
    total_num = 300
    i = 1
    while i < total_num:
        try:
            time.sleep(2)
            json_data = {
                'arg': {
                    'channelType': 2,
                    'collapseType': 0,
                    'commentTagId': 0,
                    'pageIndex': i,
                    'pageSize': 10,
                    'poiId': poi_id,
                    'sourceType': 1,
                    'sortType': 3,
                    'starType': 0,
                },
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
            session.options('https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList',
                            params=params, headers=headers)

            response = session.post(
                'https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList',
                params=params,
                headers=headers,
                json=json_data,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            if 'result' not in data or 'items' not in data['result']:
                logger.warning(f"未找到有效数据，可能已到达最后一页或数据格式有误")
                break
            logger.info(f'正在获取{name}第{i}页评论')
            datas = data['result']['items']

            for item in datas:
                images = item['images']
                images_url = [image['imageSrcUrl'] for image in images]
                download_images(images_url,spot_name)
                content = item.get('content', '无内容')
                publishTypeTag = item.get('publishTypeTag', '无发布时间')
                csv_f.writerow([name, value, publishTypeTag, content])
            i += 1
        except requests.RequestException as e:
            _, guid = get_poid(value)
            logger.error(f"请求点评数据时发生错误: {e}")
            break
        except Exception as e:
            logger.error(f"处理数据时发生错误: {e}")
            break

    time.sleep(2)

f.close()
logger.info("数据抓取完成")
