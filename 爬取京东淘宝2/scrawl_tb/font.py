import matplotlib.font_manager as fm
import pandas as pd


def find_chinese_fonts():
    """返回系统所有支持中文的字体路径"""
    chinese_fonts = []
    for font in fm.fontManager.ttflist:
        # 检查字体名是否包含常见中文字体标识
        if any(keyword in font.name.lower() for keyword in
               ['sim', 'hei', 'kai', 'fang', 'song', 'stkaiti', 'msyh', 'pingfang']):
            chinese_fonts.append((font.name, font.fname))
    return chinese_fonts

# 使用示例
# fonts = find_chinese_fonts()
# for name, path in fonts:
#     print(f"字体名称: {name}\n路径: {path}\n")
# 1. 读取CSV文件（假设列名为'comment'）
def read_comments(csv_path):
    """读取CSV文件的第二列数据（不依赖列名）"""
    df = pd.read_csv(csv_path)
    second_column = df.iloc[:, 0]  # 通过位置索引获取第二列
    return second_column.dropna().unique().tolist()  # 去空值并转为列表

csv_path = f'csv/冷吃三拼评论.csv'
print(read_comments(csv_path))