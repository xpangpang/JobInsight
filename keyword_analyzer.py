from collections import Counter
import jieba

def analyze_keywords(job_titles):
    text = ' '.join(job_titles)
    words = jieba.lcut(text)
    word_counts = Counter(words)
    return word_counts.most_common(10)  # 返回前10高频词