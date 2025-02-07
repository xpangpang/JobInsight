import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def fetch_job_titles(keyword, city):
    url = f"https://www.zhipin.com/web/geek/job?query={keyword}&city={city}"
    headers = {'User-Agent': UserAgent().random}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取岗位名称（需根据实际网站结构调整选择器）
    jobs = soup.select('.job-title')
    return [job.text.strip() for job in jobs]