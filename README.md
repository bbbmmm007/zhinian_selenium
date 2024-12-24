
## 1. 环境准备
**安装项目依赖库**
```cmd
pip install -r requirements.txt
```
**创建数据库和表**
```sql
-- 删除现有数据库并重新创建
DROP DATABASE IF EXISTS data_analysis;
CREATE DATABASE IF NOT EXISTS data_analysis;

-- 使用数据库
USE data_analysis;

-- 删除现有表并重新创建
DROP TABLE IF EXISTS job_info;

-- 创建表并设置字符集和排序规则
CREATE TABLE data_analysis.job_info
(
    category         VARCHAR(255) NULL COMMENT '一级分类',
    sub_category     VARCHAR(255) NULL COMMENT '二级分类',
    job_title        VARCHAR(255) NULL COMMENT '岗位名称',
    province         VARCHAR(100) NULL COMMENT '省份',
    job_location     VARCHAR(255) NULL COMMENT '工作位置',
    job_company      VARCHAR(255) NULL COMMENT '企业名称',
    job_industry     VARCHAR(255) NULL COMMENT '行业类型',
    job_finance      VARCHAR(255) NULL COMMENT '融资情况',
    job_tpye         VARCHAR(255) NULL COMMENT '企业类型',
    job_scale        VARCHAR(255) NULL COMMENT '企业规模',
    job_salary_range VARCHAR(255) NULL COMMENT '薪资范围',
    job_experience   VARCHAR(255) NULL COMMENT '工作年限',
    job_education    VARCHAR(255) NULL COMMENT '学历要求',
    job_skills       VARCHAR(255) NULL COMMENT '技能要求',
    create_time      VARCHAR(50)  NULL COMMENT '抓取时间'
)
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  -- 设置字符集和排序规则

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
![](https://github.com/bbbmmm007/zhinian_selenium/blob/master/VisualResult/Picture/抓取效果.png)
![](https://github.com/bbbmmm007/zhinian_selenium/blob/master/VisualResult/Picture/111.png)
![](https://github.com/bbbmmm007/zhinian_selenium/blob/master/VisualResult/Picture/招聘概况.png)
![](https://github.com/bbbmmm007/zhinian_selenium/blob/master/VisualResult/Picture/3333.png)

常见报错情况
![](https://github.com/bbbmmm007/zhinian_selenium/blob/master/VisualResult/Picture/报错情况2.png)
一般在这两种报错情况下，多运行几次就能解决
![](https://github.com/bbbmmm007/zhinian_selenium/blob/master/VisualResult/Picture/成功.png)

下面的报错情况是因为抓取的数量到了一定，也会发生报错
![](https://github.com/bbbmmm007/zhinian_selenium/blob/master/VisualResult/Picture/抓取过程报错.png)
然后你可以记住到爬取到哪个地区出错了，然后在salary_map.py文件中的
all_province注释掉那个省份，防止抓取到重复的数据。
在连接数据库时，记得更换为自己的账号和密码，还有需要注意爬取网站时切勿使用其他浏览器打开网址。失败就是多重试几次
声明：
     本项目，只提供学习借鉴，切勿其他用途。
如果对你有帮助麻烦点个start,

