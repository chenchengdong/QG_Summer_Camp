import time
import requests
from requests.packages import urllib3
from requests.adapters import HTTPAdapter


def review_info(book_id: str, sess2) -> list:
    requests.packages.urllib3.disable_warnings()
    requests.adapters.DEFAULT_RETRIES = 5  # 重试次数
    url = 'https://weread.qq.com/web/review/list'
    # UA伪装
    ua = 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'
    header2 = {
        'authority': 'weread.qq.com',
        'user-agent': ua,
        'Connection': 'close',
    }
    # get参数
    param2 = {
        'bookId': book_id,
        'listType': '3',
        'maxIdx': '0',
        'count': '3',
        'listMode': '2',
        'code': 'fake',
        'synckey': '0',
    }

    # 发起请求
    response2 = sess2.get(url=url, params=param2, headers=header2, verify=False, timeout=(7, 7))
    response2.encoding = 'utf-8'
    review_json = response2.json()

    # 数据解析
    review_data = []
    for i in range(3):
        try:
            username = review_json['reviews'][i]['review']['author']['name']  # 用户名
            username = "".join(username)
            photo = review_json['reviews'][i]['review']['author']['avatar']  # 头像url
            photo = "".join(photo)
            review_text = review_json['reviews'][i]['review']['content']  # 评论文字
            review_text = "".join(review_text)
            # try:
            #     review_star = review_json['reviews'][i]['review']['star']  # 用户评分
            # except KeyError:
            #     review_star = ''
        except (IndexError, KeyError):
            username = ' '
            photo = ' '
            review_text = ' '
        review = "-".join((username, photo, review_text))  # 一个用户的评论信息
        review_data.append(review)
        # print(review_data)

    response2.close()
    time.sleep(1)
    return review_data


if __name__ == '__main__':
    print('ok')
