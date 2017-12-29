import requests
import os


def getHTMLText(url, code='utf-8'):
    headers = {
        'Host': '724.169pp.net',
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


def main():
    os.makedirs('169pic', exist_ok=True)

    yearm = 201712
    num = 193
    i = 1
    url = "http://724.169pp.net/169mm/{}/{}/{}.jpg".format(yearm, num, i)

    while num != 100:
        os.makedirs('169pic/{}'.format(num), exist_ok=True)

        while True:
            picContent = getHTMLText(url)
            if picContent == 'fail':
                break
            filename = str(i) + '.jpg'
            print('正在下载{}文件下的第{}张'.format(num, i))
            with open('169pic/{}/{}'.format(num, filename), 'wb') as f:
                f.write(picContent)
            i = i + 1
            url = "http://724.169pp.net/169mm/{}/{}/{}.jpg".format(yearm, num, i)
        num = num - 1
        i = 1
        url = "http://724.169pp.net/169mm/{}/{}/{}.jpg".format(yearm, num, i)


if __name__ == "__main__":
    main()
