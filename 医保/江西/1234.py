# 1. 导入pandas库
import pandas as pd

# 2. 读取CSV文件（替换为你的CSV文件路径，如 "./medicine_data.csv"）
df = pd.read_csv("drug_list.csv")

# 3. 按指定三列去重，保留每组重复数据的第一条（核心步骤）
# subset：指定用于判断重复的列（药品名、药店地址、药品价格，需与你的CSV列名完全一致）
# keep：保留策略，"first" 保留第一条，"last" 保留最后一条
# inplace：False 表示返回新的去重后DataFrame，True 表示直接在原DataFrame上修改
df_deduplicated = df.drop_duplicates(
    subset=["药品名", "药店地址", "药店价格"],
    keep="first",
    inplace=False
)

# 4. （可选）将去重结果保存为新CSV文件（避免覆盖原数据）
df_deduplicated.to_csv("南昌药品_0127.csv", index=False, encoding="utf-8-sig")

# （可选）打印去重结果概览
print(f"原数据行数：{len(df)}")
print(f"去重后数据行数：{len(df_deduplicated)}")
print("去重完成，结果已保存为 medicine_data_deduplicated.csv")