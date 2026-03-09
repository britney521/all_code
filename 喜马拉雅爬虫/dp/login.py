import base64
import io
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
from matplotlib import pyplot as plt


def check_login():
    login_btn = tab.ele('css:.login-btn')
    return login_btn

op = ChromiumOptions().set_paths('/Applications/GPT Chrome.app/Contents/MacOS/GptBrowser')
browser = Chromium(op)
logger.info("浏览器对象创建完成")

tab = browser.new_tab()
tab.get('https://www.ximalaya.com/')

login_btn = check_login()
if login_btn:
    logger.info(f'检测需要登入')
    login_btn.click()
    tab.wait(2)
    scran_img = tab.ele('css:.qrcode-login__qrcode')
    s_style = scran_img.attr('style') or ''

    m = re.search(r'background-image:\s*url\(["\']?(.*?)["\']?\)', s_style)
    if m:
        data_uri = m.group(1)               # 整段 data:image/...;base64,xxxxx
        logger.info(f'获取图片二维码')
        header, b64 = data_uri.split(',', 1)  # 只要逗号后面的纯 base64
        img_bytes = base64.b64decode(b64)

        img = Image.open(io.BytesIO(img_bytes))
        plt.imshow(img)
        plt.axis('off')
        plt.show()
        while check_login():
            tab.wait(5)
            logger.info(f'请扫码登入')