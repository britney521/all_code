import os
import pandas as pd
import chardet

# 定义文件夹路径
folder_path = 'csv'  # 替换为你的文件夹路径

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 检查文件是否是 CSV 文件
    if filename.endswith('.csv'):
        # 构建完整的文件路径
        file_path = os.path.join(folder_path, filename)

        # 检测文件编码
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())  # 或者使用 f.read(100000) 检测前 100KB
            encoding = result['encoding']
            print(f"Detected encoding for {filename}: {encoding}")

        # 读取 CSV 文件
        try:
            df = pd.read_csv(file_path, encoding=encoding)
        except Exception as e:
            print(f"Failed to read {filename} with encoding {encoding}: {e}")
            continue

        # 输出文件名（去掉 .csv 后缀并添加 .xls 后缀）
        output_filename = filename[:-4] + '.xls'
        output_path = os.path.join(folder_path, output_filename)

        # 将数据写入到 .xls 格式的 Excel 文件
        df.to_excel(output_path, index=False)
        print(f"Processed {filename} and saved as {output_filename}")

print("All files have been processed.")