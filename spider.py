import requests
import json
import hashlib
from urllib import parse

def get_x_sign(api):
    x_sign = "X"
    m = hashlib.md5()
    m.update((api + "WSUDD").encode())
    x_sign = x_sign + m.hexdigest()
    return x_sign


def get_proxy():
    return requests.get("http://0.0.0.0:5010/get/").text


def spider(keyword, d_page, sort_by='general', ):
    """
    :param keyword:
    :param d_page: 页数
    :param sort_by: general：综合排序，hot_desc：热度排序
    :return:
    """
    host = 'https://www.xiaohongshu.com'
    url = '/fe_api/burdock/weixin/v2/search/notes?keyword={}&sortBy={}' \
          '&page={}&pageSize=20&prependNoteIds=&needGifCover=true'.format(parse.quote(keyword),
                                                                          sort_by,
                                                                          d_page + 1)
    # page 从0开始, 所以这里+1

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'Referer': 'https://servicewechat.com',
        'Authorization': '',  # 在这里填入抓到的header
        'X-Sign': get_x_sign(url)
    }
    # proxies = {'http': "http://{}".format(get_proxy())}
    # 记得使用代理池

    resp = requests.get(url=host + url, headers=headers, timeout=5)
    if resp.status_code == 200:
        res = json.loads(resp.text)
        return res['data']['notes'], res['data']['totalCount']
    else:
        print('Fail:{}'.format(resp.text))


note, total_count = spider('要搜索的关键词', d_page=1)
print(note)
