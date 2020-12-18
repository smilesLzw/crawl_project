'''
批量抓取次幂数据上公众号的各项数据
python version: 3.7
'''

import logging
from urllib import parse

import xlwt
import requests
import cchardet
from lxml import etree

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


# 抓取搜索页面
def scrapy_search_page(keyword):
    url = 'https://www.ershicimi.com/search/account'
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'Cookie':
        'gr_user_id=7bcaa18a-3e7f-448c-b62e-120ff9e70978; UM_distinctid=175ac626db733b-0fac93585fc804-303464-144000-175ac626db8695; _ga=GA1.2.396193193.1604914933; Hm_lvt_ea5245057e456d6e5fe2fa739275b9dc=1608192256; ticket=yiXe9It627cq4C5fQDbrvAM8jVlFRBPW; remember_token=869|fa536281695b90672e772aec6740499b8308bfbab9c10443ea4b2f6fe7fce5fb93c862ed0954900f5c9686992ec01a8b14c3af4e720dc06d3d1c502d853387d5; session=.eJwdUMtuAjEM_JUqZ1R5EztO-BUWoTzsgloWaZeoB8S_19vL-CHbM-OXu-hP2a6yuePp5T6eFtxvWZfb8uUObh4cuc6DlMgQQeYRPfZ5JNAda9V5ZBLZc7GZnHhHjt6d3-eDnV9lu7rjcx1i1a27o5sm5KIcg9aGvhJSUKiFE-aqKQRl7pClTBNRU4EcQhKN3vuGk0IKvWsIEounJkq1BI-WA0MpHQhb0l224ISp9VS4qlZIjWMDjBXMWNtWvTwf37KYHpvsmJsxMhGJ0bei2ci0VfCcQ_QRqZPtrXKXe5X1skl7LN2-FgETwCcc3Nis_28wxezefyZrZsk.X9sRsA.pHS7U6kEm4L87GwdnwKYvRiyLxE; CNZZDATA1278946121=436446697-1604914360-https%253A%252F%252Fwww.google.com%252F%7C1608193325; Hm_lpvt_ea5245057e456d6e5fe2fa739275b9dc=1608197119',
    }
    params = {
        'q': keyword,
        'fensi': '',
        'read': '',
        'original_rate': '',
        'index': '',
        'open': '',
        'key': '',
        'cat_id': '',
    }
    try:
        res = requests.get(url=url, headers=headers, params=params)
        if res.status_code == 200:
            encoding = cchardet.detect(res.content)['encoding']
            html = res.content.decode(encoding)
            return html
        logging.error(
            f'get invalid status code {res.status_code} while scrapign {url}')
    except requests.RequestException:
        logging.error(f'error occurred while scraping {url}', exc_info=True)


# 解析搜索页面，获取第一页全部 bid 和 wxname
def get_bids_by_category(category):
    html = scrapy_search_page(category)
    selector = etree.HTML(html)
    bids = selector.xpath('//li[@class="author-item"]/@data-bid')
    wxnames = selector.xpath('//p[@class="tit"]/a/text()')
    # 去重两边多余字符
    wxnames = [wxname.strip() for wxname in wxnames]
    results = dict(zip(wxnames, bids))
    # result {wxnames: bids}
    return results


# 解析搜索页面，获取对应的 bid 集合
def get_bids_by_wxnames(wxnames):
    results = {}
    for wxname in wxnames:
        html = scrapy_search_page(wxname)
        selector = etree.HTML(html)
        bid = selector.xpath('//li[@class="author-item"]/@data-bid')[0]
        results[wxname] = bid
    return results


# 根据筛选条件爬取数据
def scrapy_index(bid, page, order_by=None):
    '''
    bid:
    page: 爬取页码
    order_by: 排序规则，默认按照点赞逆序排列
    '''
    url = 'https://www.ershicimi.com/api/stats'
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'Cookie':
        'gr_user_id=7bcaa18a-3e7f-448c-b62e-120ff9e70978; UM_distinctid=175ac626db733b-0fac93585fc804-303464-144000-175ac626db8695; _ga=GA1.2.396193193.1604914933; remember_token=869|fa536281695b90672e772aec6740499b8308bfbab9c10443ea4b2f6fe7fce5fb93c862ed0954900f5c9686992ec01a8b14c3af4e720dc06d3d1c502d853387d5; session=eyJfZnJlc2giOmZhbHNlLCJ1c2VyX2lkIjoiODY5In0.X9x7og.MuUAOv-MsXswCPt05cmFg3_eL78; CNZZDATA1278946121=436446697-1604914360-https%253A%252F%252Fwww.google.com%252F%7C1608281723; Hm_lvt_ea5245057e456d6e5fe2fa739275b9dc=1608192256,1608285092; Hm_lpvt_ea5245057e456d6e5fe2fa739275b9dc=1608285092',
    }
    _order_by = '-old_like_num'
    if order_by:
        _order_by = order_by
    params = {
        'page': page,
        'page_size': 20,
        'bid': bid,
        'start_at': '2019-12-18',
        'end_at': '2020-12-17',
        'position': 'all',
        'include': 'articles',
        'order_by': _order_by
    }
    try:
        res = requests.get(url=url, headers=headers, params=params)
        if res.status_code == 200:
            return res.json()
        logging.error(
            f'get invalid status code {res.status_code} while scraping {url}')
    except requests.RequestException:
        logging.error(f'error occurred while scraping {url}', exc_info=True)


# 提取数据
def parse_page(wxname, bid, pages, order_by=None):
    logging.info(f'scraping {wxname}...')
    data_list = []
    for page in range(pages):
        json_data = scrapy_index(bid, page + 1)
        for item in json_data.get('data').get('articles'):
            published_at = item.get('published_at')
            published_at = published_at[:10]
            title = item.get('title')
            link = item.get('content_url')
            read_num = item.get('read_num')
            old_like_num = item.get('old_like_num')
            like_num = item.get('like_num')
            data = {
                'wxname': wxname,
                'published_at': published_at,
                'title': title,
                'link': link,
                'read_num': read_num,
                'old_like_num': old_like_num,
                'like_num': like_num,
            }
            data_list.append(data)
    logging.info(f'scrape {wxname} done!')
    return data_list


def save_to_xls(data, filename=None):
    '''
    filename: xxx.xls
    '''
    _filename = '公众号数据分析.xls'
    logging.info(f'start save data to xls!')
    # 定义 excle  工作表
    xls = xlwt.Workbook()
    sheet = xls.add_sheet('sheet1')
    sheet.write(0, 0, '公众号')
    sheet.write(0, 1, '时间')
    sheet.write(0, 2, '标题')
    sheet.write(0, 3, '链接')
    sheet.write(0, 4, '阅读数')
    sheet.write(0, 5, '点赞数')
    sheet.write(0, 6, '在看数')
    for key, val in enumerate(data):
        sheet.write(key + 1, 0, val.get('wxname'))
        sheet.write(key + 1, 1, val.get('published_at'))
        sheet.write(key + 1, 2, val.get('title'))
        sheet.write(key + 1, 3, val.get('link'))
        sheet.write(key + 1, 4, val.get('read_num'))
        sheet.write(key + 1, 5, val.get('old_like_num'))
        sheet.write(key + 1, 6, val.get('like_num'))

    if filename:
        _filename = filename
    try:
        xls.save(_filename)
        logging.info(f'data saved successful!')
    except:
        pass


# 根据公众号名称批量抓取
def scrape_by_wxname(wxnames, page):
    '''
    wxname: 要抓取的微信公众号名列表 ['痴海', ]
    page: 要抓取的页数
    '''
    datas = []

    # 开始抓取数据
    results = get_bids_by_wxnames(wxnames)
    for wxname, bid in results.items():
        data = parse_page(wxname, bid, page)
        datas += data
    return datas


# 根据类别批量抓取
def scrape_by_category(categories, page):
    '''
    categories: 分类
    page: 要抓取的页数
    '''
    datas = []
    results = get_bids_by_category(categories)
    for wxname, bid in results.items():
        data = parse_page(wxname, bid, page)
        datas += data
    return datas


if __name__ == '__main__':
    '''
    使用示例
    '''
    wxnames = [
        '裸睡的猪',
    ]
    datas = scrape_by_wxname(wxnames, 2)
    filename = '裸睡的猪.xls'
    save_to_xls(datas, filename)

    categories = 'Python'
    datas = scrape_by_category(categories, 2)
    filename = 'Python公众号数据分析.xls'
    save_to_xls(datas, filename)
