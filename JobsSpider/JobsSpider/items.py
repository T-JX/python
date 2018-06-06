# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from .es_model import JobType
from elasticsearch_dsl.connections import connections

# 创建连接获取连接对象
es = connections.create_connection(hosts=["127.0.0.1"])

class JobsspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 将传递进来的字段进行分词处理
# index 分词字段信息
def conduct_suggest(index, *args):
    '''
    :param index: 操作的索引
    :param args: 需要进行分词的内容
    :return: 返回分词之后的列表
    '''
    # 调用分词接口
    # 1.index 操作的索引
    use_words = set()
    suggest = []
    for text,weight in args:
        wrods = es.indices.analyze(
            index=index,
            body={
                'analyzer': 'ik_max_word',
                'text':text
            },
            params={
                'filter':['lowercase']
            }
        )
        # 取出分词结果
        analyzer_word = set([dic['token'] for dic in wrods['tokens']])
        # 有多个字段需要分词去除重复的分词结果
        new_words = analyzer_word - use_words
        # 将此次的分词结果存入列表中
        suggest.append({'input':list(new_words), 'weight':weight})
        # 记录分词结果
        use_words = analyzer_word

    return suggest



class JobItem(scrapy.Item):
    job_name = scrapy.Field()
    job_money = scrapy.Field()
    max_money = scrapy.Field()
    min_money = scrapy.Field()
    job_date = scrapy.Field()
    company_name = scrapy.Field()
    job_place = scrapy.Field()
    job_city = scrapy.Field()
    job_area = scrapy.Field()
    job_education = scrapy.Field()
    job_fuli = scrapy.Field()
    job_from = scrapy.Field()
    job_type = scrapy.Field()
    job_detail_href = scrapy.Field()

    # 将数据保存到es搜索服务器中
    def save_es(self):
        # 创建搜索服务器数据模型对象
        # job_name = Text(analyzer='ik_max_word')
        # job_money = Integer()
        # max_money = Integer()
        # min_money = Integer()
        # job_date = Date()
        # company_name = Text(analyzer='ik_max_word')
        # job_place = Text(analyzer='ik_max_word')
        # job_city = Text()
        # job_area = Text(analyzer='ik_max_word')
        # job_education = Text()
        # job_fuli = Text(analyzer='ik_max_word')
        # job_from = Text()
        # job_type = Text(analyzer='ik_max_word')

        job = JobType()
        # 给属性赋值，从传递进来的item中取值
        job.job_name = self['job_name']
        job.job_money = self['job_money']
        job.job_date = self['job_date']
        job.job_city = self['job_city']
        job.job_area = self['job_area']
        job.job_education = self['job_education']
        job.job_from = self['job_from']
        job.min_money = self['min_money']
        job.max_money = self['max_money']
        job.company_name = self['company_name']
        job.job_place = self['job_place']
        job.job_fuli = self['job_fuli']
        job.job_type = self['job_type']
        job.job_detail_href = self['job_detail_href']

        # 将该条数据对应分词信息进行保存
        # 将某些字段进行分词处理，将处理后的数据保存在ES服务器中

        job.suggest = conduct_suggest('jobs', (job.job_name, 10), (job.company_name, 9), (job.job_place, 8), (job.job_area, 7), (job.job_type, 6), (job.job_fuli, 5))

        job.save()
