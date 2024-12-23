import random
import re
import datetime
import time


from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from DataMap.add_map import MapChina
from dbtool import DBUtils
# 定义多个 User-Agent
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/92.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.48",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36"
]

user_agent = random.choice(user_agents)
# 打开首页
index_url = 'http://www.zhaopin.com/'


edge_options = Options()
edge_options.add_argument("--start-maximized")
edge_options.add_argument(f'user-agent={user_agent}')
# 启动 Microsoft Edge 浏览器

browser = webdriver.Edge(options=edge_options)
browser.get(index_url)
wait = WebDriverWait(browser, 10)  # 等待最长15秒

# 等待直到浏览器跳转到目标 URL
# wait.until(
#     EC.url_to_be(target_url)
# )
# print("已跳转到目标 URL，继续执行程序。")
# 模拟点击 "互联网/AI" 类别，展示职位分类     //*[@id="root"]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/dl/dd[3]/div[1]/div/a
show_ele = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div[1]/div[1]/ol/li[1]/nav/a')))
show_ele.click()

# 获取今天的日期，用于标记数据抓取的日期
today = datetime.date.today().strftime('%Y-%m-%d')

# 获取职位分类
job_len_list = browser.find_elements(by=By.XPATH, value='//*[@id="root"]/main/div[1]/div[1]/ol/li[1]/nav/div/div[1]/a')
print(f"{len(job_len_list)}个分类")

# 遍历职位分类，进行职位信息抓取
for i in range(len(job_len_list)):
    time.sleep(5)
    #理论上下面的这个方法应该好一点但是容易报错
    # current_a = wait.until(
    #     EC.element_to_be_clickable((By.XPATH, f'//*[@id="root"]/main/div[1]/div[1]/ol/li[1]/nav/div/div[1]/a[{i}]'))
    # )

    current_a = browser.find_elements(By.XPATH,'//*[@id="root"]/main/div[1]/div[1]/ol/li[1]/nav/div/div[1]/a')[i]
    current_category = current_a.find_element(by=By.XPATH, value='//*[@id="root"]/main/div[1]/div[1]/ol/li[1]/nav/div/h4').text
    sub_category = current_a.text  # 子分类

    time.sleep(2)
    # 使用 ActionChains 模拟鼠标点击
    actions = ActionChains(browser)
    actions.move_to_element(current_a).click().perform()

    # 等待新窗口打开
    wait.until(lambda driver: len(driver.window_handles) > 1)
    print("{}正在抓取{}--{}".format(today, current_category, sub_category))  # 打印当前抓取的信息

    # 获取所有窗口句柄
    window_handles = browser.window_handles
    # 关闭原来窗口
    browser.close()
    browser.switch_to.window(window_handles[-1])  # 切换到最后打开的窗口
    print("页面跳转成功，当前 URL:", browser.current_url)

    # 获取当前页面中的所有职位信息（这里只是获取一次初始页面的，后续翻页会重新获取）
    job_detail = browser.find_elements(by=By.XPATH, value='/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div')
    job_page = browser.find_elements(by=By.XPATH, value='//*[@id="positionList-hook"]/div/div[2]/div[2]/div/a')
    print(f"该分类职位有{len(job_page) - 2}页")
    # 遍历所有省份
    for province in MapChina.all_province:
        #//*[@id="filter-hook"]/div/div[2]/div[1]/div[1]/img
        # 再次加载
        time.sleep(2)
        job_page = browser.find_elements(by=By.XPATH, value='//*[@id="positionList-hook"]/div/div[2]/div[2]/div/a')
        job_detail = browser.find_elements(by=By.XPATH, value='/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div')

        # 点击地点选择按钮并输入省份
        add_select_but = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="filter-hook"]/div/div[2]/div/div[1]/img'))
        )
        browser.execute_script("arguments[0].click();", add_select_but)
        # 等待地点输入框可用
        add_input_but = browser.find_element(By.XPATH, '//*[@id="filter-hook"]/div/div[2]/div[2]/div[2]/input')

        add_input_but.clear()  # 清空输入框
        add_input_but.send_keys(province)
        # 获取包含目标元素的 ul 容器
        text_element = browser.find_element(By.XPATH, '//*[@id="filter-hook"]/div/div[2]/div[2]/div[2]/ul')
        # 获取所有 li 子元素
        li_elements = text_element.find_elements(By.TAG_NAME, 'li')
        target_text=province
        # 遍历 li 元素，查找匹配的文本并点击
        time.sleep(2)
        for li in li_elements:
            if li.text.strip() == target_text:
                # 使用显式等待确保元素可点击
                wait.until(EC.element_to_be_clickable(li))
                # 滚动元素到可视区域（如果它被其他元素遮挡）
                browser.execute_script("arguments[0].scrollIntoView(true);", li)
                # 等待目标元素可点击
                wait.until(EC.element_to_be_clickable(li))
                # 模拟点击
                browser.execute_script("arguments[0].click();", li)
                break  # 找到目标文本后退出循环

        # 模拟刷新页面
        browser.refresh()
        # 选择智能匹配
        match_type_but = wait.until(
            EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div[4]/div[2]/div[1]/ul/li[1]/a'))
        )
        match_type_but.click()
        # 新增循环用于翻页操作，从第1页开始（因为初始已经在第1页获取过信息了），直到超过job_len页数
        for page in range(len(job_page) - 1):

            #固定翻页后等待时间
            time.sleep(2)

            # 获取当前页面中的所有职位信息（每次翻页后都要重新获取）
            job_detail = browser.find_elements(by=By.XPATH,
                                               value='/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div')

            print(f"正在抓取{province}第{page+1}/{len(job_page) - 2}页")
            # 遍历每个职位，提取相关信息
            for j in range(1, len(job_detail) + 1):
                db = DBUtils('localhost', 'root', '623163', 'data_analysis')
                # time.sleep(0.2)
                # 获取职位名称   ### 1. /html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div[1]/a
                try:  ##### 2.                                     /html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[2]/div[1]/div[1]/div[1]/a
                    job_title = browser.find_element(by=By.XPATH, value=
                    f'/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[{j}]/div[1]/div[1]/div[1]/a').text.strip()

                except(TimeoutException, NoSuchElementException) as e:
                    job_title = '不明'  # 如果职位标题不存在，则跳过

                try:
                    # 尝试使用第一个 XPath 查找工作地点
                    job_location = browser.find_element(By.XPATH,
                             f'/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[{j}]/div[1]/div[1]/div[3]/div[1]/span'
                    ).text.strip()
                except (TimeoutException, NoSuchElementException) as e:
                    try:
                        # 如果第一个 XPath 查找失败，则使用第二个 XPath
                        job_location = browser.find_element(By.XPATH,
                                 f'/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[{j}]/div[1]/div[1]/div[2]/div[1]/span'
                        ).text.strip()
                    except (TimeoutException, NoSuchElementException):
                        job_location = '不明'
                # f'/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[{i}]/div[1]/div[1]/div[2]/div[1]/span
                try:

                    # 获取公司名称                                         //*[@id="positionList-hook"]/div/div[1]/div[2]/div[1]/div[2]/div[1]/a
                    job_company = browser.find_element(by=By.XPATH, value=
                    f'//*[@id="positionList-hook"]/div/div[1]/div[{j}]/div[1]/div[2]/div[1]/a').text.strip()
                except(TimeoutException, NoSuchElementException) as e:
                    job_company = '不明'
                ### 行业类型                                # /html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[2]/div[1]/div[2]/div[1]/a
                try:
                    # 尝试使用第一个 XPath 查找工作地点
                    job_industry = browser.find_element(By.XPATH,
                             f'/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[{j}]/div[1]/div[2]/div[2]/div[3]'
                    ).text.strip()
                except (TimeoutException, NoSuchElementException) as e:
                    try:
                        # 如果第一个 XPath 查找失败，则使用第二个 XPath
                        job_industry = browser.find_element(By.XPATH,
                                 f'/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[{j}]/div[1]/div[2]/div[2]/div[2]'
                        ).text.strip()
                    except (TimeoutException, NoSuchElementException) as e:
                        job_industry = '不明'

                try:  # //*[@id="positionList-hook"]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]
                    # 获取公司类型  //*[@id="positionList-hook"]/div/div[1]/div[{j}]/div[1]/div[2]/div[2]/div[1]
                    data_type = browser.find_element(by=By.XPATH, value=
                    f'//*[@id="positionList-hook"]/div/div[1]/div[{j}]/div[1]/div[2]/div[2]/div[1]').text.strip()
                    #如果得到的结果中有数字直接填充不明
                    if re.search(r'\d', data_type):
                        job_type = "不明"
                    else:
                        job_type = data_type
                except(TimeoutException, NoSuchElementException) as e:
                    job_type = '不明'


                # 获取公司规模（若无则标记为“无”）    //*[@id="positionList-hook"]/div/div[1]/div[5]/div[1]/div[2]/div[2]/div[2]
                try:
                    # 尝试使用第一个 XPath 提取数据
                    scale_data = browser.find_element(by=By.XPATH, value=
                    f'//*[@id="positionList-hook"]/div/div[1]/div[{j}]/div[1]/div[2]/div[2]/div[2]').text.strip()

                    # 如果第一个 XPath 获取到的数据中没有数字，就尝试第二个 XPath
                    if not re.search(r'\d', scale_data):
                        try:
                            # 如果第一个 XPath 获取的数据中没有数字，则使用第二个 XPath
                            job_scale = browser.find_element(By.XPATH,
                                     f'//*[@id="positionList-hook"]/div/div[1]/div[{j}]/div[1]/div[2]/div[2]/div[1]'
                            ).text.strip()
                        except (TimeoutException, NoSuchElementException) as e:
                            job_scale = '不明'  # 如果第二个 XPath 也无法获取，返回'不明'
                    else:
                        job_scale = scale_data  # 如果第一个 XPath 提取的数据包含数字，使用该数据

                except (TimeoutException, NoSuchElementException) as e:
                    # 如果第一个 XPath 查找失败，则返回'不明'
                    job_scale = '不明'



                try:
                    # 获取薪资范围      //*[@id="positionList-hook"]/div/div[1]/div[2]/div[1]/div[1]/div[1]/p
                    job_salary_range = browser.find_element(by=By.XPATH, value=
                    f'//*[@id="positionList-hook"]/div/div[1]/div[{j}]/div[1]/div[1]/div[1]/p').text.strip()
                except(TimeoutException, NoSuchElementException) as e:
                    job_salary_range = '不明'



                # 获取工作年限要求
                try:
                    # 尝试使用第一个 XPath 查找工作地点
                    job_experience = browser.find_element(By.XPATH,
                             f'//*[@id="positionList-hook"]/div/div[1]/div[{j}]/div[1]/div[1]/div[3]/div[2]'
                    ).text.strip()
                except (TimeoutException, NoSuchElementException) as e:
                    try:
                        # 如果第一个 XPath 查找失败，则使用第二个 XPath
                        job_experience = browser.find_element(By.XPATH,
                                 f'//*[@id="positionList-hook"]/div/div[1]/div[{j}]/div[1]/div[1]/div[2]/div[2]'
                        ).text.strip()
                    except (TimeoutException, NoSuchElementException) as e:
                        job_experience = '经验不限'


                # 获取学历要求
                try:
                    # 尝试使用第一个 XPath 查找工作地点
                    job_education = browser.find_element(By.XPATH,
                             f'/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[{j}]/div[1]/div[1]/div[3]/div[3]'
                    ).text.strip()
                except (TimeoutException, NoSuchElementException) as e:
                    try:
                        # 如果第一个 XPath 查找失败，则使用第二个 XPath
                        job_education = browser.find_element(By.XPATH,
                                 f'/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[{j}]/div[1]/div[1]/div[2]/div[3]'
                        ).text.strip()
                    except (TimeoutException, NoSuchElementException) as e:
                        job_education = '不限'

                # 获取技能要求（若无则标记为“无”）                                                                     /html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]
                try:
                    data_skills = ','.join([skill.text.strip() for skill in browser.find_elements(by=By.XPATH,
                     value=f'/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[{j}]/div[1]/div[1]/div[2]/div')])
                    # 匹配技能要求如果没有英文
                    if not re.search(r'[a-zA-Z]', data_skills):
                        job_skills = '无'
                    else:
                        job_skills = data_skills
                except(TimeoutException, NoSuchElementException) as e:
                    job_skills = '无'


                # 确定职位所在的省份
                province = ''
                city = job_location.split('·')[0]  # 提取城市名（从工作地点字符串中分离）
                province = MapChina.get_province_by_city(city)

                # 打印抓取的职位信息
                print(f"{j}/{len(job_detail)}", current_category, sub_category, job_title, province, job_location,
                      job_company, job_industry,
                      job_type,
                      job_scale, job_salary_range, job_experience, job_education, job_skills)

                # 将抓取的数据保存到MySQL数据库
                db.insert_data(
                    "insert into job_info(category, sub_category,job_title,province,job_location,job_company,job_industry,job_type,job_scale,job_salary_range,job_experience,job_education,job_skills,create_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    args=(
                        current_category, sub_category, job_title, province, job_location, job_company, job_industry,
                        job_type,
                        job_scale, job_salary_range, job_experience, job_education, job_skills, today))

                # 关闭数据库连接
                db.close()

            # 判断是否是最后一页，如果不是则点击下一页按钮
            if page < (len(job_page) - 2):
                try:
                    next_page_button = wait.until(
                        EC.presence_of_element_located((By.LINK_TEXT, '下一页'))
                    )

                    if 'soupager__btn--disable' not in next_page_button.get_attribute('class'):
                        # 滚动到页面的“下一页”按钮处
                        browser.execute_script("arguments[0].scrollIntoView();", next_page_button)

                        # 点击“下一页”按钮
                        browser.execute_script("arguments[0].click();", next_page_button)
                        time.sleep(2)
                        # 点击清除按钮，若有的话
                        clear_but = wait.until(
                            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/button')))
                        browser.execute_script("arguments[0].click();", clear_but)
                        print("跳转页码成功，当前 URL:", browser.current_url)
                        time.sleep(2)
                    else:
                        print("已经是最后一页")
                        break

                except (TimeoutException, NoSuchElementException) as e:
                    print("已经是最后一页")
                    continue  # 如果超时，则结束翻页循环
    # 返回到首页进行下一个分类抓取
    try:

        # 退回到首页
        browser.back()
        # 模拟点击 互联网/AI 展示出岗位分类
        show_ele = browser.find_element(by=By.XPATH, value='//*[@id="root"]/main/div[1]/div[1]/ol/li[1]/nav/a')
        show_ele.click()
    except(TimeoutException, NoSuchElementException) as e:

        browser.get(index_url)  # 如果出错，重新打开首页
        show_ele = browser.find_element(by=By.XPATH, value='//*[@id="root"]/main/div[1]/div[1]/ol/li[1]/nav/a')
        show_ele.click()  # 重新点击“互联网/AI”类别

# 关闭浏览器
browser.quit()

