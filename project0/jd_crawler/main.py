# _*_ coding: utf-8 _*_
# @Author: smiles
# @Time  : 2020/12/20 22:12
# @File  : main.py
import os
import sys
import json
import random
import logging

import cchardet
import requests
import pymysql

sys.path.append(os.getcwd())
from jd_crawler.jd_parse.search import search_item
from jd_crawler.settings import MYSQL_LOCAL_CONF

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'cookie': 'areaId=2;'
}

def save_item(item, keyword):
    '''
    存储器
    :param item:
    :return:
    '''
    SQL = 'INSERT INTO jd_search(img, price, name, shop, icons, sta_date) VALUES(%s, %s, %s, %s, %s, %s)'
    cursor.executemany(SQL, item)
    mysql_server.commit()
    logging.info(f'{keyword} data saved done!')



def request_search(keyword):
    '''
    下载器
    - 加上代理 IP
    :param keyword:
    :return:
    '''
    url = 'https://search.jd.com/Search'
    params = {
        'keyword': keyword,
        'wq': keyword,
        'psort': 3,
        'click': 0
    }
    # proxy = random.choice(ip_array)
    # proxies = {
    #     'http': f'http://{proxy["ip"]}:{proxy["port"]}',
    #     'https': f'https://{proxy["ip"]}:{proxy["port"]}'
    # }

    logging.info(f'scraping {url}...')
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            encoding = cchardet.detect(response.content)['encoding']
            html = response.content.decode(encoding, errors='ignore')
            return html
        logging.error(f'get invalid status code {response.status_code} while scraping {url}')
    except requests.RequestException:
        logging.error(f'error occurred while scraping {url}', exc_info=True)


def main():
    '''
    主函数/调度器
    :return:
    '''
    for keyword in keyword_array:
        result = request_search(keyword)
        item_array = search_item(result)
        save_item(item_array, keyword)

    print('done!')



if __name__ == '__main__':
    mysql_server = pymysql.connect(**MYSQL_LOCAL_CONF)
    cursor = mysql_server.cursor()
    # 代替任务生产者
    keyword_array = ['键盘', '鼠标', '显示器', '显卡', '单反']
    # json_data = json.loads()
    # ip_array = json_data['data']

    main()

