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
# # 定义多个 User-Agent
# user_agents = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/92.0",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.48",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36"
# ]
#
# user_agent = random.choice(user_agents)
# 打开首页
index_url = 'http://www.zhaopin.com/'
#登录成功后的url
target_url = 'https://xiaoyuan.zhaopin.com/?login_source=c'

edge_options = Options()
edge_options.add_argument("--start-maximized")
# edge_options.add_argument(f'user-agent={user_agent}')
# 启动 Microsoft Edge 浏览器

browser = webdriver.Edge(options=edge_options)
browser.get(index_url)
wait = WebDriverWait(browser, 25)  # 等待最长15秒

# 等待直到浏览器跳转到目标 URL
wait.until(
    EC.url_to_be(target_url)
)
print("已跳转到目标 URL，继续执行程序。")
show_job = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[1]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/span')))
show_job.click()

show_ele = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/dl/dd[3]/div[1]/div/a')))
show_ele.click()
# 获取今天的日期，用于标记数据抓取的日期
today = datetime.date.today().strftime('%Y-%m-%d')

# 获取职位分类   #登录后   //*[@id="root"]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/dl/dd[3]/div[2]/div/ul/li[1]/div/a[1]
job_len_list = browser.find_elements(by=By.XPATH, value=f'//*[@id="root"]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/dl/dd[3]/div[2]/div/ul/li[1]/div/a')
print(f"{len(job_len_list)}个分类")
# 遍历职位分类，进行职位信息抓取
for i in range(1,len(job_len_list)):

    current_a = wait.until(
        EC.element_to_be_clickable((By.XPATH, f'//*[@id="root"]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/dl/dd[3]/div[2]/div/ul/li[1]/div/a[{i}]'))
    )
    current_category = current_a.find_element(by=By.XPATH, value='//*[@id="root"]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/dl/dd[3]/div[2]/div/ul/li[1]/h4').text
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
    browser.switch_to.window(window_handles[-1])  # 切换到最后打开的窗口
    print("页面跳转成功，当前 URL:", browser.current_url)

    # 获取当前页面中的所有职位信息（这里只是获取一次初始页面的，后续翻页会重新获取） //*[@id="root"]/div/div[5]/div[1]/div/div[2]
    #每一页的职位数量
    job_num = browser.find_elements(by=By.XPATH, value='//*[@id="root"]/div/div[5]/div[1]/div/div')
    job_page = browser.find_elements(by=By.XPATH, value='//*[@id="root"]/div/div[6]/div[1]/div/div[21]/div/div')
    job_len = len(job_page) - 2
    print(f"该分类职位有{job_len}页")
    # 遍历所有省份
    while True:
        time.sleep(1)
        # 点击地点选择按钮并输入省份
        add_select_but = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div[2]/div[1]/div[2]/div[1]'))
        )
        # 新增循环用于翻页操作，从第1页开始（因为初始已经在第1页获取过信息了），直到超过job_len页数
        for page in range(1, job_len + 1):


            # 获取当前页面中的所有职位信息（每次翻页后都要重新获取）
            job_detail = browser.find_elements(by=By.XPATH,
                                               value='/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div')

            print(f"正在抓取{province}第{page}/{job_len}页")
            # 遍历每个职位，提取相关信息
            for j in range(1, len(job_detail) + 1):
                db = DBUtils('localhost', 'root', '623163', 'data_analysis')
                time.sleep(0.4)
                # 获取职位名称   ### 1.   //*[@id="root"]/div/div[5]/div[1]/div/div[1]/div/div[1]/div[1]/div[1]
                try:  ##### 2.          //*[@id="root"]/div/div[5]/div[1]/div/div[{j}]/div/div[1]/div[1]/div[1]
                    job_title = browser.find_element(by=By.XPATH, value=
                    f'//*[@id="root"]/div/div[5]/div[1]/div/div[{j}]/div/div[1]/div[1]/div[1]').text.strip()

                except(TimeoutException, NoSuchElementException) as e:
                    job_title = '不明'  # 如果职位标题不存在，则跳过

                try:
                    # 尝试使用第一个 XPath 查找工作地点    //*[@id="root"]/div/div[5]/div[1]/div/div[1]/div/div[1]/div[1]/div[2]
                    #                               //*[@id="root"]/div/div[5]/div[1]/div/div[{j}]/div/div[1]/div[1]/div[2]
                    job_location_data = browser.find_element(By.XPATH,
                             f'//*[@id="root"]/div/div[5]/div[1]/div/div[{j}]/div/div[1]/div[1]/div[2]'
                    ).text.strip()
                    job_location = re.sub(r"[^\w\u4e00-\u9fa5]", "", job_location_data )
                except (TimeoutException, NoSuchElementException) as e:
                    try:
                        # 如果第一个 XPath 查找失败，则使用第二个 XPath
                        job_location = browser.find_element(By.XPATH,
                                 f'/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[{j}]/div[1]/div[1]/div[2]/div[1]/span'
                        ).text.strip()
                    except (TimeoutException, NoSuchElementException):
                        job_location = '不明'

                # 获取公司名称
                try:

                    #                                       //*[@id="root"]/div/div[5]/div[1]/div/div[1]/div/div[2]/div[1]/div[2]
                    #                                                    //*[@id="root"]/div/div[5]/div[1]/div/div[{j}]/div/div[2]/div[1]/div[2]
                    job_company = browser.find_element(by=By.XPATH, value=
                    f'//*[@id="root"]/div/div[5]/div[1]/div/div[{j}]/div/div[2]/div[1]/div[2]').text.strip()
                except(TimeoutException, NoSuchElementException) as e:
                    job_company = '不明'


                ### 行业类型                              //*[@id="root"]/div/div[5]/div[1]/div/div[1]/div/div[2]/div[1]/div[3]/div[1]
                try:
                    # 尝试使用第一个 XPath 查找工作地点      //*[@id="root"]/div/div[5]/div[1]/div/div[{j}]/div/div[2]/div[1]/div[3]/div[1]
                    job_industry = browser.find_element(By.XPATH,
                             f'//*[@id="root"]/div/div[5]/div[1]/div/div[{j}]/div/div[2]/div[1]/div[3]/div[1]'
                    ).text.strip()
                except (TimeoutException, NoSuchElementException) as e:
                    try:
                        # 如果第一个 XPath 查找失败，则使用第二个 XPath
                        job_industry = browser.find_element(By.XPATH,
                                 f'/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[{j}]/div[1]/div[2]/div[2]/div[2]'
                        ).text.strip()
                    except (TimeoutException, NoSuchElementException) as e:
                        job_industry = '不明'

                try:  #          //*[@id="root"]/div/div[5]/div[1]/div/div[1]/div/div[2]/div[1]/div[3]/div[3]
                    # 获取公司类型  //*[@id="root"]/div/div[5]/div[1]/div/div[{j}]/div/div[2]/div[1]/div[3]/div[3]
                    data_type = browser.find_element(by=By.XPATH, value=
                    f'//*[@id="root"]/div/div[5]/div[1]/div/div[{j}]/div/div[2]/div[1]/div[3]/div[3]').text.strip()
                    #如果得到的结果中有数字直接填充不明
                    if re.search(r'\d', data_type):
                        job_type = "不明"
                    else:
                        job_type = data_type
                except(TimeoutException, NoSuchElementException) as e:
                    job_type = '不明'


                # 获取公司规模（若无则标记为“无”）   //*[@id="root"]/div/div[5]/div[1]/div/div[1]/div/div[2]/div[1]/div[3]/div[2]
                try:
                    # 尝试使用第一个 XPath 提取数据   //*[@id="root"]/div/div[5]/div[1]/div/div[{j}]/div/div[2]/div[1]/div[3]/div[2]
                    scale_data = browser.find_element(by=By.XPATH, value=
                    f'//*[@id="root"]/div/div[5]/div[1]/div/div[{j}]/div/div[2]/div[1]/div[3]/div[2]').text.strip()

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



                try:  #                 //*[@id="root"]/div/div[5]/div[1]/div/div[1]/div/div[1]/div[2]
                    # 获取薪资范围      //*[@id="root"]/div/div[5]/div[1]/div/div[{j}]/div/div[1]/div[2]
                    job_salary_range = browser.find_element(by=By.XPATH, value=
                    f'//*[@id="root"]/div/div[5]/div[1]/div/div[{j}]/div/div[1]/div[2]').text.strip()
                except(TimeoutException, NoSuchElementException) as e:
                    job_salary_range = '不明'



                # 获取工作年限要求                      c//*[@id="root"]/div/div[5]/div[1]/div/div[2]/div/ul/li[3]
                try:
                    # 尝试使用第一个 XPath 查找工作地点   //*[@id="root"]/div/div[5]/div[1]/div/div[{j}]/div/ul/li[3]
                    job_experience = browser.find_element(By.XPATH,
                             f'//*[@id="root"]/div/div[5]/div[1]/div/div[{j}]/div/ul/li[3]'
                    ).text.strip()
                except (TimeoutException, NoSuchElementException) as e:
                    try:
                        # 如果第一个 XPath 查找失败，则使用第二个 XPath
                        job_experience = browser.find_element(By.XPATH,
                                 f'//*[@id="positionList-hook"]/div/div[1]/div[{j}]/div[1]/div[1]/div[2]/div[2]'
                        ).text.strip()
                    except (TimeoutException, NoSuchElementException) as e:
                        job_experience = '经验不限'


                # 获取学历要求    //*[@id="root"]/div/div[5]/div[1]/div/div[1]/div/ul/li[2]
                try:
                    # 尝试使用第一个 XPath 查找工作地点  //*[@id="root"]/div/div[5]/div[1]/div/div[{j}]/div/ul/li[2]
                    job_education = browser.find_element(By.XPATH,
                             f'//*[@id="root"]/div/div[5]/div[1]/div/div[{j}]/div/ul/li[2]'
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
                    if not re.search(r'[a-zA-Z]', data_skills):
                        job_skills = '无'
                    else:
                        job_skills = data_skills
                except(TimeoutException, NoSuchElementException) as e:
                    job_skills = '无'


                # 确定职位所在的省份
                province = ''
                city = job_location.split('·')[0]  # 提取城市名（从工作地点字符串中分离）
                for p, cities in MapChina.city_map.items():  # 遍历城市映射，查找匹配的省份
                    if city in cities:
                        province = p
                        break

                # 打印抓取的职位信息
                print(f"{j}/{len(job_detail)}", current_category, sub_category, job_title, province, job_location,
                      job_company, job_industry,
                      job_type,
                      job_scale, job_salary_range, job_experience, job_education, job_skills)

                # # 将抓取的数据保存到MySQL数据库
                # db.insert_data(
                #     "insert into job_info(category, sub_category,job_title,province,job_location,job_company,job_industry,job_type,job_scale,job_salary_range,job_experience,job_education,job_skills,create_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                #     args=(
                #         current_category, sub_category, job_title, province, job_location, job_company, job_industry,
                #         job_type,
                #         job_scale, job_salary_range, job_experience, job_education, job_skills, today))
                #
                # # 关闭数据库连接
                # db.close()

            # 判断是否是最后一页，如果不是则点击下一页按钮
            if page < job_len:
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
                            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/button')))
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
