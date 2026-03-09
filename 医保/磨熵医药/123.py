from paddleocr import PaddleOCR
import re
import os

# 1. 初始化 (去掉了不支持的 show_log 参数)
ocr = PaddleOCR(lang='ch')

# 2. 图片路径
img_path = "img/temp_234.png"

# 检查文件是否存在
if not os.path.exists(img_path):
    print("图片文件不存在")
else:
    # 3. 进行识别
    # standard paddleocr uses .ocr() method
    result = ocr.predict(img_path)

    # 4. 提取并拼接所有文本
    # PaddleOCR 返回结构: [ [ [[坐标], [文本, 置信度]], ... ] ]
    # 打印识别结果
    for line in result:
        print(line)

    print("--- 全文概览 (前100字) ---")


    # # 5. 使用正则表达式提取【用法用量】
    # # 逻辑：寻找 "用法用量" 开头，直到遇到 "不良反应"、"禁忌" 等关键词结束
    # # (?s) 开启 dotall 模式，让 . 可以匹配换行符
    pattern = r"(用法用量|用法与用量)[:：]?\s*(.*?)(?=\n\s*(不良反应|禁忌|注意事项|规格|贮藏|有效期)|$)"

    match = re.search(pattern, all_txt, re.DOTALL)

    if match:
        # group(2) 是我们需要的内容部分
        target_content = match.group(2).strip()
        print("--- 提取到的【用法用量】 ---")
        print(target_content)
    else:
        print("未在文中匹配到“用法用量”字段。")
