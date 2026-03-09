import pandas as pd

# 加载CSV文件
df = pd.read_csv('河南.csv')  # 替换为你的CSV文件名

# 按照指定的列去重
df_unique = df.drop_duplicates(subset=['药品名', '药店名称', '药店价格'])

# 保存去重后的文件
df_unique.to_csv('黑龙江鸡西.csv', index=False)  # 替换为你想要保存的文