import time
import requests
import openpyxl  # 新增导入
import os  # 新增导入

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Cookie': 'JSESSIONID=09F33887F20532F8A0DE85DEEEE39F93; _ga_YZV5950NX3=GS1.1.1728438911.4.1.1728438956.0.0.0; CHSICC_CLIENTFLAGZSML=0c8d028b463214c9bf935767c881f8c6; JSESSIONID=033C172DABE0CEADE8374E3174EC41E6; CHSICC_CLIENTFLAGYZ=50f89a53d00bdeb77cb4758d73d823cf; XSRF-CCKTOKEN=d6e419df4bc5f3452fd5669af600f3ec',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

def get_ids_from_progress():
    """从 saved_dwdm.txt 中读取所有的 id"""
    if os.path.exists('saved_dwdm.txt'):
        with open('saved_dwdm.txt', 'r') as f:
            return [line.strip() for line in f.readlines()]  # 读取所有的 id
    return []

def log_progress(dwdm, page, last_zydm):
    """记录当前处理的 dwdm、页码和最后处理的 zydm 到 log.txt"""
    with open('log.txt', 'a') as f:  # 追加模式
        f.write(f'{dwdm}, {page}, {last_zydm}\n')  # 写入当前处理的 dwdm、页码和 zydm

def get_last_progress(dwdm):
    """获取指定 dwdm 的最后处理页码和 zydm"""
    if os.path.exists('log.txt'):
        with open('log.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(', ')
                if parts[0] == dwdm:
                    return int(parts[1]), parts[2]  # 返回最后处理的页码和 zydm
    return 1, None  # 默认从第1页开始

def get_zydm(dwdm, page=1, last_zydm=None):
    url = "https://yz.chsi.com.cn/zsml/rs/dwzys.do"
    data = {
        "dwdm": dwdm,
        "start": (page - 1) * 10,
        "curPage": page,
        "pageSize": "10",
    }
    response = requests.post(url, headers=headers, data=data).json()
    if '请登录' in response['msg']:
        print('请登录后重新运行')
        return

    list = response["msg"]["list"]
    startOfNextPage = response['msg']['startOfNextPage']
    totalCount = response['msg']['totalCount']

    print(f'[{dwdm}] 开始采集数据，当前页: {page}, 总页数: {totalCount // 10 + 1}')

    last_zydm_in_page = None  # 用于记录该页最后处理的 zydm

    for item in list:
        zydm = item["zydm"]
        zymc = item["zymc"]
        xwlxmc = item["xwlxmc"]
        print(f'学校:{dwdm}, 专业:{zydm}')
        get_details(dwdm, zydm, zymc, xwlxmc)

        last_zydm_in_page = zydm  # 更新最后处理的 zydm

        # 更新进度
        log_progress(dwdm, page, last_zydm_in_page)  # 写入当前处理的 dwdm、页码和 zydm
        time.sleep(1)

    if startOfNextPage >= totalCount:
        print(f'[{dwdm}] 数据采集完毕，已采集到第 {page} 页')
    else:
        print(f'[{dwdm}] 第 {page} 页采集完毕，继续采集下一页')
        page += 1
        time.sleep(2)
        get_zydm(dwdm, page)  # 修正了递归调用的参数

def get_details(dwdm, zydm, zymc, xwlxmc):
    url = "https://yz.chsi.com.cn/zsml/rs/yjfxs.do"
    data = {
        "zydm": zydm,
        "zymc": zymc,
        "dwdm": dwdm,
    }
    response = requests.post(url, headers=headers, data=data).json()
    if '请登录' in response['msg']:
        print('请登录后重新运行')
        return

    list = response["msg"]["list"]

    # 新增保存数据到xlsx的逻辑
    if not os.path.exists('data.xlsx'):  # 检查文件是否存在
        workbook = openpyxl.Workbook()  # 创建新的工作簿
        sheet = workbook.active
        # 添加表头
        sheet.append(['招生单位', '考试方式', '院系所', '专业', '学习方式', '研究方向', '拟招生人数', '指导教师',
                      '是否接收退役大学生士兵专项计划考生报考',
                      '是否接收少数民族高层次骨干计划考生报考', '备注', '政治', '外语', '业务课一', '业务课二', 'link'])
    else:
        workbook = openpyxl.load_workbook('data.xlsx')  # 加载工作簿
        sheet = workbook.active  # 获取活动工作表

    for i in list:
        招生单位 = f'({i["dwdm"]})({i["dwmc"]})'
        考试方式 = i['ksfsmc']
        院系所 = f'({i["yxsdm"]})({i["yxsmc"]})'
        专业 = f'({i["zydm"]})({xwlxmc})({i["zymc"]})'
        xxfs = i['xxfs']
        学习方式 = '全日制' if xxfs == '1' else '非全日制'
        研究方向 = f'({i["yjfxdm"]})({i["yjfxmc"]})'
        拟招生人数 = i['nzsrsstr']
        指导教师 = i['zdjs']

        是否接收退役大学生士兵专项计划考生报考 = '是' if i['tydxs'] == '1' else '否'
        是否接收少数民族高层次骨干计划考生报考 = '是' if i['jsggjh'] == '1' else '否'

        备注 = i['zybz']
        km2Vo = [f"({k['km2Vo']['kskmdm']}){k['km2Vo']['kskmmc']}" for k in i['kskmz']]

        政治 = f"({i['kskmz'][0]['km1Vo']['kskmdm']}){i['kskmz'][0]['km1Vo']['kskmmc']}"
        外语 = '、'.join(km2Vo)
        业务课一 = f"({i['kskmz'][0]['km3Vo']['kskmdm']}){i['kskmz'][0]['km3Vo']['kskmmc']}"
        业务课二 = f"({i['kskmz'][0]['km4Vo']['kskmdm']}){i['kskmz'][0]['km4Vo']['kskmmc']}"
        link = f'https://yz.chsi.com.cn/zsml/yjfxdetail?id={i["id"]}'

        # 将数据写入工作表
        sheet.append([招生单位, 考试方式, 院系所, 专业, 学习方式, 研究方向, 拟招生人数, 指导教师,
                      是否接收退役大学生士兵专项计划考生报考,
                      是否接收少数民族高层次骨干计划考生报考, 备注, 政治, 外语, 业务课一, 业务课二, link])
        print([招生单位, 考试方式, 院系所, 专业, 学习方式, 研究方向, 拟招生人数, 指导教师,
               是否接收退役大学生士兵专项计划考生报考,
               是否接收少数民族高层次骨干计划考生报考, 备注, 政治, 外语, 业务课一, 业务课二, link])

    workbook.save('data.xlsx')  # 保存到 Excel 文件

def main():
    dwdm_list = get_ids_from_progress()  # 从文件中获取所有 dwdm
    for dwdm in dwdm_list:
        page, last_zydm = get_last_progress(dwdm)  # 获取该 dwdm 的最后进度
        get_zydm(dwdm, page, last_zydm)  # 从上次进度继续采集

if __name__ == "__main__":
    main()
