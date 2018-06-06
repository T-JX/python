from elasticsearch_dsl import DocType, Completion, Keyword, Text, Boolean, Integer, Date, Float
# 引入链接函数
from elasticsearch_dsl.connections import connections
# 引入elasticsearch中的分析器
from elasticsearch_dsl.analysis import CustomAnalyzer
# 创建ES连接，

connections.create_connection(hosts=["127.0.0.1"])

# 自定义分词器对象
class MyAnalyzer(CustomAnalyzer):
    # 返回分词器对象
    def get_analysis_definition(self):
        return {}

# 创建分析器对象
# filter 忽略大小写
ik_analyzer = MyAnalyzer('ik_max_word', filter=['lowercase'])


class JobType(DocType):
    # 搜索建议字段
    # Completion 用来做搜索建议的类型
    # 不能直接指定分词器名称，需要指定一个自定义对象
    suggest = Completion(analyzer=ik_analyzer)

    job_name = Text(analyzer='ik_max_word')
    job_money = Text()
    max_money = Float()
    min_money = Float()
    job_date = Text()
    company_name = Text(analyzer='ik_max_word')
    job_place = Text(analyzer='ik_max_word')
    job_city = Text()
    job_area = Text(analyzer='ik_max_word')
    job_education = Text()
    job_fuli = Text(analyzer='ik_max_word')
    job_from = Text()
    job_type = Text(analyzer='ik_max_word')
    job_detail_href = Text()

    class Meta:
        # index 索引名（数据库）
        index = 'jobs'
        # doc_type 类型（表名称）
        doc_type = 'job'


if __name__ == '__main__':
    JobType.init()
