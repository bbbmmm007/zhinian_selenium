
## 1. 环境准备
**安装项目依赖库**
```cmd
pip install -r requirements.txt
```
**创建数据库和表**
```sql
drop database if exists data_analysis;
create database if not exists data_analysis;
       
use data_analysis;

drop table if exists job_info;
create table data_analysis.job_info
(
    category         varchar(255) null comment '一级分类',
    sub_category     varchar(255) null comment '二级分类',
    job_title        varchar(255) null comment '岗位名称',
    province         varchar(100) null comment '省份',
    job_location     varchar(255) null comment '工作位置',
    job_company      varchar(255) null comment '企业名称',
    job_industry     varchar(255) null comment '行业类型',
    job_finance      varchar(255) null comment '融资情况',
    job_tpye         varchar(255) null comment '企业类型',
    job_scale        varchar(255) null comment '企业规模',
    job_salary_range varchar(255) null comment '薪资范围',
    job_experience   varchar(255) null comment '工作年限',
    job_education    varchar(255) null comment '学历要求',
    job_skills       varchar(255) null comment '技能要求',
    create_time      varchar(50)  null comment '抓取时间'
);
```

```
本项目是基于selenium和pyecharts，对智联招聘的IT互联网的招聘数据，实现自动抓取和可视化
项目结构
zhilian_selenium_pyecharts
  ---DataMap                            # 数据映射工具文件夹
     ---add_map.py                      # 地点字段处理
     ---education_map.py                # 学历字段处理
     ---experience_map.py               # 经验字段处理
     ---salary_map.py                   # 薪水字段处理

以省和直辖市为单位进行抓取.

  ---Tool                               # 工具文件夹
     ---colorByDataDivide.py            # 进行在地图上展示的数量于颜色的划分处理
     ---wordCloudCreateTool.py          # 自定义词云生成工具
     ---dbtool.py                       # 数据库工具

  ---VisualResult                       # 可视化结果文件夹
     ---Chart                           # 数据图表
     ---WordCloud # 词云
  ---datalooking.ipynb                  # 数据可视化代码 jupyter
  ---zhinian_selenlum.py                # 抓取数据代码
  ---datalook.py                        # 数据可视化 py
  ---requirements.txt                   # 需要的包
```

部分效果展示
![](C:\Users\TY\Pictures\Screenshots\抓取效果.png)
![](C:\Users\TY\Pictures\Screenshots\111.png)
![](C:\Users\TY\Pictures\Screenshots\2222.png)
![](C:\Users\TY\Pictures\Screenshots\3333.png)

常见报错情况
![](C:\Users\TY\Pictures\Screenshots\报错情况2.png)
一般在这两种报错情况下，多运行几次就能解决
![](C:\Users\TY\Pictures\Screenshots\成功.png)

下面的报错情况是因为抓取的数量到了一定，也会发生报错
![](C:\Users\TY\Pictures\Screenshots\抓取过程报错.png)
然后你可以记住到爬取到哪个地区出错了，然后在salary_map.py文件中的
all_province注释掉那个省份，防止抓取到重复的数据。
在连接数据库时，记得更换为自己的账号和密码，还有需要注意爬取网站时切勿使用其他浏览器打开网址。失败就是多重试几次
声明：
     本项目，只提供学习借鉴，切勿其他用途。
如果对你有帮助麻烦点个start,

