import requests
from requests.packages import urllib3
from requests.adapters import HTTPAdapter
import json
import re
import time
from wechatReading import nav_get_url
from author import author_info
from reviews import review_info
from dataSave import data_save

# UA伪装
ua = 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'
header = {
    'authority': 'weread.qq.com',
    'user-agent': ua,
    'Connection': 'close',
}
# get请求参数
param = {
    'maxIndex': '',
}
# 计数
cnt = 0

requests.packages.urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 5  # 重试次数
# 改变request的keep-alive设置
sess = requests.Session()
sess.mount('http://', HTTPAdapter(max_retries=3))
sess.mount('https://', HTTPAdapter(max_retries=3))
sess.keep_alive = False  # 关闭多余连接

# 调用请求函数获取导航栏url
navDict = nav_get_url(header)
cut = ['飙升榜', '新书榜', '总榜', '神作榜', '神作潜力榜']

# 文件保存
with open('./data/BookInformation.json', 'w', encoding='utf-8') as f:
    # 遍历导航栏网址
    for key in navDict.keys():
        if key in cut:
            continue  # 舍去几个排行榜
        else:
            sign = re.findall('\d+', navDict[key])[0]
            url = 'https://weread.qq.com/web/bookListInCategory/' + sign  # 每一个书籍栏目的url
            header['referer'] = 'https://weread.qq.com/web/category/' + sign
            # 发送请求
            maxPage = 520
            for i in range(0, maxPage, 20):  # 二十本一批
                param['maxIndex'] = str(i)
                response = sess.get(url=url, params=param, headers=header, verify=False, timeout=(7, 7))
                response.encoding = 'utf-8'
                books = response.json()['books']
                for book in books:
                    bookInfo = book['bookInfo']
                    bookId = bookInfo['bookId']
                    pointDetail = bookInfo['newRatingDetail']
                    pointCount = pointDetail['good'] + pointDetail['fair'] + pointDetail['poor']
                    bookInfoDict = {'title': bookInfo['title'], 'cover': bookInfo['cover'],
                                    'author': bookInfo['author'], 'translator': bookInfo['translator'],
                                    'publishTime': bookInfo['publishTime'], 'tag': bookInfo['category']}
                    try:
                        bookInfoDict["point"] = pointDetail['good'] * 1000 // pointCount / 10
                    except ZeroDivisionError:
                        bookInfoDict["point"] = 0
                    bookInfoDict['pointCount'] = pointCount
                    bookInfoDict['readingCount'] = book['readingCount']
                    bookInfoDict['goodCount'] = pointDetail['good']
                    bookInfoDict['starCount'] = 0
                    bookInfoDict['bookInfo'] = bookInfo['intro']
                    bookInfoDict['authorInfo'] = author_info(bookInfo['author'], header, sess)
                    bookInfoDict['review'] = review_info(bookId, sess)

                    json.dump(bookInfoDict, f, ensure_ascii=False, separators=(', ', ':'))
                    f.write('\n')
                    # 计数
                    cnt += 1
                    print('----- 第{}本书爬取成功 -----'.format(cnt))

                response.close()  # 关闭响应
                time.sleep(1)

print('全部书本爬取完毕！！！')

# 存储数据到数据库
# data_save()
