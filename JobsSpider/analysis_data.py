#!/usr/bin/env python
# -*- coding:utf-8 -*-

# python的数据分析工具：pandas，numpy
# python的图表工具：matplotlib

import pymysql
import pandas as pd
import numpy as np

# from scrapy.utils.project import get_project_settings
# settings = get_project_settings()
# connect = pymysql.connect(**settings['MYSQL_SETTINGS'])

from JobsSpider.settings import MYSQL_SETTINGS
connect = pymysql.connect(**MYSQL_SETTINGS)
cursor = connect.cursor()
# 1. 统计三个网站的工作总量占多少(饼状图)
sql1 = "select job_from, count(*) from job group by job_from"
cursor.execute(sql1)
result = cursor.fetchall()
result = dict(result)
print(result)
#
# import matplotlib.pyplot as plt
# from pylab import mpl
# #
# mpl.rcParams['font.sans-serif'] = ['FangSong']
# mpl.rcParams['axes.unicode_minus'] = False
#
# keys = list(result.keys())
# values = list(result.values())
# labels = keys
# total = sum(values)
# fracs = list(map(lambda x: x/total, values))
# index = values.index(max(values))
# explode = [0, 0, 0]
# explode[index] = 0.1
# plt.axes(aspect=1)
# plt.pie(x=fracs, labels=labels, explode=explode, autopct='%3.1f %%', shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6)
# plt.show()

# 2. 统计拉钩网 python，php，html的工作比例
# sql2 = "select job_type, count(*) from job WHERE job_from='拉勾网' GROUP BY job_type"
# cursor.execute(sql2)
# result = cursor.fetchall()
# result = dict(result)
# labels = result.keys()
# fracs = pd.Series(list(result.values())) / sum(result.values())
# explode = pd.Series(list(result.values())) // max(result.values()) * 0.1
# plt.axes(aspect=1)
# plt.title("拉勾网的职位比例饼状图")
# plt.pie(x=fracs, labels=labels, explode=explode, autopct='%3.1f %%', shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6)
# plt.show()

# 3. 统计 拉勾网 python 的各薪资分布区间的 工作数量
# 3000 以下
# 3000 - 5000
# 5000 - 8000
# 8000 - 10000
# 10000- 15000
# 15000 - 20000
# 20000以上

# sql3 = "select min_money, count(*) from job where job_type='python' and job_from='拉勾网' GROUP BY min_money"
# cursor.execute(sql3)
# result = cursor.fetchall()
# result = dict(result)
# money_info = {
#     3000: 0, 5000: 0, 8000: 0, 10000: 0, 15000: 0, 20000: 0,
# }
# for key, value in result.items():
#     for key1, value1 in money_info.items():
#         if key < key1:
#             value1 += value
#             money_info[key1] = value1
#             break
# s = result.values()
# money20000 = sum(result.values()) - sum(money_info.values())
# money_info[20001] = money20000
# num_list = list(money_info.values())
# n = list(money_info.keys())
# plt.title("拉勾网python专业薪资分布")
# plt.bar(list(money_info.keys()), num_list)
# plt.show()