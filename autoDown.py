import pymysql
import pandas as pd
from pyecharts import options as opts

# 连接到 MySQL 数据库
conn = pymysql.connect(
    host="localhost",       # 数据库地址
    user="root",            # 数据库用户名
    password="623163",      # 数据库密码
    database="spider_db"    # 数据库名称
)
# 直接用 pandas 从 MySQL 读取数据
query = "SELECT * FROM job_info"  # 替换为你的 SQL 查询语句
df = pd.read_sql(query, conn)

# 关闭连接
conn.close()
from DataMap.salary_map import SalaryMap

output_path = "D:/MuMuwork/GitCangKu/bosszp-selenium/VisualResult/Chart/"
#进行数据映射
from DataMap.experience_map import expMap
from DataMap.education_map import educationMap

from DataMap.add_map import MapChina

df_data = df.copy()

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
grouped_salary_by_location = df_data.groupby(['job_salary_range','job_location']).size().reset_index(name='count')
grouped_salary_by_education = df_data.groupby(['job_salary_range','job_education']).size().reset_index(name='count')
grouped_salary_by_experience = df_data.groupby(['job_salary_range','job_experience']).size().reset_index(name='count')



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
    .render(output_path+"salary_by_experience.html")  # 输出文件
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
    .add_yaxis(series_name="高中", y_axis=pivoted['高中'].tolist())
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
    .render(output_path+"salary_by_education.html")  # 输出文件
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
    .render(output_path+"salary_by_location.html")  # 输出文件
)