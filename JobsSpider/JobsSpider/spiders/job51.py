# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import JobItem
# from scrapy_redis.spiders import RedisSpider


# class Job51Spider(RedisSpider):
class Job51Spider(scrapy.Spider):
    name = 'job51'
    allowed_domains = ['job51.com']
    start_urls = [
        'https://search.51job.com/list/010000%252C020000%252C030200%252C040000%252C180200,000000,0000,00,9,99,python,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
        'https://search.51job.com/list/010000%252C020000%252C030200%252C040000%252C180200,000000,0000,00,9,99,php,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
        'https://search.51job.com/list/010000%252C020000%252C030200%252C040000%252C180200,000000,0000,00,9,99,html,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
    ]
    # redis_key = 'job51:start_urls'

    def parse(self, response):
        total_page = response.xpath("//*[contains(text(), '页，到第')]/text()").extract_first("")
        total_page = total_page.replace("页，到第", "").replace("共", "")
        total_page = int(total_page) if total_page.isdigit() else 1
        for page in range(1, total_page+1):
            url = response.url.replace("1.html", "{}.html".format(page))
            yield scrapy.Request(
                url=url,
                callback=self.parse_one_page,
                meta={},
                dont_filter=True
            )

    def parse_one_page(self, response):
        job_list = response.xpath("//div[@class='el']")
        for job in job_list:
            job_name = job.xpath("p/span/a/@title").extract_first("").strip()
            job_detail_href = job.xpath("p/span/a/@href").extract_first("").strip()
            job_money = job.xpath("span[@class='t4']/text()").extract_first("面议").strip()
            pattern = re.compile(r"[-/年月日万千元]")
            list1 = pattern.split(job_money)
            if job_money == "面议":
                min_money = max_money = 0
            elif "-" in job_money:
                max_money, min_money = list1[1], list1[0]
            else:
                min_money = max_money = list1[0]
            min_money = float(min_money)
            max_money = float(max_money)

            if "万" in job_money:
                min_money *= 10000
                max_money *= 10000
            elif "千" in job_money:
                min_money *= 1000
                max_money *= 1000
            if "年" in job_money:
                min_money //= 12
                max_money //= 12
            elif "日" in job_money:
                min_money *= 30
                max_money *= 30

            job_date = job.xpath("span[@class='t5']/text()").extract_first("").strip()
            company_name = job.xpath("span[@class='t2']/a/@title").extract_first("").strip()
            job_place = job.xpath("span[@class='t3']/text()").extract_first("").strip()
            if "-" in job_place:
                job_city = job_place.split("-")[0]
                job_area = job_place.split("-")[1]
            else:
                if "异地" in job_place or "招聘" in job_place:
                    job_city = job_area = "异地"
                else:
                    job_city, job_area = job_place, ""

            pattern = re.compile("00,9,99,(.*?),2")
            result = pattern.findall(response.url)
            job_type = result[0]

            meta = response.meta
            meta['job_name'] = job_name
            meta['job_money'] = job_money
            meta['max_money'] = max_money
            meta['min_money'] = min_money
            meta['job_date'] = job_date
            meta['company_name'] = company_name
            meta['job_place'] = job_place
            meta['job_city'] = job_city
            meta['job_area'] = job_area
            meta['job_type'] = job_type

            if job_detail_href:
                yield scrapy.Request(
                    url=job_detail_href,
                    callback=self.parse_detail_page,
                    meta=meta,
                    dont_filter=True,
                )

    def parse_detail_page(self, response):
        pattern = re.compile(r"本科|专科|大专|硕士|博士|初中|高中|中技|小学")
        result = pattern.findall(response.text)
        result = set(result)
        job_education = "、".join(result)
        if not job_education:
            job_education = "无限制"
        meta = response.meta
        item = JobItem()
        item['job_name'] = meta['job_name']
        item['job_money'] = meta['job_money']
        item['max_money'] = meta['max_money']
        item['min_money'] = meta['min_money']
        item['job_date'] = meta['job_date']
        item['company_name'] = meta['company_name']
        item['job_place'] = meta['job_place']
        item['job_city'] = meta['job_city']
        item['job_area'] = meta['job_area']
        item['job_education'] = job_education
        item['job_fuli'] = ""
        item['job_from'] = "51job"
        item['job_type'] = meta['job_type']
        item['job_detail_href'] = response.url
        yield item
