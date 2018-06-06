#!/usr/bin/env python
# -*- coding:utf-8 -*-
from scrapy.commands import ScrapyCommand
from scrapy.utils.project import get_project_settings


class Command(ScrapyCommand):

    def short_desc(self):
        return "执行所有爬虫"

    def run(self, args, opts):
        # settings = get_project_settings()
        # print(settings['BOT_NAME'])
        spider_list = self.crawler_process.spiders.list()
        for name in spider_list:
            self.crawler_process.crawl(name, **opts.__dict__)
        self.crawler_process.start()


