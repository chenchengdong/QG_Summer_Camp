import time
import requests
from requests.packages import urllib3
from requests.adapters import HTTPAdapter
from lxml import etree


def author_info(author: str, head, sess1) -> str:
    requests.packages.urllib3.disable_warnings()
    requests.adapters.DEFAULT_RETRIES = 5  # 重试次数
    url_author = 'https://weread.qq.com/web/search/books'
    # UA伪装
    header1 = head
    # get请求参数
    param1 = {
        'authority': 'weread.qq.com',
        'author': author,
    }

    # 发送请求
    response1 = sess1.get(url=url_author, params=param1, headers=header1, verify=False, timeout=(7, 7))
    response1.encoding = 'utf-8'
    author_html = response1.text
    # 数据解析
    tree = etree.HTML(author_html)
    try:
        intro = tree.xpath('//p[@class="search_bookDetail_header_detail search_bookDetail_header_detail_Normal"]/text()')[0]
    except IndexError:
        intro = ''
    # print(intro)

    response1.close()
    time.sleep(1)
    return intro
