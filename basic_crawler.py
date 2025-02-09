from selenium import webdriver
from selenium.webdriver import Edge
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def fetch_jobs(keyword, city):
    # 设置Edge选项
    edge_options = Options()
    # edge_options.add_argument("--headless")  # 无头模式，不打开浏览器窗口
    edge_options.add_argument("--no-sandbox")  # 禁用沙盒模式
    edge_options.add_argument("--disable-dev-shm-usage")  # 避免内存不足问题

    # 避免人机验证，需要避免传入自动化测试控制的标识
    # 正常情况下在浏览器控制台输window.navigator.webdriver会返回false，而通过selenium来操作浏览器的情况下会返回true。
    edge_options.use_chromium = True# 使用chromium内核，打开开发者模式
    edge_options.add_argument('--disable-blink-features=AutomationControlled')# 添加参数

    # 使用本地的WebDriver文件
    edge_driver_path = r"C:\2025\edgedriver_win64\msedgedriver.exe"
    service = Service(edge_driver_path)
    driver = webdriver.Edge(service=service, options=edge_options)# 将参数配置到driver对象

    # 构造URL并访问
    url = f"https://www.zhipin.com/web/geek/job?query={keyword}&city={city}"
    driver.get(url)

    # 等待页面加载完成
    wait = WebDriverWait(driver, 100)
    job_elements = wait.until(EC.presence_of_all_elements_located(# 确保元素已经被加载到页面上，但不一定需要与元素进行交互
        (By.CSS_SELECTOR, "div.job-card-body.clearfix")
    ))

    # 提取岗位名称
    jobs =[]
    for element in job_elements:
        job_name = element.find_element(By.CSS_SELECTOR, "span.job-name").text
        job_area = element.find_element(By.CSS_SELECTOR, "span.job-area").text
        job_detail_link = element.find_element(By.CSS_SELECTOR, "a.job-card-left").get_attribute('href')
        job_detail = fetch_job_details(job_detail_link, driver)
        print(f"职位名称: {job_name}, 工作地点: {job_area}，详细信息：{job_detail}")
        job = {
            "name": job_name,
            "area": job_area,
            "detail": job_detail
        }
        jobs.append(job)

    # 关闭浏览器
    driver.quit()

    return jobs

def fetch_job_details(job_detail_link, driver):
    driver.execute_script("window.open('');")  # 打开新窗口
    driver.switch_to.window(driver.window_handles[-1])  # 切换到新窗口
    driver.get(job_detail_link)
    try:
        job_description = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.job-sec-text"))
        ).text

    except Exception as e:
        print(f"Error fetching job details: {e}")
        job_description = "无法获取详情信息"
    finally:
        # 关闭当前（详情）页面，返回到前一个页面
        driver.close()
        driver.switch_to.window(driver.window_handles[0])  # 切换回原始窗口

    return job_description


if __name__ == "__main__":
    keyword = "自动化测试"
    city = "101210100"  # 杭州的城市代码
    jobs = fetch_jobs(keyword, city)
    print(f"找到 {len(jobs)} 个岗位:")
    for job in jobs:
        print(job)