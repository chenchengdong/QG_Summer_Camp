import requests
from lxml import etree
import re
import time
import random

data_all = []  # 全部数据

url = 'https://weread.qq.com/web/category/100000'
# UA伪装
ua = 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'
header = {
    'user-agent': ua,
}
# 发送请求
response1 = requests.get(url=url, headers=header)
response1.encoding = 'utf-8'
rise_html = response1.text
# 数据解析
tree1 = etree.HTML(rise_html)
detailList = tree1.xpath('//ul[@class="ranking_content_bookList"]/li/a/@href')
for detail in detailList:
    data = {}  # 一条数据
    url = 'https://weread.qq.com' + detail
    response2 = requests.get(url=url, headers=header)
    response2.encoding = 'utf-8'
    detailHtml = response2.text  # 详情页面

    # 数据解析
    tree2 = etree.HTML(detailHtml)
    divHead = tree2.xpath('//div[@class="readerBookInfo_head"]')[0]
    data['keywords'] = tree2.xpath('//meta[@name="keywords"]/@content')[0]  # 关键词
    data['cover'] = divHead.xpath('.//img[@class="wr_bookCover_img"]/@src')[0]  # 封面url
    data['title'] = divHead.xpath('.//div[@class="bookInfo_right_header_title"]/text()')[0]  # 标题
    data['writer'] = divHead.xpath('.//a[@class="bookInfo_author link"]/text()')[0]  # 作者
    data['intro'] = tree2.xpath('//div[@class="bookInfo_intro"]/text()')[0]  # 简介

    signs = ['出版社', '出版时间', '字数', '分类']
    j = 1
    for i in range(4):
        try:
            sign = tree2.xpath('//div[@class="introDialog_content_pub_line"][{}]/span[1]/text()'.format(j))[0]
            if signs[i] == sign:
                data[signs[i]] = tree2.xpath('//div[@class="introDialog_content_pub_line"][{}]/span[2]/text()'.format(j))[0]  # 出版社,出版时间，字数，分类
                j += 1
            else:
                data[signs[i]] = ''
        except IndexError:
            sign = tree2.xpath('//div[@class="introDialog_content_pub_line long"][{}]/span[1]/text()'.format(j))[0]
            if signs[i] == sign:
                data[signs[i]] = tree2.xpath('//div[@class="introDialog_content_pub_line long"][{}]/span[2]/text()'.format(j))[0]  # 出版社,出版时间，字数，分类
                j += 1
            else:
                data[signs[i]] = ''

        # data['pressTime'] = tree2.xpath('//div[@class="introDialog_content_pub_line"][2]/span[2]/text()')[0]  # 出版时间
        # data['count'] = tree2.xpath('//div[@class="introDialog_content_pub_line"][3]/span[2]/text()')[0]  # 字数
        # data['tag'] = tree2.xpath('//div[@class="introDialog_content_pub_line"][4]/span[2]/text()')[0]  # 分类

    data['star'] = re.findall('\d.+', tree2.xpath('//div[@class="book_ratings_header"]/span/text()')[0])[0]  # 评分
    data['popular'] = tree2.xpath('//div[@class="book_rating_item_detail_count"]/span/text()')[0]  # 点评人数

    # n = 3
    # reviewList = []  # 三个用户评论
    # for i in range(n):
    #     reviewDict = {'personName': tree2.xpath('//span[@class="name"][{}]/text()'.format(i + 1))[0],  # 用户名
    #                   'personHead': tree2.xpath('//img[@class="wr_avatar_img"][{}]/@src'.format(i + 1))[0],  # 头像
    #                   'review': tree2.xpath('//p[@class="content content_Normal"][{}]'.format(i + 1))[0],  # 评论
    #                   }
    #     reviewList.append(reviewDict)
    # data['reviewList'] = reviewList
    # extractList = []  # 三个摘抄列表
    # for i in range(n):
    #     extract = tree2.xpath('//div[@class="marks_item_content"][{:}]/text()'.format(i + 1))[0]  # 摘抄
    #     extractList.append(extract)
    # data['extractList'] = extractList
    print(data)
    data_all.append(data)
    time.sleep(random.randint(0, 10))

with open('data_20.txt', 'w', encoding='utf-8') as f:
    for i in data_all:
        f.write(str(i) + '\n\n')

print('succeed!')
