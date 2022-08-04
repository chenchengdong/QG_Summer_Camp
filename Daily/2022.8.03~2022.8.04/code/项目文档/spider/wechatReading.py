import requests
from lxml import etree
import json


def nav_get_url(head):
    url_nav = 'https://weread.qq.com/web/category/100000'
    # 发送请求
    response = requests.get(url=url_nav, headers=head, verify=False, timeout=(7, 7))
    response.encoding = 'utf-8'
    wcr_html = response.text
    # 数据解析
    tree = etree.HTML(wcr_html)  # 实例化etree对象
    nav_list = tree.xpath('//ul[@class="ranking_list"]/li/a')
    nav_dict = {}
    for nav in nav_list:
        try:
            nav_title = nav.xpath('./span/text()')[0]  # 获取列表名称
        except IndexError:
            nav_title = nav.xpath('./text()')[0]
        nav_url = 'https://weread.qq.com' + nav.xpath('./@href')[0]
        nav_dict[nav_title] = nav_url
        # print(nav_title)
        # print(nav_url)
    return nav_dict


if __name__ == '__main__':
    # UA伪装
    ua = 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'
    header = {
        'user-agent': ua,
    }
    # 调用请求函数
    navDict = nav_get_url(header)
    # 永久保存数据
    fp = open('all.json', 'w', encoding='utf-8')
    json.dump(navDict, fp=fp, ensure_ascii=False, separators=(',\n', ': '))
    fp.close()

    print('finish!!!')
