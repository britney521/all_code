import pandas as pd
import jieba
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


# 1. 读取CSV文件（假设列名为'comment'）
def read_comments(csv_path):
    """读取CSV文件的第二列数据（不依赖列名）"""
    df = pd.read_csv(csv_path)
    second_column = df.iloc[:, 1]  # 通过位置索引获取第二列
    return second_column.dropna().tolist()  # 去空值并转为列表


# 2. 使用jieba分词并统计词频
def analyze_word_frequency(comments, stopwords_path=None,output_excel='word_frequency.xlsx'):
    # jieba.add_word('不好吃')
    # jieba.del_word('好吃')
    # 加载停用词（可选）
    stopwords = set()
    if stopwords_path:
        with open(stopwords_path, 'r', encoding='utf-8') as f:
            stopwords = set([line.strip() for line in f])

    # 分词并统计
    word_counts = Counter()
    for comment in comments:
        words = jieba.lcut(comment)
        filtered_words = [word for word in words if len(word) > 1 and word not in stopwords]
        word_counts.update(filtered_words)

    # 将结果转换为DataFrame
    df = pd.DataFrame(word_counts.most_common(), columns=['词语', '频次'])

    # 写入Excel文件
    df.to_excel(output_excel, index=False)

    return word_counts


# 3. 生成词云图
def generate_wordcloud(word_counts, mask_image_path=None, output_path='wordcloud.png'):
    # 准备词云数据（字典格式：{词: 频次}）
    freq_dict = dict(word_counts.most_common(200))  # 取前200个高频词

    # 设置词云参数
    if mask_image_path:
        mask = np.array(Image.open(mask_image_path))  # 使用图片形状
    else:
        mask = None

    wc = WordCloud(
        font_path='/System/Library/Fonts/Supplemental/Songti.ttc',  # 中文字体（需下载）
        background_color='white',
        relative_scaling=0,
        max_words=200,
        width=800,
        height=600,
        colormap='viridis',  # 使用更鲜艳的配色

    )

    # 生成并保存词云
    wc.generate_from_frequencies(freq_dict)
    plt.figure(figsize=(10, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()


# 主流程
if __name__ == '__main__':
    keyword = '冷吃三拼'
    # 文件路径配置
    csv_path = f'{keyword}评论.csv'  # 你的CSV文件路径
    stopwords_path = 'stopwords.txt'  # 停用词文件（可选）
    mask_image_path = 'mask.png'  # 词云形状图片（可选）

    # 执行流程
    comments = read_comments(csv_path)
    word_counts = analyze_word_frequency(comments, stopwords_path,f'{keyword}好评词频.xlsx')
    generate_wordcloud(word_counts,output_path=f'img/{keyword}.png')