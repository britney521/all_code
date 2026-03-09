import os
import re
import pandas as pd
from paddleocr import PaddleOCR
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# 1. 初始化 OCR (仅在这里初始化，避免主程序崩溃)
print("正在初始化 OCR 模型...")
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

# 2. 读取第一步生成的 Excel
input_excel = '【用法用量】提取完成.xlsx'  # 确保文件名一致
df = pd.read_excel(input_excel)

print(f"开始补全 OCR 数据，总行数: {len(df)}")


# 定义提取函数 (针对本地文件)
def extract_from_local_image(image_path):
    try:
        # PaddleOCR 直接读取本地路径，比传二进制更稳定
        result = ocr.predict(image_path)

        if not result or not result[0]:
            return None

        # 拼接文本
        rec_texts = result[0]['rec_texts']  # list[str]
        all_txt = " ".join(rec_texts)

        # 正则提取
        pattern = r"(?:【|^)\s*(?:用法用量|用法与用量)(?:】|[:：])?\s*(.*?)(?=\n?\s*(?:【|\[|不良反应|禁忌|注意事项|规格|贮藏|有效期|批准文号)|$)"
        match = re.search(pattern, all_txt, re.DOTALL | re.IGNORECASE)

        if match:
            return match.group(1).strip()
        else:
            return f"OCR识别成功但未匹配正则\n(全文前50字): {all_txt[:50]}..."

    except Exception as e:
        return f"OCR 运行出错: {e}"


# 3. 遍历并补全
count = 0
for index, row in df.iterrows():
    # 只处理标记为 '代读取图片' 的行
    if str(row['用法用量']).strip() == '代读取图片':

        # 构造对应的图片路径 (必须与第一步保存的规则一致)
        img_path = f"img/temp_{index + 1}.png"

        print(f"[{index + 1}] 正在识别本地图片: {img_path}")

        if os.path.exists(img_path):
            # 执行识别
            res = extract_from_local_image(img_path)

            if res:
                df.at[index, '用法用量'] = res
                print(f"   -> 识别结果: {str(res)[:30]}...")
            else:
                df.at[index, '用法用量'] = "OCR未识别到文字"
                print("   -> 未识别到文字")
        else:
            df.at[index, '用法用量'] = "图片文件丢失"
            print(f"   -> 错误: 找不到文件 {img_path}")

        count += 1

        # 每处理 10 张保存一次，防止 OCR 再次崩溃白跑
        if count % 10 == 0:
            df.to_excel('【用法用量】补全中_temp.xlsx', index=False)
            print("   --- 临时保存 ---")

# 4. 最终保存
final_output = '【用法用量】最终完整版.xlsx'
df.to_excel(final_output, index=False)
print(f"\n补全完成！共处理 {count} 张图片，结果已保存至 {final_output}")