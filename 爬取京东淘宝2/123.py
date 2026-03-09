import re
from collections import Counter
import jieba  # 中文分词库（若评论为英文，可用nltk/spacy代替）

# 假设评论列表（实际可从文件/数据库读取）
comments = [
    "手机外观非常漂亮，时尚的设计，颜色很炫酷",
    "外壳材质一般，但造型很独特，手感光滑",
    "屏幕超大，边框极窄，整体看起来很精致",
    "做工粗糙，颜色和宣传图差别大，不够时尚"
]

# 1. 中文分词和词性标注（需提前安装jieba和jieba.posseg）
import jieba.posseg as pseg

adjectives = []
for comment in comments:
    words = pseg.cut(comment)
    for word, flag in words:
        if flag == 'a':  # 'a'表示形容词
            adjectives.append(word)

# 英文替代方案（使用nltk）：
# from nltk import pos_tag, word_tokenize
# adjectives = []
# for comment in comments:
#     tokens = word_tokenize(comment)
#     tagged = pos_tag(tokens)
#     adjectives += [word for word, pos in tagged if pos.startswith('JJ')]

# 2. 词频统计
adjective_counts = Counter(adjectives)

# 3. 按频率排序输出
print("形容词词频排序结果：")
for adj, count in adjective_counts.most_common():
    print(f"{adj}: {count}次")