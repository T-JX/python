# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import JobItem
import re


class LagouSpider(scrapy.Spider):
    next_page = True
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_urls = [
        'https://www.lagou.com/jobs/positionAjax.json?px=default&city=北京&needAddtionalResult=false',
        'https://www.lagou.com/jobs/positionAjax.json?px=default&city=上海&needAddtionalResult=false',
        'https://www.lagou.com/jobs/positionAjax.json?px=default&city=广州&needAddtionalResult=false',
        'https://www.lagou.com/jobs/positionAjax.json?px=default&city=深圳&needAddtionalResult=false',
        'https://www.lagou.com/jobs/positionAjax.json?px=default&city=杭州&needAddtionalResult=false',
        'https://www.lagou.com/jobs/positionAjax.json?px=default&city=苏州&needAddtionalResult=false',
        'https://www.lagou.com/jobs/positionAjax.json?px=default&city=西安&needAddtionalResult=false',
        'https://www.lagou.com/jobs/positionAjax.json?px=default&city=天津&needAddtionalResult=false',
        'https://www.lagou.com/jobs/positionAjax.json?px=default&city=南京&needAddtionalResult=false',
        'https://www.lagou.com/jobs/positionAjax.json?px=default&city=成都&needAddtionalResult=false',
    ]

    headers = {
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Accept-Language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        'Accept-Encoding': "gzip, deflate, br",
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'X-Requested-With': "XMLHttpRequest",
        'X-Anit-Forge-Token': "None",
        'X-Anit-Forge-Code':"0",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0",
        'Referer': "https://www.lagou.com/jobs/list_python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=",
        'Cookie': "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1523492977,1523864475,1523924034; _ga=GA1.2.1521840397.1523492979; index_location_city=%E5%85%A8%E5%9B%BD; user_trace_token=20180412082943-98390180-3de8-11e8-b9e0-525400f775ce; LGUID=20180412082943-9839044a-3de8-11e8-b9e0-525400f775ce; JSESSIONID=ABAAABAACEBACDGCDD59597BDACAEB3C6A3550F461404CC; LGRID=20180417081408-3f6a5266-41d4-11e8-88d8-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1523924048; TG-TRACK-CODE=index_search"
    }

    jobs = ['python', 'php', 'html']

    def start_requests(self):
        for url in self.start_urls:
            for job in self.jobs:
                a = {"first": 'False', "pn": '1', "kd": job, }
                referer = self.headers['Referer']
                pattern = re.compile(r"list_.*?\?")
                referer = pattern.sub("list_{}?".format(job), referer)

                pattern = re.compile(r"city=(.*?)&")
                city = pattern.findall(url)
                city = city[0] if city else "北京"
                referer = pattern.sub(city, referer)
                self.headers['Referer'] = referer

                yield scrapy.FormRequest(url=url, callback=self.parse, meta={"page": 1}, dont_filter=True, method="POST", formdata=a, headers=self.headers)

    def parse(self, response):
        print(response.text)
        page = response.meta['page']
        result = json.loads(response.text)
        pageNo = result['content']['pageNo']
        job_list = result['content']['positionResult']['result']
        job_type = result['content']['positionResult']['queryAnalysisInfo']['positionName']
        for job in job_list:
            job_name = job['positionName']
            positionId = job['positionId']
            job_education = job['education']
            job_money = job['salary'].lower().replace("以上", "").replace("以下", "")
            job_date = job['createTime']
            job_city = job['city'] if job['city'] else ""
            job_area = job['district'] if job['district'] else ""
            job_fuli = ",".join(job['companyLabelList'])
            if "-" in job_money:
                min_money, max_money = job_money.split("-")
            else:
                min_money = max_money = job_money
            min_money = float(min_money.replace("k", "000"))
            max_money = float(max_money.replace("k", "000"))
            company_name = job['companyFullName']

            item = JobItem()
            item['job_name'] = job_name
            item['job_money'] = job_money
            item['max_money'] = max_money
            item['min_money'] = min_money
            item['job_date'] = job_date
            item['company_name'] = company_name
            item['job_place'] = job_city+"-"+job_area if job_city and job_area else "没有地区"
            item['job_city'] = job_city
            item['job_area'] = job_area
            item['job_education'] = job_education
            item['job_fuli'] = job_fuli
            item['job_from'] = "拉勾网"
            item['job_type'] = job_type
            item['job_detail_href'] = "https://www.lagou.com/jobs/{}.html".format(positionId)
            yield item
        page += 1
        print("------------------正在爬取第{}页数据,{}".format(page, result['content']['pageNo']))
        if page - pageNo == 1:
            yield scrapy.Request(url=response.url, callback=self.parse_next_page, meta={"page": page, }, dont_filter=True, headers=self.headers)

    def parse_next_page(self, response):
        page = response.meta['page']
        for job in self.jobs:
            a = {"first": 'False', "pn": str(page), "kd": job}
            yield scrapy.FormRequest(url=response.url, callback=self.parse, meta={"page": page}, dont_filter=True, formdata=a, method="POST",headers=self.headers)
