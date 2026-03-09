from collections import OrderedDict

import requests
import json
import re
import hashlib
import time

# 获取当前时间戳（毫秒级）
eP = int(time.time() * 1000)
def generate_md5_signature(productid,page,token):
    # 固定参数
    eS = "12574478"

    # 构造JSON字符串（注意保持和JS完全一致，包括空格和字段顺序）
    json_data = {
        "showTrueCount": False,
        "auctionNumId": str(productid),
        "pageNo": page,
        "pageSize": 20,
        "rateType": "",
        "searchImpr": "-8",
        "orderType": "",
        "expression": "", # 10231014-13  差评
        "rateSrc": "pc_rate_list"
    }
    json_str = json.dumps(json_data, separators=(',', ':'))  # 去除空格，保持紧凑格式

    # 拼接待加密字符串
    string_to_hash = f"{token}&{eP}&{eS}&{json_str}"

    # MD5加密
    md5_hash = hashlib.md5(string_to_hash.encode('utf-8')).hexdigest()

    return md5_hash,json_str
cookies = {
    'cna': 'AmhFIX/sg1sBASoCbqCoyO/x',
    'xlly_s': '1',
    'lid': '%E5%B8%83%E5%85%B0%E5%A6%AEgreat',
    'wk_unb': 'UonciUrwAhKNfw%3D%3D',
    'dnk': '%5Cu5E03%5Cu5170%5Cu59AEgreat',
    'tracknick': '%5Cu5E03%5Cu5170%5Cu59AEgreat',
    'lgc': '%5Cu5E03%5Cu5170%5Cu59AEgreat',
    'cookie2': '1df6a65020f61d54cda9fed4ad317043',
    'cancelledSubSites': 'empty',
    't': '0daa8756fef7024b09fe0c5ba5ecea07',
    'sn': '',
    '_tb_token_': '5ad537555116d',
    'havana_sdkSilent': '1757343542784',
    'cookie3_bak': '1df6a65020f61d54cda9fed4ad317043',
    'env_bak': 'FM%2BgwZ4N3GAOJnyHXAITmd9IBxN4sbnFEsOs%2Bbs1aTob',
    'wk_cookie2': '11e78b7c5dd4e5ee5414a1ba00afd9a1',
    'cookie3_bak_exp': '1757576458809',
    '_l_g_': 'Ug%3D%3D',
    'cookie1': 'WvLEeeU9JXBlLInRXvpZ94RiEx71uUnjqWq3%2Fv35U3c%3D',
    'login': 'true',
    'sg': 't49',
    'uc1': 'cookie21=URm48syIYBrb0wDboXk1&cookie14=UoYbzNfYVXTApg%3D%3D&pas=0&cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=true&cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D',
    'uc3': 'nk2=0X7nDn%2BDuaAbsDo%3D&vt3=F8dD2fYBGqvFAV2xOH0%3D&id2=UonciUrwAhKNfw%3D%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D',
    'havana_lgc_exp': '1788428953550',
    'uc4': 'nk4=0%4000Z7ohQnczaLBI7JbMQ4C75TyEZ%2FDA%3D%3D&id4=0%40UOE2TvRA9Gq834g%2FIDxxqOP4CV2f',
    'unb': '1870847194',
    'cookie17': 'UonciUrwAhKNfw%3D%3D',
    '_nk_': '%5Cu5E03%5Cu5170%5Cu59AEgreat',
    'sgcookie': 'E100TEuEs6q6xyGzRTDOGyBA294pF14x6zIkXXF9X4CXKLGwlrFSeTqCZB03n0fZo2J8JIP3RaZ2ohM8EPeOpsrGWRcKOhx%2ByI9%2BqUUMmr2TYZITmZg5Py%2BE7giZzfLEmQmt',
    'csg': '982e92c9',
    'isg': 'BLKy6fo6DnO-LzJP1tFSpMU_A_6UQ7bdbVj8i3yL3mVQD1IJZNMG7bjs_6uzfy51',
    'mtop_partitioned_detect': '1',
    '_m_h5_tk': '011aa19d68475ad8d4d731df46886417_1757334700662',
    '_m_h5_tk_enc': 'd88fb4dc875cf7c4188b7465a1401424',
    'x5sectag': '527478',
    'x5sec': '7b2274223a313735373333303737342c22733b32223a2235366231326434316563376164623135222c22617365727665723b33223a22307c434e4c362b735547454d50757436482b2f2f2f2f2f774561444445344e7a41344e4463784f5451374f53494a5932467763485636656d786c4d4c375270717747227d',
    'tfstk': 'g7ZmL0T6LbOCyCtXoOmfkjxDYr_Jcmiss5Kt6chNzbl7XrhOlGXiZJuAh5FTrfVzZjyx6tZgrSwEk521hAla_5cTkaILh-isb6nGvMefv-ONiomw68ojB-DAt3SLh-9ynCWLzMpg8TUo3fPZu4lrpb-Z_nPZzglSCARqQnWuUbGrQhkZQbJrhAK235oNE8lSQck4_qWuUbMZbflO3hl3buZP_AkB4WP__uDmoXylRh-gXH3mT-ckb6ronXGU3bxwbXjQONya_1xtYyNuj2P1j3iYKzornzXwzju3uSH7sMxqgu240jEVwnh4c8zLX7Wwbf4z8Vl4P_ssuyNY84qRi3GUz82trz66kfUIQ5gQX6tjgRyQAynhjdDu-8ol4MYy8UN6fYWT4FTsuYMo9xlCn7Df0411ETYClqkSH6BlEFsxuYMP9TXk8m0qFxJA.',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 'cookie': 'cna=vq8TIfzK3AMBASQOA2i7Jciv; thw=xx; xlly_s=1; 3PcFlag=1754055147884; wk_cookie2=194dcd8e95ff959d2bbda300592b4f2f; wk_unb=UonciUrwAhKNfw%3D%3D; _hvn_lgc_=0; havana_lgc2_0=eyJoaWQiOjE4NzA4NDcxOTQsInNnIjoiNzE2NTEzYTA1OGIwODg1ZjAxMjhkNTBkNmMyNmQwNDciLCJzaXRlIjowLCJ0b2tlbiI6IjFQWVNMZTlKdndOUWt5ZU1JTFdQWDlRIn0; unb=1870847194; lgc=%5Cu5E03%5Cu5170%5Cu59AEgreat; cancelledSubSites=empty; cookie17=UonciUrwAhKNfw%3D%3D; dnk=%5Cu5E03%5Cu5170%5Cu59AEgreat; tracknick=%5Cu5E03%5Cu5170%5Cu59AEgreat; _l_g_=Ug%3D%3D; sg=t49; _nk_=%5Cu5E03%5Cu5170%5Cu59AEgreat; cookie1=WvLEeeU9JXBlLInRXvpZ94RiEx71uUnjqWq3%2Fv35U3c%3D; sn=; aui=1870847194; cookie2=137fad237ea73e13608be9ab31578f54; t=23868b9d1f7d30e779625e49fe7e2eb1; _tb_token_=3d68678e11bf7; mtop_partitioned_detect=1; _m_h5_tk=ab4e7749d8ce05e17e891baf0cb2890f_1754107960821; _m_h5_tk_enc=2dfa25941a2877f22a3796a0fe0dc65b; isg=BDo6UAyfBjgXn4rVtRwgh6g_i2Zc677FtXBk40Qz5k2YN9pxLHsO1QDEh8PrpzZd; _samesite_flag_=true; uc1=cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&existShop=true&cookie14=UoYbz9oxb9IPxw%3D%3D&pas=0&cookie21=URm48syIYBrb0wDboXk1&cookie15=UIHiLt3xD8xYTw%3D%3D; uc3=id2=UonciUrwAhKNfw%3D%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D&nk2=0X7nDn%2BDuaAbsDo%3D&vt3=F8dD2fnvkgN4yXt8EOs%3D; csg=e7977b22; skt=6ddffd3b77323320; existShop=MTc1NDEwMjEwOA%3D%3D; uc4=nk4=0%4000Z7ohQnczaLBI7JbMQ4CLiAlMWjkg%3D%3D&id4=0%40UOE2TvRA9Gq834g%2FIDxy3bP2xTkd; _cc_=Vq8l%2BKCLiw%3D%3D; sgcookie=E100vvt39sx2ctgZzHR6xm5LNO3OElrUF2dFKbQiFUF0W3I3UOw9NYvioP8NaNOt5V6npuzwYuWZp3Ls9gmCBHOj7g3AtUWp5Z6N7j2hkBzNdLVaxjuMyegYR4zW3sTC0t74; havana_lgc_exp=1785206108745; sdkSilent=1754130908745; havana_sdkSilent=1754130908745; tfstk=gDLKh8culfFLtw8dsBogZ7h7nzcg2cAe6pRbrTX3Vdp9KIthxQ6lyLpJe9jSLwYJBpAXxMAWr_TR8Fx3r9DFyQ9cyxDmoqAeTN7Snxfrp9SOlsZCN8fCfN_lwNqfslOeTaPas8iDfBP-S4lFda955G1cwa1CFgas6_CAFa6CVRZ1GO_5PgsQfR1PizaCOgG91O55P6sBFNGOwO6S_hHRCW6uyHBx-5-76VnxDFCdvTUlCzI95rjChBBTPx1A9dWXOOU7PthYY3OWFYUllnJ9yi9ryP7HMh_19hh7f9svApfweqUCdFdBR9YIIyXB8CtDrdG7PTK6cg6BbAuPAnJHcGLipPWXfCdlXhlzxTxVNLS2rxzFdQO2unbxy7C9DC_O47TDk9GanIX8AfhT4uSC_X1LLL3PwLoF6tcKyurPbf5Onfna4uSC_1Bmsgqz4GHf.',
    'referer': 'https://item.taobao.com/',
    'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}
def save_commnets(id):
    # 677276144260
    token = cookies['_m_h5_tk'].split('_')[0]
    for page in range(1,40):
        time.sleep(3)
        sign,json_str = generate_md5_signature(id,page,token)
        # print(sign,type(json_str))
        params = {
            'jsv': '2.7.5',
            'appKey': '12574478',
            't': str(eP),
            'sign': sign,
            'api': 'mtop.taobao.rate.detaillist.get',
            'v': '6.0',
            'isSec': '0',
            'ecode': '1',
            'timeout': '20000',
            'type': 'jsonp',
            'dataType': 'jsonp',
            'jsonpIncPrefix': 'pcdetail',
            'callback': 'mtopjsonppcdetail16',
            'data': json_str,
        }

        response = requests.get(
            'https://h5api.m.taobao.com/h5/mtop.taobao.rate.detaillist.get/6.0/',
            params=params,
            cookies=cookies,
            headers=headers,
        )
        if response.status_code == 200:
            pattern = r'\{.*\}'  # 匹配最外层的大括号内容
            text = response.text
            match = re.search(pattern, text)

            if match:
                json_str = match.group(0)

                data = json.loads(json_str)  # 转换为 Python 字典
                # print(data)
                datas = data['data'].get('rateList')
                if datas and  datas[0]['feedback'] not in ['该用户未及时主动评价，系统默认好评','该用户觉得商品非常好，给出好评',
                                                          '该用户觉得商品非常好，给出5星好评','该用户觉得商品还不错','该用户未填写评价内容']:
                    for item in datas:
                        print(item['feedback'])
                        csv_f.writerow([id,item['feedback']])
                else:
                    break


def extract_item_ids_from_file(file_path):
    """å
    从文本文件中读取淘宝/天猫链接，提取所有商品ID并去重
    :param file_path: 包含链接的文本文件路径
    :return: 去重后的商品ID列表
    """
    item_ids = OrderedDict()

    # 匹配淘宝/天猫商品ID的正则表达式
    id_pattern = re.compile(r'[?&]id=(\d+)')

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            # 方法1：使用正则表达式直接提取
            match = id_pattern.search(line)
            if match:
                item_ids[match.group(1)] = None

            # 方法2：使用urllib解析（更规范）
            # try:
            #     parsed = urlparse(line)
            #     params = parse_qs(parsed.query)
            #     if 'id' in params:
            #         item_ids.add(params['id'][0])
            # except Exception as e:
            #     print(f"解析链接出错: {line} - {str(e)}")

    return list(item_ids)

# save_commnets(677276144260,1000)

if __name__ == '__main__':
    keyword = '全麦' # 低GI  全麦
    import csv
    input_file = f"{keyword}tb.txt"  # 替换为你的文件路径
    ids = extract_item_ids_from_file(input_file)


    f = open(f'csv2/{keyword}.csv','a',encoding='utf-8',newline='')
    csv_f = csv.writer(f)


    print(f"共提取到 {len(ids)} 个唯一商品ID:")
    for i, item_id in enumerate(ids[60:]):
        time.sleep(2)
        print(f"{i}. {item_id}==============================================================")
        save_commnets(item_id)
