import requests
from bs4 import BeautifulSoup
import os
import re


def getHTMLText(url, code='utf-8'):
    headers = {
        'Host': 'www.169pic.com',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = code
        data = r.content
        return data
    except:
        return 'fail'


def parserHTML(html):
    soup = BeautifulSoup(html, 'html.parser')

    all_pic = soup.select('p[align="center"] img')

    # 查找标题作为文件名, 因为有分页所以会有数字后缀, 用正则把数字给去掉
    name = soup.select('.position')[0].getText().split('>')[-1].strip()
    name = ''.join(re.findall(r'[^\x00-\xff]', name))

    if all_pic:
        print('Could not find image')
    else:
        try:
            os.makedirs('169pic/{}'.format(name), exist_ok=True)
            for pic in all_pic:
                picurl = pic.get('src')
                print('正在下载图片,地址:' + picurl)
                res = requests.get(picurl, headers={'Host': '724.169pp.net',
                                                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) '
                                                                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                                                    })
                res.raise_for_status()

                filename = ''.join(picurl.split('/')[-3:])

                with open('169pic/{}/{}'.format(name, filename), 'wb') as f:
                    f.write(res.content)
        except Exception as exc:
            print(exc)

    # 翻页设置
    page = soup.select('.pagelist li a')
    nextPage = page[-1]
    # 获得当前页面的网址去除最后的部分
    URL = soup.select('link[rel="alternate"]')[0].get('href')[:-10]

    # 下一个美女的链接
    nextHref = soup.select('.fenxianga a')[0].get('href')

    # 如果翻页为#则表示全都下载完, 返回下一个美女的链接
    if nextPage.get('href') != '#':
        url = URL + nextPage.get('href')
        return url
    return nextHref


if __name__ == "__main__":

    url = "http://www.169pic.com/xingganmeinv/2017/0514/38594.html"
    os.makedirs('169pic', exist_ok=True)

    html = getHTMLText(url)
    pics = parserHTML(html)

    while pics != '':
        html = getHTMLText(pics)
        pics = parserHTML(html)
