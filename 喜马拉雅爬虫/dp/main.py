# -*- coding: utf-8 -*-
"""
极验 4 滑块验证码自动识别（多线程版）
在原脚本基础上统一加 logger 与中文注释，方便并发调试。
"""
import os
import re
import time
from loguru import logger
import requests
import cv2
import numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

from DrissionPage import Chromium, ChromiumOptions

# ========================== 日志配置 ==========================
from loguru import logger
import sys
# 控制台输出 + 线程名 + 颜色


# ========================== 浏览器初始化 ==========================
op = ChromiumOptions().set_paths('/Applications/GPT Chrome.app/Contents/MacOS/GptBrowser')
browser = Chromium(op)
logger.info("浏览器对象创建完成")

# ========================== 功能函数 ==========================
def get_imgs(page):
    """
    下载背景图与滑块图，保存到本地 ./img/ 目录
    返回 (bg_path, slider_path)
    """
    logger.debug("开始提取背景图 URL")
    bg = page.ele('css:.geetest_bg')
    style = bg.attr('style') or ''
    url_match = re.search(r'background-image:\s*url\(["\']?(.*?)["\']?\)', style)
    if not url_match:
        logger.error("未找到背景图 URL，style={}", style)
        raise ValueError('未找到背景图 URL')
    url = url_match.group(1).replace('&quot;', '')
    logger.info("背景图 URL: {}".format(url))

    # 下载背景图
    os.makedirs('img', exist_ok=True)
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    bg_path = 'img/bg.png'
    with open(bg_path, 'wb') as f:
        f.write(r.content)
    logger.info("背景图已保存 -> {}", bg_path)

    # 下载滑块图
    logger.debug("开始提取滑块图 URL")
    s_style = page.ele('css:.geetest_slice_bg').attr('style') or ''
    s_url_match = re.search(r'background-image:\s*url\(["\']?(.*?)["\']?\)', s_style)
    slider_path = None
    if s_url_match:
        s_url = s_url_match.group(1).replace('&quot;', '')
        logger.info("滑块图 URL: {}", s_url)
        r = requests.get(s_url, timeout=10)
        slider_path = 'img/slider.png'
        with open(slider_path, 'wb') as f:
            f.write(r.content)
        logger.info("滑块图已保存 -> {}", slider_path)
    else:
        logger.warning("未找到滑块图 URL")

    return bg_path, slider_path


def calculate_gap_position(bg_path, slice_path):
    """
    用 OpenCV 模板匹配计算滑块缺口距离
    返回缺口 x 坐标（像素）
    """
    logger.debug("开始计算缺口位置 | bg={} | slice={}", bg_path, slice_path)
    bg = cv2.cvtColor(np.array(Image.open(bg_path).convert('RGB')), cv2.COLOR_RGB2GRAY)
    tp = cv2.cvtColor(np.array(Image.open(slice_path).convert('RGB')), cv2.COLOR_RGB2GRAY)
    tp = 255 - tp  # 反色，让滑块区域更突出
    res = cv2.matchTemplate(bg, tp, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    logger.info("模板匹配最大值=%.3f，缺口坐标={}", max_val, max_loc)
    return max_loc[0] if max_val > 0.3 else None

def get_getTracksList(data_packet):

    res = data_packet.response.body
    datas = res['data']['tracks']
    return datas


def crack_one(tab_id: int):
    """
    单个线程的破解逻辑
    tab_id: 仅用于日志区分不同线程/标签页
    """
    logger.info("====== 线程 [{}] 启动 ======", tab_id)
    tab = browser.new_tab()
    try:

        logger.info("打开 https://www.ximalaya.com/album/{}".format(tab_id))
        tab.listen.start('album/v1/getTracksList')
        tab.get('https://www.ximalaya.com/album/{}'.format(tab_id))
        tab.wait.doc_loaded()

        # 4. 循环拖动直到成功
        while tab.ele('css:.geetest_bg',timeout=2):
            logger.info("[{}] 开始新一轮滑块验证", tab_id)

            # 4-1 下载图片
            bg_path, slider_path = get_imgs(tab)

            # 4-2 计算缺口
            distance = calculate_gap_position(bg_path, slider_path)
            if distance is None:
                logger.error("[{}] 缺口识别失败，跳过本轮", tab_id)
                break
            tab.wait(1)
            # 4-3 拖动滑块
            tab.wait.ele_displayed('css:.geetest_btn')
            ele = tab('css:.geetest_btn')
            tab.actions.move_to(ele_or_loc=ele)
            tab.actions.hold(ele)
            logger.debug("[{}] 按住滑块，准备移动 %.1f px", tab_id, distance)
            tab.actions.move(distance, 0)
            tab.actions.release(ele)
            logger.debug("[{}] 滑块释放", tab_id)

            tab.wait(2)
            # 4-4 等待验证结果
            tab.wait.doc_loaded()

            tab.refresh()
            tab.wait.doc_loaded()
            tab.wait(1)

            if not tab.ele('css:.geetest_bg'):
                logger.success("[{}] ====== 验证通过！======", tab_id)
                break
            else:
                logger.warning("[{}] 验证未通过，继续重试", tab_id)
        data_packets = tab.listen.wait()
        tacks = get_getTracksList(data_packets)
        return tacks
    except Exception as e:
        logger.exception("[{}] 线程异常: {}", tab_id, e)
    finally:
        logger.info("[{}] 线程结束，关闭标签页", tab_id)
        tab.close()


# ========================== 多线程入口 ==========================
if __name__ == "__main__":
    # 这里示范并发 3 个标签页，可自行调整
    crack_one(1)
    # browser.quit()