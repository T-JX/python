#!/usr/bin/env python
# -*- coding:utf-8 -*-

from urllib.parse import urlparse, parse_qsl
import re
url = "http://www.baidu.com?a=1&d=4&b=2&c=3"
result = urlparse(url=url)
result = parse_qsl(result.query)
result = dict(result)
print(result['d'])

content = "学历水平本科、硕士以上,大学本科学习计算机专业，负责教授小学内容"
# if '中专' in content:
#     job_education = "中专"

pattern = re.compile(r"中专|本科|硕士|小学")
result = pattern.findall(content)
print(result)
