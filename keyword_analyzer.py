from collections import Counter
import jieba

with open('哈工大停用词表.txt', encoding='utf-8') as f: # 可根据需要打开停用词库，然后加上不想显示的词语
    con = f.readlines()
    stop_words = set() # 集合可以去重
    for i in con:
        i = i.replace("\n", "")   # 去掉读取每一行数据的\n
        stop_words.add(i)

def analyze_keywords(jobs):
    text = ''
    for job in jobs:
        text += job['detail'] +''  # 合并所有职位详细内容
    result = []
    for word in jieba.lcut(text):# 分词
        if word not in stop_words:# 去除停用词
            result.append(word)
    word_counts = Counter(result)
    return word_counts.most_common(10)  # 返回前10高频词