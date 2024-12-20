
import pymysql
import pandas as pd
from pyecharts import options as opts

# 连接到 MySQL 数据库
conn = pymysql.connect(
    host="localhost",       # 数据库地址
    user="root",            # 数据库用户名
    password="623163",      # 数据库密码
    database="data_analysis"    # 数据库名称
)
# 直接用 pandas 从 MySQL 读取数据
query = "SELECT * FROM job_info"  # 替换为你的 SQL 查询语句
df = pd.read_sql(query, conn)

# 关闭连接
conn.close()
from DataMap.salary_map import SalaryMap

#进行数据映射
from DataMap.experience_map import expMap
from DataMap.education_map import educationMap
from DataMap.add_map import MapChina

df_data = df.copy()


# print(df_data.columns)
# 行业字段预处理
industry_data = df_data["job_industry"]
industry_list = []
for s_i in industry_data:
    industry_list.append(s_i)

# 技术字段预处理
skills_data = df_data["job_skills"]
skills_list = []
for s_k in skills_data:
    skills_list.append(s_k)

#词云生成
from Tool.wordCloudCreateTool import WordCloudCreate
wordCloud_ind = WordCloudCreate(industry_list, output_file="VisualResult/WordCloud/industryWordCloud.html")
wordCloud_ski = WordCloudCreate(skills_list, output_file="VisualResult/WordCloud/skillWordCloud.html")

#城市映射
location_list=df_data["job_location"]
result_location_dict = []
for s_l in location_list:
    s_category = MapChina.get_city_tier(s_l)
    result_location_dict.append(s_category)
df_data.loc[:, "job_location"] = result_location_dict

#薪水映射
salary_list = df_data["job_salary_range"]
result_salary_dict = []
for s_s in salary_list:
    s_category = SalaryMap.salaryMap(s_s)
    result_salary_dict.append(s_category)
df_data.loc[:, "job_salary_range"] = result_salary_dict

#省份映射
province_list = df_data["province"]
result_province_dict = []
for s_p in province_list:
    s_category = MapChina.get_province_name(s_p)
    result_province_dict.append(s_category)
df_data.loc[:, "province"] = result_province_dict

#学历映射
education_list = df_data["job_education"]
education_dict = []
for s_e in education_list:
    s_category = educationMap.map_education(s_e)
    education_dict.append(s_category)
df_data.loc[:, "job_education"] = education_dict

#经验映射
experience_list = df_data["job_experience"]
experience_dict = []
for s_i in experience_list:
    s_category = expMap.map_exp(s_i)
    experience_dict.append(s_category)
df_data.loc[:, "job_experience"] = experience_dict

#数据分析初分组
grouped_salary = df_data.groupby(['job_salary_range']).size().reset_index(name='count')
grouped_salary_by_location = df_data.groupby(['job_salary_range','job_location']).size().reset_index(name='count')
grouped_salary_by_education = df_data.groupby(['job_salary_range','job_education']).size().reset_index(name='count')
grouped_salary_by_experience = df_data.groupby(['job_salary_range','job_experience']).size().reset_index(name='count')
print(grouped_salary)


#薪资与经验的可视化分析
from pyecharts.charts import Bar
from pyecharts import options as opts
import pandas as pd
# 创建 DataFrame
df_view = pd.DataFrame(grouped_salary_by_experience)

# 按薪资段和经验类型分组，并求每组的人数总和
grouped = df_view.groupby(['job_salary_range', 'job_experience'], as_index=False)['count'].sum()

# 重塑数据，将经验类型变为列
pivoted = grouped.pivot(index='job_salary_range', columns='job_experience', values='count').reset_index()

# 定义薪资段的排序规则
salary_order = ["5k以下", "5k-7k", "7k-9k", "9k-12k", "12k-15k", "15k-18k", "18k-20k", "20k以上"]
# 定义经验年限的排序规则
experience_order = ["在校/应届", "1年以下", "1-3年", "3-5年", "5-10年", "10年以上"]
#将薪资段按照指定的顺序排序
pivoted['job_salary_range'] = pd.Categorical(pivoted['job_salary_range'], categories=salary_order, ordered=True)
pivoted = pivoted.sort_values(by='job_salary_range')


from Tool.colorByDataDivide import colorByDataDivide
#统计各个类别的数量
province_counts=df_data["province"].value_counts()

province_data = [(province, count) for province, count in province_counts.items()]

# 填充省份数据（没有数据的省份填充为0）
province_dict = {province: 0 for province in MapChina.get_all_provinces()}  # 初始化所有省份为 0
for province, count in province_data:
    mapped_province = MapChina.get_province_name(province)  # 映射省份名称
    if mapped_province in province_dict:
        province_dict[mapped_province] = count  # 填充有数据的省份
# 将省份数据转换为 pyecharts 可用的格式
formatted_data = [[province, province_dict[province]] for province in province_dict]
# 转换为数据框
df_data = pd.DataFrame(province_data, columns=['province', 'count'])
# 提取数值部分
province_values = df_data['count'].tolist()
pieces = colorByDataDivide.auto_generate_pieces(province_values)


from pyecharts.charts import Map

# 绘制可视化地图
c = (
    Map()
    .add("BOSS直聘计算机相关招聘信息概况", formatted_data, "china")  # 将数据传入 "china" 地图
    .set_global_opts(
        title_opts=opts.TitleOpts(title="BOSS直聘计算机相关岗位数量分布"),
        visualmap_opts=opts.VisualMapOpts(
            max_=max(province_dict.values()),  # 动态设置最大值
            is_piecewise=True,
            pieces=pieces,# 设置为分段显示
            range_text=["高", "低"]            # 显示文本
        ),
        tooltip_opts=opts.TooltipOpts(
            trigger="item",             # 鼠标悬停显示项
            formatter="{b}: {c}"         # 格式化显示省份和对应的数值
        )
    )
    .set_series_opts(
        label_opts=opts.LabelOpts(is_show=True, formatter="{c}"),  # 显示数值
        itemstyle_opts=opts.ItemStyleOpts(color="#69c0ff")          # 自定义颜色
    )
    .render(path='VisualResult/Chart/chinaMap.html')  # 渲染为 HTML 文件
)







# 创建 pyecharts 图表
c_i = (
    Bar()
    .add_xaxis(pivoted['job_salary_range'].tolist())  # 薪资段作为 X 轴
    .add_yaxis(series_name="经验不限", y_axis=pivoted['经验不限'].tolist())
    # .add_yaxis(series_name="在校/应届", y_axis=pivoted['在校/应届'].tolist())
    .add_yaxis(series_name="1年以下", y_axis=pivoted['1年以下'].tolist())
    .add_yaxis(series_name="1-3年", y_axis=pivoted['1-3年'].tolist())
    .add_yaxis(series_name="3-5年", y_axis=pivoted['3-5年'].tolist())
    .add_yaxis(series_name="5-10年", y_axis=pivoted['5-10年'].tolist())
    .add_yaxis(series_name="10年以上", y_axis=pivoted['10年以上'].tolist())
    .set_global_opts(
        title_opts=opts.TitleOpts(title="各经验薪资段人数统计"),
        xaxis_opts=opts.AxisOpts(type_="category", name="薪资段"),
        yaxis_opts=opts.AxisOpts(name="人数"),
        legend_opts=opts.LegendOpts(pos_top="5%"),  # 设置图例位置
        datazoom_opts=[opts.DataZoomOpts(orient="vertical"),opts.DataZoomOpts(orient="horizontal")] # 添加横纵数据调节

    )
    .render(path='VisualResult/Chart/salaryByex.html')  # 输出文件
)






# 创建 DataFrame
df_education = pd.DataFrame(grouped_salary_by_education)

# 按薪资段和学历分组，并求每组的人数总和
grouped = df_education.groupby(['job_salary_range', 'job_education'], as_index=False)['count'].sum()

# 重塑数据，将城市类型变为列
pivoted = grouped.pivot(index='job_salary_range', columns='job_education', values='count').reset_index()

# 定义薪资段的排序规则
salary_order = ["5k以下", "5k-7k", "7k-9k", "9k-12k", "12k-15k", "15k-18k", "18k-20k", "20k以上"]

# 将薪资段按照指定的顺序排序
pivoted['job_salary_range'] = pd.Categorical(pivoted['job_salary_range'], categories=salary_order, ordered=True)
pivoted = pivoted.sort_values(by='job_salary_range')



# 创建 pyecharts 图表
c_e = (
    Bar()
    .add_xaxis(pivoted['job_salary_range'].tolist())  # 薪资段作为 X 轴
    .add_yaxis(series_name="学历不限", y_axis=pivoted['学历不限'].tolist())
    # .add_yaxis(series_name="高中", y_axis=pivoted['高中'].tolist())
    .add_yaxis(series_name="大专", y_axis=pivoted['大专'].tolist())
    .add_yaxis(series_name="本科", y_axis=pivoted['本科'].tolist())
    .add_yaxis(series_name="硕士", y_axis=pivoted['硕士'].tolist())
    .set_global_opts(
        title_opts=opts.TitleOpts(title="各学历薪资段人数统计"),
        xaxis_opts=opts.AxisOpts(type_="category", name="薪资段"),
        yaxis_opts=opts.AxisOpts(name="人数"),
        legend_opts=opts.LegendOpts(pos_top="5%"),  # 设置图例位置
        datazoom_opts=[opts.DataZoomOpts(orient="vertical"),opts.DataZoomOpts(orient="horizontal")] # 添加横纵数据调节
    )
    .render(path='VisualResult/Chart/salaryByed.html')   # 输出文件
)

# 创建 DataFrame
df_view = pd.DataFrame(grouped_salary_by_location)

# 按薪资段和城市类型分组，并求每组的人数总和
grouped = df_view.groupby(['job_salary_range', 'job_location'], as_index=False)['count'].sum()

# 重塑数据，将城市类型变为列
pivoted = grouped.pivot(index='job_salary_range', columns='job_location', values='count').reset_index()

# 定义薪资段的排序规则
salary_order = ["5k以下", "5k-7k", "7k-9k", "9k-12k", "12k-15k", "15k-18k", "18k-20k", "20k以上"]

# 将薪资段按照指定的顺序排序
pivoted['job_salary_range'] = pd.Categorical(pivoted['job_salary_range'], categories=salary_order, ordered=True)
pivoted = pivoted.sort_values(by='job_salary_range')



# 创建 pyecharts 图表
c_l = (
    Bar()
    .add_xaxis(pivoted['job_salary_range'].tolist())  # 薪资段作为 X 轴
    .add_yaxis(series_name="其他城市", y_axis=pivoted['其他城市'].tolist())
    .add_yaxis(series_name="二线城市", y_axis=pivoted['二线城市'].tolist())
    .add_yaxis(series_name="新一线城市", y_axis=pivoted['新一线城市'].tolist())
    .add_yaxis(series_name="超一线城市", y_axis=pivoted['超一线城市'].tolist())
    .set_global_opts(
        title_opts=opts.TitleOpts(title="各城市薪资段人数统计"),
        xaxis_opts=opts.AxisOpts(type_="category", name="薪资段"),
        yaxis_opts=opts.AxisOpts(name="人数"),
        legend_opts=opts.LegendOpts(pos_top="5%"),  # 设置图例位置
        datazoom_opts=[opts.DataZoomOpts(orient="vertical"),opts.DataZoomOpts(orient="horizontal")] # 添加横纵数据调节
    )
    .render(path='VisualResult/Chart/salaryBylo.html')  # 输出文件
)