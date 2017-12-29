import requests, sys, webbrowser, pyperclip
from bs4 import BeautifulSoup


def getSearch():

    #从命令行取查询词
    if len(sys.argv) > 1:
        search = ' '.join(sys.argv[1:])
        return search
    else:
    #从剪贴板中获取
        search = pyperclip.paste()
        return search


def getHTMLText(url, code='utf-8'):

    try:
        res = requests.get(url)
        res.raise_for_status()
        res.enconding = code
        return res.text
    except:
        return ''


def parserHTML(html):

    soup = BeautifulSoup(html, 'html.parser')
    

    #找到百度所有查询结果
    all_result = soup.select('.result')

    #只取结果前五个页面直接打开
    for i in range(5):
        SearchPage = all_result[i].select('h3 a')[0].get('href')
        webbrowser.open(SearchPage)


if __name__ == "__main__":

    search = getSearch()
    url = 'http://www.baidu.com/s?wd='
    url = url + search
    html = getHTMLText(url)
    parserHTML(html)