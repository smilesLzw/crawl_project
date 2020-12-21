import re

import execjs
import requests

headers = {
    'origin': 'https://fanyi.baidu.com',
    'referer': 'https://fanyi.baidu.com/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

session = requests.Session()
session.headers = headers


def make_execjs_object():
    with open('js1/baidu_translate.js', 'r') as f:
        js = f.read()
    return execjs.compile(js)


get_sign = make_execjs_object()


def get_token_gtk():
    url = 'https://fanyi.baidu.com/'
    for i in range(3):
        response = session.get(url)
        token = re.findall("token: '(.*?)'", response.text)[0]
        gtk = re.findall("window.gtk = '(.*?)'", response.text)[0]
        print(f'{[i]} token: {token}')
        print(f'{[i]} gkt: {gtk}')

    return token, gtk


def translate_result(keyword):
    token, gtk = get_token_gtk()

    sign = get_sign.call('e', keyword, gtk)
    if sign:
        url = 'https://fanyi.baidu.com/v2transapi?from=zh&to=en'
        form_data = {
            'from': 'zh',
            'to': 'en',
            'query': keyword,
            'transtype': 'enter',
            'simple_means_flag': 3,
            'sign': sign,
            'token': token,
            'domain': 'common',
        }

        response = session.post(url, data=form_data)
        result = re.findall('"dst":"(.*?)"', response.text)[0]
    return result


if __name__ == '__main__':
    keyword = input('请输入中文: ')
    result = translate_result(keyword)
    print(keyword + ': ' + result)
