from basic_crawler import fetch_jobs
from keyword_analyzer import analyze_keywords
def main():
    search_keyword = input("请输入搜索关键词（如：101210100 Python）: ")
    city, keyword = search_keyword.split()  # 简单分割输入

    # 调用爬虫功能
    print(f"\n正在爬取{city}地区的{keyword}岗位...")
    job_titles = fetch_jobs(keyword, city)

    # 调用热词分析功能
    hot_words = analyze_keywords(job_titles)
    print("\n热门技能需求：")
    for word, count in hot_words:
        print(f"{word}: {count}次")

import csv

def save_to_csv(jobs, filename='data/jobs.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['职位名称'])
        for job in jobs:
            writer.writerow([job])