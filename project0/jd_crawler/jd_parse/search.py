# _*_ coding: utf-8 _*_
# @Author: smiles
# @Time  : 2020/12/20 22:22
# @File  : search.py
import json
import time

from bs4 import BeautifulSoup

def search_item(html):
    '''
    解析器
    :param html:
    :return:
    '''
    result = []
    soup = BeautifulSoup(html, 'lxml')
    li_ele_array = soup.select('ul[class^="gl-warp"] li[class="gl-item"]')
    for li_ele in li_ele_array:
        try:
            img = li_ele.select('.p-img')
            price = li_ele.select('.p-price')
            name = li_ele.select('div[class^="p-name"]')
            shop = li_ele.select('.p-shop')
            icons = li_ele.select('.p-icons')

            result.append([
                img[0].a.img.attrs['data-lazy-img'] if img else '',
                price[0].strong.i.text.strip() if price else '',
                name[0].a.text.strip() if name else '',
                shop[0].span.a.attrs['title'].strip() if shop else '',
                json.dumps([x.text.strip() for x in icons[0].select('i')]),
                time.strftime('%Y-&m-%d')
            ])
        except Exception as e:
            print(e.args)
    return result
