# -*- coding: utf-8 -*-
import scrapy
import re
from urllib.parse import urljoin
from urllib.parse import urlparse, parse_qsl
from JobsSpider.items import JobItem


class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['zhilian.com']
    custom_settings = {}
    start_urls = [
        'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%8C%97%E4%BA%AC%2B%E4%B8%8A%E6%B5%B7%2B%E5%B9%BF%E5%B7%9E%2B%E6%B7%B1%E5%9C%B3%2B%E6%AD%A6%E6%B1%89&kw=python&p=1&isadv=0',
        'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%8C%97%E4%BA%AC%2B%E4%B8%8A%E6%B5%B7%2B%E5%B9%BF%E5%B7%9E%2B%E6%B7%B1%E5%9C%B3%2B%E6%AD%A6%E6%B1%89&kw=php&p=1&isadv=0',
        'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%8C%97%E4%BA%AC%2B%E4%B8%8A%E6%B5%B7%2B%E5%B9%BF%E5%B7%9E%2B%E6%B7%B1%E5%9C%B3%2B%E6%AD%A6%E6%B1%89&kw=html&p=1&isadv=0',
    ]

    def parse(self, response):
        yield scrapy.Request(
            url=response.url,
            callback=self.parse_all_page,
            meta={},
            dont_filter=True,
        )

    def parse_one_page(self, response):
        table_list = response.xpath("//div[@id='newlist_list_content_table']/table")
        for table in table_list[1:]:
            job_name = table.xpath("tr/td/div/a//text()").extract()
            job_name = [x for x in job_name if x.strip()]
            job_name = "".join(job_name)
            job_detail_href = table.xpath("tr/td/div/a/@href").extract_first("")
            job_detail_href = urljoin(response.url, job_detail_href)
            job_money = table.xpath("tr/td[@class='zwyx']/text()").extract_first("面议")
            if job_money == "面议":
                max_money = min_money = 0
            elif "-" in job_money:
                min_money = job_money.split("-")[0]
                max_money = job_money.split("-")[1]
            elif "元以下" in job_money:
                min_money = max_money = job_money.replace("元以下", "")
            elif "元以上" in job_money:
                min_money = max_money = job_money.replace("元以上", "")
            else:
                min_money = max_money = 0
                print("薪资出现特殊情况{}".format(job_money))
                with open("money.txt", "a", encoding="utf-8") as f:
                    f.write(job_money+"\n")

            min_money = float(min_money)
            max_money = float(max_money)

            job_place = table.xpath("tr/td[@class='gzdd']/text()").extract_first("没有地点")
            if "-" in job_place:
                job_city = job_place.split("-")[0]
                job_area = job_place.split("-")[1]
            else:
                if "异地" in job_place or "招聘" in job_place:
                    job_city = job_area = "异地"
                else:
                    job_city, job_area = job_place, ""
            job_education = table.xpath("//tr/td/div/div/ul/li/span[contains(text(),'学历')]/text()").extract_first("不限")
            job_education = job_education.replace("学历：", "").replace("学历:", "")
            job_type = dict(parse_qsl(urlparse(response.url).query))['kw']
            company_name = table.xpath("tr/td[@class='gsmc']/a/text()").extract_first("").strip()
            meta = response.meta
            meta['job_name'] = job_name
            meta['job_money'] = job_money
            meta['max_money'] = max_money
            meta['min_money'] = min_money
            meta['job_date'] = ""
            meta['company_name'] = company_name
            meta['job_place'] = job_place
            meta['job_city'] = job_city
            meta['job_area'] = job_area
            meta['job_education'] = job_education
            meta['job_type'] = job_type
            yield scrapy.Request(
                url=job_detail_href,
                callback=self.parse_detail_page,
                meta=meta,
                dont_filter=True,
            )

    def parse_all_page(self, response):
        next_page = response.xpath("//a[@class='next-page nopress2']")
        pattern = re.compile(r"&p=(\d+)")
        page = pattern.findall(response.url)
        page = int(page[0]) if page else 1
        if not next_page:
            yield scrapy.Request(
                url=response.url,
                callback=self.parse_one_page,
                meta={},
                dont_filter=True
            )
            print("当前正在爬取{}页".format(page))
            url = response.url.replace("&p={}".format(page), "&p={}".format(page + 1))
            yield scrapy.Request(
                url=url,
                callback=self.parse_all_page,
                meta={},
                dont_filter=True,
            )
        else:
            print("爬取{}页完成".format(page))

    def parse_detail_page(self, response):
        job_fuli = response.xpath("//div[@class='welfare-tab-box']/span/text()").extract()
        job_fuli = [x for x in job_fuli if x.strip()]
        job_fuli = ",".join(job_fuli)
        if not job_fuli:
            job_fuli = "没有福利"

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
        item['job_education'] = meta['job_education']
        item['job_fuli'] = job_fuli
        item['job_from'] = "智联招聘"
        item['job_type'] = meta['job_type']
        item['job_detail_href'] = response.url
        yield item
