# _*_ coding: utf-8 _*_
# @Author: smiles
# @Time  : 2020/12/20 23:45
# @File  : search_test.py

from pprint import pprint

from jd_crawler.jd_parse.search import search_item

file = r'F:\lzw\PythonRunner\crawl_project\project0\jd_crawler\test\jd_search.html'
with open(file, 'r', encoding='utf-8') as f:
    result = search_item(f.read())