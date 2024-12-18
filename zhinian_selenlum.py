from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import datetime
from DataMap.add_map import MapChina
from dbutils import DBUtils


# 打开首页
index_url = 'https://www.zhaopin.com/'
browser = webdriver.Edge()
browser.get(index_url)
wait = WebDriverWait(browser, 15)  # 等待最长15秒

# 模拟点击 "互联网/AI" 类别，展示职位分类
show_ele = browser.find_element(by=By.XPATH, value='//*[@id="root"]/main/div[1]/div[1]/ol/li[1]/nav/a')
show_ele.click()

# 获取今天的日期，用于标记数据抓取的日期
today = datetime.date.today().strftime('%Y-%m-%d')

# 获取职位分类
job_len_list = browser.find_elements(by=By.XPATH, value='//*[@id="root"]/main/div[1]/div[1]/ol/li[1]/nav/div/div[1]/a')
print(f"{len(job_len_list)}个分类")

# 遍历职位分类，进行职位信息抓取
for i in range(len(job_len_list)):

    current_a = browser.find_elements(by=By.XPATH, value='//*[@id="root"]/main/div[1]/div[1]/ol/li[1]/nav/div/div[1]/a')[i]
    current_category = current_a.find_element(by=By.XPATH, value='//*[@id="root"]/main/div[1]/div[1]/ol/li[1]/nav/div/h4').text
    sub_category = current_a.text  # 子分类

    current_a.click()
    # 等待新窗口打开
    wait.until(lambda driver: len(driver.window_handles) > 1)
    print("{}正在抓取{}--{}".format(today, current_category, sub_category))  # 打印当前抓取的信息

    # 获取所有窗口句柄
    window_handles = browser.window_handles
    browser.switch_to.window(window_handles[-1])  # 切换到最后打开的窗口
    print("页面跳转成功，当前 URL:", browser.current_url)

    # 获取当前页面中的所有职位信息（这里只是获取一次初始页面的，后续翻页会重新获取）
    job_detail = browser.find_elements(by=By.XPATH, value='/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div')
    job_page = browser.find_elements(by=By.XPATH, value='//*[@id="positionList-hook"]/div/div[2]/div[2]/div/a')
    job_len = len(job_page) - 2
    print(f"该分类职位有{job_len}页")
    # 地点选择按钮
    add_select_but = browser.find_element(by=By.XPATH,value='//*[@id="filter-hook"]/div/div[2]/div/div[1]/img')
    add_select_but.click()
    # 地点输入框
    add_input_but = browser.find_element(by=By.XPATH,value='//*[@id="filter-hook"]/div/div[2]/div[2]/div[2]/input')
    add_input_but.send_keys(MapChina.all_province[0])
    # 新增循环用于翻页操作，从第1页开始（因为初始已经在第1页获取过信息了），直到超过job_len页数
    for page in range(1, job_len + 1):
        # 获取当前页面中的所有职位信息（每次翻页后都要重新获取）
        job_detail = browser.find_elements(by=By.XPATH, value='/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div')
        print(f"正在抓取第{page}/{job_len}页")
        # 遍历每个职位，提取相关信息
        for j in range(1, len(job_detail) + 1):
            db = DBUtils('localhost', 'root', '623163', 'data_analysis')

            # 获取职位名称   ### 1. /html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div[1]/a
            try:  ##### 2.                                     /html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[2]/div[1]/div[1]/div[1]/a
                job_title = browser.find_element(by=By.XPATH, value=
                f'/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[{j}]/div[1]/div[1]/div[1]/a').text.strip()

            except:
                continue  # 如果职位标题不存在，则跳过

            try:
                # 尝试使用第一个 XPath 查找工作地点
                job_location = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         f'/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[{j}]/div[1]/div[1]/div[3]/div[1]/span'))
                ).text.strip()
            except (TimeoutException, NoSuchElementException):
                try:
                    # 如果第一个 XPath 查找失败，则使用第二个 XPath
                    job_location = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                             f'/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[{j}]/div[1]/div[1]/div[2]/div[1]/span'))
                    ).text.strip()
                except (TimeoutException, NoSuchElementException):
                    job_location = '不明'
            # f'/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[{i}]/div[1]/div[1]/div[2]/div[1]/span
            # 获取公司名称                                         //*[@id="positionList-hook"]/div/div[1]/div[2]/div[1]/div[2]/div[1]/a
            job_company = browser.find_element(by=By.XPATH, value=
            f'//*[@id="positionList-hook"]/div/div[1]/div[{j}]/div[1]/div[2]/div[1]/a').text.strip()
            ### 行业类型                                # /html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[2]/div[1]/div[2]/div[1]/a
            try:
                # 尝试使用第一个 XPath 查找工作地点
                job_industry = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         f'/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[{j}]/div[1]/div[2]/div[2]/div[3]'))
                ).text.strip()
            except (TimeoutException, NoSuchElementException):
                try:
                    # 如果第一个 XPath 查找失败，则使用第二个 XPath
                    job_industry = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                             f'/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[{j}]/div[1]/div[2]/div[2]/div[2]'))
                    ).text.strip()
                except (TimeoutException, NoSuchElementException):
                    job_industry = '不明'

            try:
                # 获取融资情况
                job_finance = browser.find_element(by=By.XPATH, value=
                "./div[1]/div/div[2]/ul/li[2]").text.strip()
            except:
                job_finance = '无'
            # 获取公司规模（若无则标记为“无”）    //*[@id="positionList-hook"]/div/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]
            try:
                job_scale = browser.find_element(by=By.XPATH, value=
                f'//*[@id="positionList-hook"]/div/div[1]/div[{j}]/div[1]/div[2]/div[2]/div[2]').text.strip()
            except:  # //*[@id="positionList-hook"]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]
                job_scale = "无"

            # 获取公司福利（若无则标记为“无”）
            try:
                job_welfare = browser.find_element(by=By.XPATH, value="./div[2]/div").text.strip()
            except:
                job_welfare = '无'

            # 获取薪资范围      //*[@id="positionList-hook"]/div/div[1]/div[2]/div[1]/div[1]/div[1]/p
            job_salary_range = browser.find_element(by=By.XPATH, value=
            f'//*[@id="positionList-hook"]/div/div[1]/div[{j}]/div[1]/div[1]/div[1]/p').text.strip()
            # 获取工作年限要求
            try:
                # 尝试使用第一个 XPath 查找工作地点
                job_experience = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         f'//*[@id="positionList-hook"]/div/div[1]/div[{j}]/div[1]/div[1]/div[3]/div[2]'))
                ).text.strip()
            except (TimeoutException, NoSuchElementException):
                try:
                    # 如果第一个 XPath 查找失败，则使用第二个 XPath
                    job_experience = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                             f'//*[@id="positionList-hook"]/div/div[1]/div[{j}]/div[1]/div[1]/div[2]/div[2]'))
                    ).text.strip()
                except (TimeoutException, NoSuchElementException):
                    job_experience = '经验不限'
            # 获取学历要求
            try:
                # 尝试使用第一个 XPath 查找工作地点
                job_education = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         f'/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[{j}]/div[1]/div[1]/div[3]/div[3]'))
                ).text.strip()
            except (TimeoutException, NoSuchElementException):
                try:
                    # 如果第一个 XPath 查找失败，则使用第二个 XPath
                    job_education = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                             f'/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[{j}]/div[1]/div[1]/div[2]/div[3]'))
                    ).text.strip()
                except (TimeoutException, NoSuchElementException):
                    job_education = '不限'

            # 获取技能要求（若无则标记为“无”）                                                                     /html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]
            try:
                job_skills = ','.join([skill.text.strip() for skill in browser.find_elements(by=By.XPATH,
                                                                                             value=f'/html/body/div[1]/div[4]/div[2]/div[2]/div/div[1]/div[{j}]/div[1]/div[1]/div[2]/div')])
            except:
                job_skills = '无'

            # 确定职位所在的省份
            province = ''
            city = job_location.split('·')[0]  # 提取城市名（从工作地点字符串中分离）
            for p, cities in MapChina.city_map.items():  # 遍历城市映射，查找匹配的省份
                if city in cities:
                    province = p
                    break

            # 打印抓取的职位信息
            print(f"{j}/{len(job_detail)}",current_category, sub_category, job_title, province, job_location, job_company, job_industry,
                  job_finance,
                  job_scale, job_welfare, job_salary_range, job_experience, job_education, job_skills)

            # 将抓取的数据保存到MySQL数据库
            db.insert_data(
                "insert into job_info(category, sub_category,job_title,province,job_location,job_company,job_industry,job_finance,job_scale,job_welfare,job_salary_range,job_experience,job_education,job_skills,create_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                args=(
                    current_category, sub_category, job_title, province, job_location, job_company, job_industry,
                    job_finance,
                    job_scale, job_welfare, job_salary_range, job_experience, job_education, job_skills, today))

            # 关闭数据库连接
            db.close()

        # 判断是否是最后一页，如果不是则点击下一页按钮（这里假设下一页按钮的XPath定位是准确的，可根据实际页面调整）
        if page < job_len:
            try:

                next_page_button = wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, '下一页')))
                browser.execute_script("arguments[0].scrollIntoView();", next_page_button)
                next_page_button.click()
                # 等待页面加载完成（可根据页面实际加载情况调整等待条件和时间）
                clear_but=wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/button')))
                clear_but.click()
                print("跳转页码成功,当前url",browser.current_url)
            except TimeoutException:
                print("下一页按钮点击超时或者页面加载超时，可能出现异常，继续下一个分类")
                continue
    # 返回到首页进行下一个分类抓取
    try:
        # 退回到首页
        browser.back()
        # 模拟点击 互联网/AI 展示出岗位分类
        show_ele = browser.find_element(by=By.XPATH, value='//*[@id="root"]/main/div[1]/div[1]/ol/li[1]/nav/a')
        show_ele.click()
    except:
        browser.get(index_url)  # 如果出错，重新打开首页
        show_ele = browser.find_element(by=By.XPATH, value='//*[@id="root"]/main/div[1]/div[1]/ol/li[1]/nav/a')
        show_ele.click()  # 重新点击“互联网/AI”类别

# 关闭浏览器
browser.quit()